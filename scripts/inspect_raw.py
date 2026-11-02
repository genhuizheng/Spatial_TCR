#!/usr/bin/env python3
"""Inspect every raw file under a root directory and write a Markdown report
of what each file kind actually contains, plus a full file inventory TSV.

Read-only. Nothing under the root is modified.
Pickles are NEVER unpickled (unpickling runs arbitrary code); their opening
bytes are scanned with pickletools to list the classes and keys they use.

Optional libraries (the report says which were missing):
    pyarrow  -> Parquet schema and rows (Xenium cells / transcripts / boundaries)
    h5py     -> HDF5 / 10x .h5 / .h5ad structure, read lazily (no full load)

Usage:
    python3 inspect_raw.py --root data/raw --out metadata/RAW_DATA_FORMATS.md \
        --inventory metadata/raw_file_inventory.tsv
"""
import argparse
import ast
import collections
import datetime
import gzip
import io
import os
import pickletools
import platform
import re
import shutil
import socket
import struct
import sys
import tarfile
import tempfile
import zipfile

LIBS = {}
try:
    import h5py  # noqa: F401
    LIBS["h5py"] = h5py.__version__
except Exception:  # noqa: BLE001
    h5py = None
try:
    import pyarrow
    import pyarrow.parquet as pq
    LIBS["pyarrow"] = pyarrow.__version__
except Exception:  # noqa: BLE001
    pq = None
try:
    import numpy as np
    LIBS["numpy"] = np.__version__
except Exception:  # noqa: BLE001
    np = None

TEXT_EXT = (".csv", ".tsv", ".txt", ".mtx", ".json", ".md", ".bed", ".tab")
SKIP_CONTENT = re.compile(r"^cfg.*\.txt$")       # SCP bulk-download configs carry signed URLs
CELL_MAX = 60                                    # truncate long cell values in tables
LINE_MAX = 400                                   # truncate long text lines


# ----------------------------------------------------------------- helpers
def human(n):
    if n is None or n < 0:
        return "?"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1000 or unit == "TB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.2f} {unit}"
        n /= 1000.0
    return "?"


def logical_ext(name):
    low = name.lower()
    for ext in (".parquet.gz", ".ome.tif.gz", ".tif.gz", ".tar.gz", ".csv.gz", ".tsv.gz",
                ".txt.gz", ".mtx.gz", ".html.gz", ".fastq.gz", ".json.gz", ".soft.gz"):
        if low.endswith(ext):
            return ext
    return os.path.splitext(low)[1] or "(none)"


def kind_of(name):
    """Collapse sample-specific parts of a file name so files of the same kind group.

    Leading tokens without digits are kept (e.g. 'new_format', 'Puck_object'),
    everything up to the last token containing a digit is replaced by '*',
    and the remaining tail is kept: GSM9054471_Nov_21_24_230322_cells.parquet.gz
    -> '*cells.parquet.gz'; Puck_220408_13_clones.txt -> 'Puck*clones.txt'."""
    ext = logical_ext(name)
    stem = name[: len(name) - len(ext)] if ext != "(none)" and name.lower().endswith(ext) else name
    tokens = re.split(r"[_]", stem)
    digit_idx = [i for i, t in enumerate(tokens) if re.search(r"\d", t)]
    if not digit_idx:
        return name
    first, last = digit_idx[0], digit_idx[-1]
    lead = "_".join(tokens[:first])
    tail = "_".join(tokens[last + 1:])
    return f"{lead}*{tail}{ext}" if tail else f"{lead}*{ext}"


def clip(v, n=CELL_MAX):
    s = v.decode("utf-8", "replace") if isinstance(v, (bytes, bytearray)) else str(v)
    s = s.replace("\n", " ").replace("|", "/")
    return s if len(s) <= n else s[: n - 3] + "..."


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(clip(x) for x in r) + " |")
    return "\n".join(out)


def open_maybe_gz(path):
    return gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb")


def head_lines(fh, n=6, max_bytes=2_000_000):
    """First n lines of a binary stream, decoded, each clipped to LINE_MAX."""
    data = fh.read(max_bytes)
    lines = data.split(b"\n")[:n]
    return [ln.decode("utf-8", "replace").rstrip("\r")[:LINE_MAX] for ln in lines]


def sniff_delim(line):
    counts = {d: line.count(d) for d in ("\t", ",", ";", " ")}
    d = max(counts, key=counts.get)
    return d if counts[d] else None


# --------------------------------------------------------------- inspectors
def inspect_text(path):
    out = []
    with open_maybe_gz(path) as fh:
        lines = head_lines(fh)
    if lines and not path.lower().endswith((".md", ".md.gz")):
        d = sniff_delim(lines[0])
        if d:
            names = {"\t": "tab", ",": "comma", ";": "semicolon", " ": "space"}
            out.append(f"delimiter: {names[d]}; columns in first line: {len(lines[0].split(d))}")
    out.append("first lines:")
    out.append("```text")
    out.extend(lines)
    out.append("```")
    raw = os.path.getsize(path)
    if not path.endswith(".gz") and raw < 300_000_000:
        with open(path, "rb") as fh:
            n = sum(chunk.count(b"\n") for chunk in iter(lambda: fh.read(1 << 24), b""))
        out.append(f"line count: {n:,}")
    elif path.endswith(".gz") and raw < 60_000_000:
        with gzip.open(path, "rb") as fh:
            n = sum(chunk.count(b"\n") for chunk in iter(lambda: fh.read(1 << 24), b""))
        out.append(f"line count (decompressed): {n:,}")
    return out


def inspect_fastq(path):
    with open_maybe_gz(path) as fh:
        lines = head_lines(fh, n=8)
    return ["first two reads:", "```text", *lines, "```"]


def inspect_parquet(path, tmpdir):
    if pq is None:
        return ["pyarrow not available: schema not read"]
    src = path
    tmp = None
    if path.endswith(".gz"):
        tmp = os.path.join(tmpdir, os.path.basename(path)[:-3])
        with gzip.open(path, "rb") as fi, open(tmp, "wb") as fo:
            shutil.copyfileobj(fi, fo, 1 << 24)
        src = tmp
    try:
        with open(src, "rb") as fh:  # explicit handle so the temp copy can be removed afterwards
            pf = pq.ParquetFile(fh)
            meta = pf.metadata
            out = [f"rows: {meta.num_rows:,}; row groups: {meta.num_row_groups}; columns: {meta.num_columns}"]
            out.append(md_table(["column", "arrow type"], [[f.name, str(f.type)] for f in pf.schema_arrow]))
            kv = pf.schema_arrow.metadata or {}
            keys = [k.decode("utf-8", "replace") for k in kv if not k.startswith(b"ARROW")]
            if keys:
                out.append("key-value metadata keys: " + ", ".join(keys[:20]))
            batch = next(pf.iter_batches(batch_size=5), None)
            if batch is not None:
                cols = batch.schema.names
                rows = list(zip(*[batch.column(i).to_pylist() for i in range(len(cols))]))
                out.append("first rows:")
                out.append(md_table(cols, rows))
        return out
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)


def _plain(v):
    """numpy scalars / bytes / nested lists -> plain Python values for display."""
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if hasattr(v, "item") and not hasattr(v, "__len__"):
        return v.item()
    return v


def _h5_value_preview(ds, n=3):
    try:
        if hasattr(ds, "shape") and ds.shape == ():
            return clip(_plain(ds[()]))
        vals = ds[: n] if getattr(ds, "ndim", 1) == 1 else ds[: n, ...]
        if hasattr(vals, "tolist"):
            vals = vals.tolist()
        return clip(_plain(vals), 120)
    except Exception as exc:  # noqa: BLE001
        return f"(unreadable: {exc})"


def inspect_hdf5(path):
    if h5py is None:
        return ["h5py not available: structure not read"]
    out = []
    with h5py.File(path, "r") as f:
        enc = f.attrs.get("encoding-type")
        is_h5ad = path.endswith(".h5ad") or (enc is not None and "anndata" in clip(enc))
        if is_h5ad:
            out.extend(_inspect_h5ad(f))
        if "matrix" in f and isinstance(f["matrix"], h5py.Group):
            out.extend(_inspect_10x_h5(f["matrix"]))
        out.append("HDF5 tree (depth <= 3):")
        out.append("```text")
        lines = []

        def walk(g, prefix, depth):
            for k in list(g.keys())[:40]:
                obj = g[k]
                if isinstance(obj, h5py.Dataset):
                    lines.append(f"{prefix}{k}  dataset shape={obj.shape} dtype={obj.dtype}")
                else:
                    et = obj.attrs.get("encoding-type")
                    tag = f" [{clip(et)}]" if et is not None else ""
                    lines.append(f"{prefix}{k}/{tag}")
                    if depth < 3:
                        walk(obj, prefix + "  ", depth + 1)
            if len(g.keys()) > 40:
                lines.append(f"{prefix}... {len(g.keys()) - 40} more")
        walk(f, "", 1)
        out.extend(lines[:250])
        out.append("```")
    return out


def _h5ad_frame(g, name):
    """Describe an AnnData obs/var group (new format) or compound dataset (old format)."""
    rows = []
    if isinstance(g, h5py.Dataset) and g.dtype.names:  # legacy compound table
        for col in g.dtype.names:
            rows.append([col, str(g.dtype[col]), _h5_value_preview(g[col][:3])])
        return [f"{name}: legacy compound table, {g.shape[0]:,} rows",
                md_table(["column", "dtype", "first values"], rows)]
    idx = clip(g.attrs.get("_index", "_index"))
    order = [clip(c) for c in g.attrs.get("column-order", [])] or \
        [k for k in g.keys() if k not in (idx, "__categories")]
    legacy_cats = g["__categories"] if "__categories" in g else None  # anndata < 0.8 layout
    n = None
    for c in order:
        if c not in g:
            continue
        obj = g[c]
        if legacy_cats is not None and c in legacy_cats and isinstance(obj, h5py.Dataset):
            cats = [_plain(x) for x in legacy_cats[c][()]]
            n = obj.shape[0]
            first = [str(cats[i]) for i in obj[:3] if 0 <= i < len(cats)]
            rows.append([c, f"categorical ({len(cats)} levels: {', '.join(map(str, cats[:8]))})",
                         ", ".join(first)])
        elif isinstance(obj, h5py.Group) and "codes" in obj:
            cats = obj["categories"]
            n = obj["codes"].shape[0]
            first = [clip(cats[i]) for i in obj["codes"][:3] if i >= 0] if len(cats) else []
            rows.append([c, f"categorical ({len(cats)} levels)", ", ".join(first)])
        elif isinstance(obj, h5py.Dataset):
            n = obj.shape[0]
            rows.append([c, str(obj.dtype), _h5_value_preview(obj)])
        else:
            rows.append([c, "group", ""])
    head = f"{name}: {n if n is not None else '?'} rows, {len(order)} columns; index '{idx}'"
    if idx in g and isinstance(g[idx], h5py.Dataset):
        head += f" (first ids: {_h5_value_preview(g[idx])})"
    return [head, md_table(["column", "dtype", "first values"], rows[:80])]


def _inspect_h5ad(f):
    out = ["AnnData (.h5ad) summary:"]
    if "X" in f:
        X = f["X"]
        if isinstance(X, h5py.Group):
            shape = X.attrs.get("shape", X.attrs.get("h5sparse_shape"))
            et = clip(X.attrs.get("encoding-type", "sparse"))
            out.append(f"X: {et}, shape={tuple(int(s) for s in shape) if shape is not None else '?'}, "
                       f"nnz={X['data'].shape[0]:,}, dtype={X['data'].dtype}")
        else:
            out.append(f"X: dense, shape={X.shape}, dtype={X.dtype}")
    for name in ("obs", "var"):
        if name in f:
            try:
                out.extend(_h5ad_frame(f[name], name))
            except Exception as exc:  # noqa: BLE001
                out.append(f"{name}: unreadable ({exc})")
    for name in ("obsm", "varm", "layers", "obsp"):
        if name in f and isinstance(f[name], h5py.Group) and len(f[name].keys()):
            items = []
            for k in f[name].keys():
                o = f[name][k]
                items.append(f"{k} {o.shape if isinstance(o, h5py.Dataset) else '(group)'}")
            out.append(f"{name}: " + "; ".join(items))
    if "uns" in f and isinstance(f["uns"], h5py.Group):
        keys = list(f["uns"].keys())
        out.append(f"uns keys ({len(keys)}): " + ", ".join(keys[:40]))
    return out


def _inspect_10x_h5(m):
    out = ["10x feature-barcode matrix (.h5):"]
    try:
        shape = tuple(int(s) for s in m["shape"][()])
        out.append(f"shape (features x barcodes): {shape}; nnz={m['data'].shape[0]:,}")
        out.append(f"first barcodes: {_h5_value_preview(m['barcodes'])}")
        if "features" in m:
            feat = m["features"]
            names = [clip(x) for x in feat["name"][()]]
            ftype = [clip(x) for x in feat["feature_type"][()]] if "feature_type" in feat else ["?"] * len(names)
            cnt = collections.Counter(ftype)
            rows = []
            for t, c in cnt.most_common():
                ex = [n for n, tt in zip(names, ftype) if tt == t][:4]
                rows.append([t, f"{c:,}", ", ".join(ex)])
            out.append(md_table(["feature_type", "n features", "examples"], rows))
            extra = [k for k in feat.keys() if k not in ("name", "feature_type", "id", "genome")]
            if extra:
                out.append("other feature fields: " + ", ".join(extra))
    except Exception as exc:  # noqa: BLE001
        out.append(f"(unreadable: {exc})")
    return out


def _is_textlike(name):
    low = name.lower()
    base = low[:-3] if low.endswith(".gz") else low
    return base.endswith(TEXT_EXT)


def _member_head(fh, name):
    raw = fh.read(2_000_000)
    if name.lower().endswith(".gz"):
        try:
            raw = gzip.decompress(raw)
        except Exception:  # noqa: BLE001  (truncated stream: decompress what we have)
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read1(2_000_000) if raw else b""
    return [ln.decode("utf-8", "replace").rstrip("\r")[:LINE_MAX] for ln in raw.split(b"\n")[:5]]


def _archive_summary(entries):
    """entries: list of (name, size). Returns listing lines."""
    out = [f"members: {len(entries):,} files, {human(sum(s for _, s in entries))} uncompressed"]
    tops = collections.Counter()
    for n, _ in entries:
        parts = n.strip("/").split("/")
        tops["/".join(parts[:2]) if len(parts) > 2 else parts[0]] += 1
    if any("/" in n.strip("/") for n, _ in entries) and len(tops) > 1:
        out.append("top-level folders (first two levels) and file counts:")
        out.append("```text")
        out.extend(f"{c:6d}  {t}" for t, c in tops.most_common(40))
        out.append("```")
    out.append("first members:")
    out.append("```text")
    out.extend(f"{human(s):>10}  {n}" for n, s in entries[:40])
    if len(entries) > 40:
        out.append(f"... {len(entries) - 40} more")
    out.append("```")
    return out


def inspect_tar(path, max_heads=6):
    entries, heads, seen = [], [], set()
    with tarfile.open(path, "r|*") as tf:
        for m in tf:
            if not m.isfile():
                continue
            entries.append((m.name, m.size))
            base = os.path.basename(m.name)
            key = kind_of(base)
            if len(heads) < max_heads and key not in seen and _is_textlike(base) and m.size < 500_000_000:
                fh = tf.extractfile(m)
                if fh is not None:
                    heads.append((m.name, _member_head(fh, base)))
                    seen.add(key)
    out = _archive_summary(entries)
    for name, lines in heads:
        out.append(f"head of `{name}`:")
        out.extend(["```text", *lines, "```"])
    return out


def inspect_zip(path, max_heads=6):
    with zipfile.ZipFile(path) as zf:
        infos = [i for i in zf.infolist() if not i.is_dir() and "__MACOSX" not in i.filename]
        entries = [(i.filename, i.file_size) for i in infos]
        out = _archive_summary(entries)
        seen = set()
        for i in infos:
            if len(seen) >= max_heads:
                break
            base = os.path.basename(i.filename)
            key = kind_of(base)
            if key in seen or not _is_textlike(base) or i.file_size > 500_000_000:
                continue
            with zf.open(i) as fh:
                lines = _member_head(fh, base)
            seen.add(key)
            out.append(f"head of `{i.filename}`:")
            out.extend(["```text", *lines, "```"])
    return out


def inspect_npz(path):
    out = []
    with zipfile.ZipFile(path) as zf:
        rows = []
        for i in zf.infolist():
            with zf.open(i) as fh:
                magic = fh.read(6)
                if magic != b"\x93NUMPY":
                    rows.append([i.filename, "not .npy", ""])
                    continue
                major = fh.read(2)[0]
                hlen = struct.unpack("<H" if major == 1 else "<I", fh.read(2 if major == 1 else 4))[0]
                hdr = ast.literal_eval(fh.read(hlen).decode("latin1"))
                rows.append([i.filename, str(hdr.get("shape")), str(hdr.get("descr"))])
        out.append(md_table(["array", "shape", "dtype"], rows))
    return out


def inspect_pickle(path, nbytes=8_000_000):
    """Scan opcodes of the first bytes without executing anything."""
    with open(path, "rb") as fh:
        data = fh.read(nbytes)
    proto, globals_, strings = None, collections.Counter(), []
    recent = []
    try:
        for op, arg, _pos in pickletools.genops(io.BytesIO(data)):
            if op.name == "PROTO":
                proto = arg
            elif op.name == "GLOBAL":
                globals_[str(arg).replace(" ", ".")] += 1
            elif op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "BINUNICODE8"):
                recent = (recent + [arg])[-2:]
                if len(strings) < 60 and isinstance(arg, str) and len(arg) < 60 and arg not in strings:
                    strings.append(arg)
            elif op.name == "STACK_GLOBAL" and len(recent) == 2:
                globals_[f"{recent[0]}.{recent[1]}"] += 1
    except Exception:  # noqa: BLE001  (we stop at the truncation point by design)
        pass
    out = [f"pickle protocol: {proto}; scanned first {human(len(data))} without unpickling"]
    if globals_:
        out.append("classes / functions referenced: " + ", ".join(g for g, _ in globals_.most_common(25)))
    if strings:
        out.append("first short strings (attribute names, keys): " + ", ".join(strings[:60]))
    out.append("note: loading this needs the original authors' Python classes; treat as untrusted code.")
    return out


def _tiff_first_ifd(buf):
    """Parse the first IFD of a (Big)TIFF from bytes. Returns {tag: value} for a few tags."""
    if len(buf) < 16 or buf[:2] not in (b"II", b"MM"):
        return None
    e = "<" if buf[:2] == b"II" else ">"
    ver = struct.unpack(e + "H", buf[2:4])[0]
    big = ver == 43
    if big:
        off = struct.unpack(e + "Q", buf[8:16])[0]
    else:
        off = struct.unpack(e + "I", buf[4:8])[0]
    if off + 8 > len(buf):
        return {"_ifd_offset_beyond_head": off}
    n = struct.unpack(e + ("Q" if big else "H"), buf[off: off + (8 if big else 2)])[0]
    pos = off + (8 if big else 2)
    size = 20 if big else 12
    types = {1: ("B", 1), 2: ("s", 1), 3: ("H", 2), 4: ("I", 4), 5: ("II", 8), 16: ("Q", 8), 12: ("d", 8)}
    want = {256: "width", 257: "height", 258: "bits_per_sample", 259: "compression",
            262: "photometric", 277: "samples_per_pixel", 270: "image_description",
            282: "x_resolution", 296: "resolution_unit", 322: "tile_width", 323: "tile_length"}
    tags = {}
    for i in range(min(n, 200)):
        ent = buf[pos + i * size: pos + (i + 1) * size]
        if len(ent) < size:
            break
        tag, typ = struct.unpack(e + "HH", ent[:4])
        cnt = struct.unpack(e + ("Q" if big else "I"), ent[4:12] if big else ent[4:8])[0]
        valfield = ent[12:20] if big else ent[8:12]
        if tag not in want or typ not in types:
            continue
        fmt, w = types[typ]
        total = w * cnt
        if total <= len(valfield):
            raw = valfield[:total]
        else:
            vo = struct.unpack(e + ("Q" if big else "I"), valfield)[0]
            raw = buf[vo: vo + total] if vo + total <= len(buf) else None
        if raw is None:
            tags[want[tag]] = "(beyond scanned head)"
            if want[tag] == "image_description":
                tags["_desc_at"] = (struct.unpack(e + ("Q" if big else "I"), valfield)[0], total)
        elif typ == 2:
            tags[want[tag]] = raw.rstrip(b"\x00").decode("utf-8", "replace")
        elif typ == 5:
            a, b = struct.unpack(e + "II", raw[:8])
            tags[want[tag]] = a / b if b else None
        else:
            tags[want[tag]] = struct.unpack(e + fmt[0] * cnt, raw[: w * cnt])[0] if cnt else None
    tags["bigtiff"] = big
    return tags


def read_head(path, nbytes):
    """Up to nbytes of (decompressed) content; tolerates a truncated gzip stream."""
    chunks, have = [], 0
    with open_maybe_gz(path) as fh:
        try:
            while have < nbytes:
                c = fh.read1(min(1 << 20, nbytes - have)) if hasattr(fh, "read1") else fh.read(nbytes)
                if not c:
                    break
                chunks.append(c)
                have += len(c)
        except EOFError:
            pass
    return b"".join(chunks)


def inspect_image(path, nbytes=64_000_000):
    buf = read_head(path, nbytes)
    out = []
    tags = _tiff_first_ifd(buf)
    if tags and "_desc_at" in tags:
        # OME-XML stored past the head: seek there (a gzip seek decompresses up to it)
        off, cnt = tags.pop("_desc_at")
        try:
            with open_maybe_gz(path) as fh:
                fh.seek(off)
                tags["image_description"] = fh.read(min(cnt, 20_000_000)).rstrip(b"\x00").decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            tags["image_description"] = f"(could not read at offset {off}: {type(exc).__name__})"
    if tags:
        desc = tags.pop("image_description", None)
        out.append("TIFF first IFD: " + ", ".join(f"{k}={v}" for k, v in tags.items()))
    else:
        desc = None
        out.append("not a TIFF header in the first bytes")
    text = desc if isinstance(desc, str) and "<OME" in desc else None
    if text is None:
        m = re.search(rb"<OME[\s\S]{0,400000}?</OME>", buf)
        text = m.group(0).decode("utf-8", "replace") if m else None
    if text:
        px = re.search(r"<Pixels\b([^>]*)>", text)
        if px:
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', px.group(1)))
            keep = ["SizeX", "SizeY", "SizeZ", "SizeC", "SizeT", "Type", "DimensionOrder",
                    "PhysicalSizeX", "PhysicalSizeXUnit", "PhysicalSizeY", "PhysicalSizeYUnit"]
            out.append("OME Pixels: " + ", ".join(f"{k}={attrs[k]}" for k in keep if k in attrs))
        chans = re.findall(r'<Channel\b[^>]*Name="([^"]*)"', text)
        if chans:
            out.append("OME channels: " + ", ".join(chans[:12]))
        n_img = len(re.findall(r"<Image\b", text))
        out.append(f"OME images in metadata: {n_img}")
    elif isinstance(desc, str) and desc.strip():
        out.append(f"ImageDescription: {clip(desc, 300)}")
    return out


def inspect_rds(path):
    with open(path, "rb") as fh:
        head = fh.read(16)
    comp = {b"\x1f\x8b": "gzip", b"BZ": "bzip2", b"\xfd7": "xz"}.get(head[:2], "none")
    inner = head
    if comp == "gzip":
        with gzip.open(path, "rb") as fh:
            inner = fh.read(16)
    fmt = {b"X\n": "XDR binary", b"A\n": "ASCII", b"B\n": "native binary"}.get(inner[:2], "unknown")
    return [f"R serialized object (readRDS): compression={comp}, format={fmt}; open with R to see the class"]


def inspect_html(path):
    with open_maybe_gz(path) as fh:
        data = fh.read(3_000_000).decode("utf-8", "replace")
    title = re.search(r"<title>(.*?)</title>", data, re.S)
    out = [f"HTML page, title: {clip(title.group(1).strip(), 120) if title else '(none)'}"]
    if "web_summary" in data or "Cell Ranger" in data or "cellranger" in data:
        out.append("looks like a 10x Cell Ranger web summary")
    return out


def inspect_binary_magic(path):
    with open(path, "rb") as fh:
        head = fh.read(8)
    kinds = {b"\xd0\xcf\x11\xe0": "OLE2 (legacy Excel .xls / Office)", b"%PDF": "PDF",
             b"PK\x03\x04": "zip container", b"\x1f\x8b": "gzip"}
    for k, v in kinds.items():
        if head.startswith(k):
            return [f"binary: {v}"]
    return [f"binary, first bytes {head.hex()}"]


def inspect_file(path, tmpdir):
    name = os.path.basename(path)
    ext = logical_ext(name)
    if os.path.getsize(path) == 0:
        return ["empty file (0 bytes)"]
    if SKIP_CONTENT.match(name):
        return ["download config with signed URLs; content intentionally not shown"]
    if ext in (".parquet", ".parquet.gz"):
        return inspect_parquet(path, tmpdir)
    if ext in (".h5", ".h5ad", ".hdf5", ".loom"):
        return inspect_hdf5(path)
    if ext in (".fastq", ".fastq.gz", ".fq"):
        return inspect_fastq(path)
    if ext in (".tar", ".tar.gz", ".tgz"):
        return inspect_tar(path)
    if ext == ".zip":
        return inspect_zip(path)
    if ext == ".npz":
        return inspect_npz(path)
    if ext in (".pickle", ".pkl"):
        return inspect_pickle(path)
    if ext in (".ome.tif.gz", ".tif.gz", ".tif", ".tiff"):
        return inspect_image(path)
    if ext in (".rds",):
        return inspect_rds(path)
    if ext in (".html", ".html.gz"):
        return inspect_html(path)
    base = name[:-3] if name.lower().endswith(".gz") else name
    if base.lower().endswith(TEXT_EXT) or ext in (".csv.gz", ".tsv.gz", ".txt.gz", ".mtx.gz"):
        return inspect_text(path)
    if ext in (".soft", ".soft.gz"):
        return ["GEO SOFT record; summarised in the GEO metadata section"]
    return inspect_binary_magic(path)


# --------------------------------------------------------------- GEO SOFT
def soft_summary(path):
    opener = gzip.open if path.endswith(".gz") else open
    series, samples, cur = collections.OrderedDict(), [], None
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("^SERIES"):
                cur = series
            elif line.startswith("^SAMPLE"):
                cur = collections.OrderedDict(accession=line.split("=", 1)[1].strip())
                samples.append(cur)
            elif line.startswith("^"):
                cur = None
            elif cur is not None and line.startswith("!") and "=" in line:
                k, v = line[1:].split("=", 1)
                k = re.sub(r"^(Series|Sample)_", "", k.strip())
                cur.setdefault(k, []).append(v.strip())
    return series, samples


def geo_section(geo_dir):
    out = []
    if not os.path.isdir(geo_dir):
        return out
    softs = sorted(f for f in os.listdir(geo_dir) if f.endswith((".soft.gz", ".soft")))
    if not softs:
        return out
    out.append("## GEO series and sample metadata\n")
    out.append("Taken from the GEO SOFT records cached during download. Sample characteristics are "
               "the authors' own fields; they are the basis for linking samples to patients.\n")
    done = set()
    for f in softs:
        acc = f.split("_")[0]
        if acc in done:
            continue
        p = os.path.join(geo_dir, f)
        try:
            series, samples = soft_summary(p)
        except Exception as exc:  # noqa: BLE001
            out.append(f"### {acc}\nunreadable SOFT ({exc})\n")
            continue
        if not series:
            continue
        done.add(acc)
        title = " ".join(series.get("title", []))
        out.append(f"### {acc}: {title}\n")
        for k in ("type", "summary", "overall_design"):
            if k in series:
                out.append(f"- **{k}**: {clip(' '.join(series[k]), 900)}")
        for rel in series.get("relation", [])[:8]:
            out.append(f"- relation: {clip(rel, 200)}")
        out.append("")
        rows = []
        for s in samples:
            supp = sum(len(v) for k, v in s.items() if k.startswith("supplementary_file") and v != ["NONE"])
            rows.append([s["accession"], " ".join(s.get("title", [])), " ".join(s.get("source_name_ch1", [])),
                         "; ".join(s.get("characteristics_ch1", [])), " ".join(s.get("library_strategy", [])),
                         str(supp)])
        if rows:
            out.append(md_table(["GSM", "title", "source", "characteristics", "library", "n supp files"], rows))
            out.append("")
    return out


# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--per-kind", type=int, default=1,
                    help="representatives inspected per (dataset, file kind); smallest first")
    ap.add_argument("--datasets", default=None,
                    help="comma-separated dataset folders to inspect (default: all under --root)")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    tmpdir = tempfile.mkdtemp(prefix="inspect_raw_", dir=os.environ.get("TMPDIR"))
    started = datetime.datetime.now(datetime.timezone.utc)

    datasets = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
    if args.datasets:
        wanted = [d.strip() for d in args.datasets.split(",") if d.strip()]
        missing = [d for d in wanted if d not in datasets]
        if missing:
            print(f"WARNING: not found under {root}: {', '.join(missing)}", file=sys.stderr)
        datasets = [d for d in datasets if d in wanted]
    inventory = []
    for ds in datasets:
        for dp, _dn, fns in os.walk(os.path.join(root, ds)):
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                inventory.append((ds, os.path.relpath(p, root), fn, os.path.getsize(p), kind_of(fn), logical_ext(fn)))

    os.makedirs(os.path.dirname(os.path.abspath(args.inventory)), exist_ok=True)
    with open(args.inventory, "w", encoding="utf-8") as fh:
        fh.write("dataset\trelative_path\tfile_name\tsize_bytes\tkind\tlogical_extension\n")
        for r in inventory:
            fh.write("\t".join(str(x) for x in r) + "\n")

    md = ["# Raw data formats: spatial TCR project\n",
          f"- generated: {started:%Y-%m-%d %H:%M} UTC on `{socket.gethostname()}`",
          f"- root: `{root}`",
          f"- python {platform.python_version()}; libraries: "
          + (", ".join(f"{k} {v}" for k, v in LIBS.items()) or "none"),
          f"- missing optional libraries: {', '.join(x for x in ('pyarrow', 'h5py') if x not in LIBS) or 'none'}",
          "- method: every file is listed; for each dataset and file kind the smallest non-empty file "
          "is opened read-only and summarised. Pickles are scanned, never unpickled.",
          f"- full per-file inventory: `{os.path.relpath(args.inventory, os.path.dirname(os.path.abspath(args.out)))}`\n"]

    by_ds = collections.defaultdict(list)
    for r in inventory:
        by_ds[r[0]].append(r)
    md.append("## Overview\n")
    md.append(md_table(["dataset", "files", "size", "file kinds"],
                       [[ds, f"{len(rs):,}", human(sum(r[3] for r in rs)), str(len({r[4] for r in rs}))]
                        for ds, rs in by_ds.items()]))
    md.append("")

    warnings = []
    for ds in datasets:
        rs = by_ds.get(ds, [])
        if not rs or ds == "geo_meta":
            continue
        md.append(f"## {ds}\n")
        kinds = collections.OrderedDict()
        for r in sorted(rs, key=lambda r: (r[4], r[3])):
            kinds.setdefault(r[4], []).append(r)
        md.append(md_table(["kind", "n files", "total size", "example"],
                           [[k, str(len(v)), human(sum(x[3] for x in v)), v[0][2]] for k, v in kinds.items()]))
        md.append("")
        zero = [r[1] for r in rs if r[3] == 0]
        if zero:
            warnings.append(f"{ds}: zero-byte files: " + ", ".join(zero))
        for k, v in kinds.items():
            reps = [x for x in v if x[3] > 0][: args.per_kind] or v[:1]
            for rep in reps:
                md.append(f"### `{k}` ({len(v)} file{'s' if len(v) != 1 else ''})\n")
                md.append(f"inspected: `{rep[1]}` ({human(rep[3])})\n")
                t0 = datetime.datetime.now()
                try:
                    lines = inspect_file(os.path.join(root, rep[1]), tmpdir)
                except Exception as exc:  # noqa: BLE001
                    lines = [f"ERROR while inspecting: {type(exc).__name__}: {exc}"]
                    warnings.append(f"{rep[1]}: {type(exc).__name__}: {exc}")
                md.extend(lines)
                secs = (datetime.datetime.now() - t0).total_seconds()
                md.append("")
                print(f"[{secs:6.1f}s] {rep[1]}", flush=True)

    md.extend(geo_section(os.path.join(root, "geo_meta")))
    md.append("## Warnings\n")
    md.extend(f"- {w}" for w in warnings) if warnings else md.append("- none")
    md.append("")

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"wrote {args.out} ({len(inventory):,} files inventoried) and {args.inventory}")


if __name__ == "__main__":
    main()
