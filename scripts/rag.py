#!/usr/bin/env python3
"""
rag.py — Conector RAG genérico para Scrum-AI Delivery (solo biblioteca estándar).

Tres tipos de fuente, registradas con `sai.py cap add-rag`:
  local : indexa una carpeta (md, txt, json, csv, html, código, y PDF si existe `pdftotext`)
          con BM25 y responde consultas con fragmentos citables (archivo + línea).
  http  : envía la consulta a una API RAG externa (POST JSON) y normaliza la respuesta.
  mcp   : el RAG está expuesto como herramienta MCP; este script solo indica qué herramienta usar.

Uso:
  python rag.py index <rag_id>
  python rag.py query <rag_id> "¿qué reglas aplican a convocatorias cerradas?" [-k 5]
  python rag.py query-all "pregunta" --phase Define     # consulta todas las fuentes aprobadas de una fase

Contrato HTTP (configurable): POST {endpoint} con {"query": str, "top_k": int}
Se aceptan respuestas con lista en: results | documents | matches | data | hits,
y por elemento los campos text|content|chunk|page_content, source|url|metadata.source, score.
El token, si aplica, se lee de la variable de entorno indicada en --auth-env (nunca se guarda).
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from pathlib import Path

TEXT_EXT = {".md", ".txt", ".rst", ".json", ".csv", ".html", ".htm", ".py", ".js", ".ts", ".tsx",
            ".jsx", ".java", ".cs", ".go", ".sql", ".yml", ".yaml", ".xml", ".bpmn", ".mmd", ".mermaid"}
CHUNK_LINES = 40
OVERLAP = 8
STOP = set("""a al algo ante con contra de del desde el ella ellos en entre era es esta este esto ha hay la las lo los mas más
me mi muy no nos o para pero por que qué se ser si sí sin sobre su sus también te tu un una uno unos y ya
the of and to in is for on with as by be are this that it or an from at""".split())


def find_root():
    p = Path.cwd().resolve()
    for c in [p, *p.parents]:
        if (c / "scrum-ai" / "capabilities.json").exists():
            return c
    sys.exit("✖ No se encontró scrum-ai/capabilities.json (ejecute sai.py init).")


def get_rag(root, rid):
    caps = json.loads((root / "scrum-ai" / "capabilities.json").read_text(encoding="utf-8"))
    for r in caps.get("rag", []):
        if r["id"] == rid:
            return r, caps
    sys.exit(f"✖ RAG '{rid}' no registrado. Use: python sai.py cap add-rag --id {rid} ...")


def tokenize(t):
    t = t.lower()
    t = re.sub(r"[áàä]", "a", t); t = re.sub(r"[éèë]", "e", t); t = re.sub(r"[íìï]", "i", t)
    t = re.sub(r"[óòö]", "o", t); t = re.sub(r"[úùü]", "u", t)
    return [w for w in re.findall(r"[a-zñ0-9_]{2,}", t) if w not in STOP]


def read_file(f):
    if f.suffix.lower() == ".pdf":
        try:
            r = subprocess.run(["pdftotext", "-layout", str(f), "-"], capture_output=True, text=True, timeout=120)
            return r.stdout
        except Exception:
            return ""
    try:
        return f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def cmd_index(a):
    root = find_root()
    r, _ = get_rag(root, a.id)
    if r["tipo"] != "local":
        sys.exit("✖ Solo las fuentes 'local' se indexan. Las 'http'/'mcp' se consultan directamente.")
    base = (root / r["ruta"]).resolve() if not os.path.isabs(r["ruta"]) else Path(r["ruta"])
    if not base.exists():
        sys.exit(f"✖ No existe {base}")
    chunks = []
    files = [f for f in base.rglob("*") if f.is_file() and (f.suffix.lower() in TEXT_EXT or f.suffix.lower() == ".pdf")
             and ".git" not in f.parts and "node_modules" not in f.parts and f.stat().st_size < 5_000_000]
    for f in files:
        lines = read_file(f).splitlines()
        step = CHUNK_LINES - OVERLAP
        for i in range(0, max(len(lines), 1), step):
            seg = "\n".join(lines[i:i + CHUNK_LINES]).strip()
            if len(seg) < 30:
                continue
            chunks.append({"src": str(f.relative_to(base)), "linea": i + 1, "texto": seg, "tf": Counter(tokenize(seg))})
    df = Counter()
    for c in chunks:
        df.update(set(c["tf"]))
    avgdl = sum(sum(c["tf"].values()) for c in chunks) / max(len(chunks), 1)
    idx = {"base": str(base), "n": len(chunks), "avgdl": avgdl, "df": df,
           "chunks": [{**c, "tf": dict(c["tf"])} for c in chunks]}
    out = root / "scrum-ai" / "rag" / f"{a.id}.index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    print(f"✔ Indexados {len(files)} archivos → {len(chunks)} fragmentos en {out.relative_to(root)}")


def bm25(idx, q, k=5, k1=1.5, b=0.75):
    qt = tokenize(q)
    N, avgdl, df = idx["n"], idx["avgdl"] or 1, idx["df"]
    scored = []
    for c in idx["chunks"]:
        dl = sum(c["tf"].values()) or 1
        s = 0.0
        for t in qt:
            f = c["tf"].get(t, 0)
            if not f:
                continue
            idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / avgdl))
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return [{"score": round(s, 3), "fuente": c["src"], "linea": c["linea"], "texto": c["texto"]} for s, c in scored[:k]]


def query_http(r, q, k):
    body = json.dumps({"query": q, "top_k": k}).encode()
    req = urllib.request.Request(r["endpoint"], data=body, headers={"Content-Type": "application/json"})
    if r.get("auth_env"):
        tok = os.environ.get(r["auth_env"])
        if not tok:
            sys.exit(f"✖ Defina la variable de entorno {r['auth_env']} con el token del RAG.")
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    items = data if isinstance(data, list) else next(
        (data[key] for key in ("results", "documents", "matches", "data", "hits") if isinstance(data.get(key), list)), [])
    out = []
    for it in items[:k]:
        if isinstance(it, str):
            out.append({"score": None, "fuente": r["endpoint"], "texto": it}); continue
        md = it.get("metadata") or {}
        out.append({"score": it.get("score"),
                    "fuente": it.get("source") or it.get("url") or md.get("source") or r["endpoint"],
                    "texto": it.get("text") or it.get("content") or it.get("chunk") or it.get("page_content") or json.dumps(it)[:800]})
    return out


def run_query(root, r, q, k):
    if r.get("estado") not in ("aprobado", "activo"):
        print(f"⚠ La fuente '{r['id']}' está en estado '{r.get('estado')}'. Úsela solo con autorización humana.", file=sys.stderr)
    if r["tipo"] == "local":
        f = root / "scrum-ai" / "rag" / f"{r['id']}.index.json"
        if not f.exists():
            sys.exit(f"✖ Falta el índice. Ejecute: python rag.py index {r['id']}")
        return bm25(json.loads(f.read_text(encoding="utf-8")), q, k)
    if r["tipo"] == "http":
        return query_http(r, q, k)
    return [{"score": None, "fuente": f"mcp:{r['mcp']}",
             "texto": f"Esta fuente RAG se consulta con la herramienta de búsqueda del servidor MCP '{r['mcp']}'. "
                      "Invoque esa herramienta directamente con la pregunta."}]


def show(rid, res):
    print(f"\n=== {rid} ===")
    if not res:
        print("(sin resultados)")
    for i, x in enumerate(res, 1):
        loc = f"{x['fuente']}" + (f":{x['linea']}" if x.get("linea") else "")
        print(f"\n[{i}] {loc}  score={x['score']}")
        print(x["texto"][:1200])


def cmd_query(a):
    root = find_root()
    r, _ = get_rag(root, a.id)
    res = run_query(root, r, a.q, a.k)
    print(json.dumps(res, ensure_ascii=False, indent=2)) if a.json else show(a.id, res)


def cmd_query_all(a):
    root = find_root()
    caps = json.loads((root / "scrum-ai" / "capabilities.json").read_text(encoding="utf-8"))
    for r in caps.get("rag", []):
        if r.get("estado") in ("aprobado", "activo") and (not a.phase or a.phase in r["fases"] or "*" in r["fases"]):
            try:
                show(r["id"], run_query(root, r, a.q, a.k))
            except SystemExit as e:
                print(f"\n=== {r['id']} === {e}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("index"); x.add_argument("id"); x.set_defaults(fn=cmd_index)
    x = sp.add_parser("query"); x.add_argument("id"); x.add_argument("q"); x.add_argument("-k", type=int, default=5)
    x.add_argument("--json", action="store_true"); x.set_defaults(fn=cmd_query)
    x = sp.add_parser("query-all"); x.add_argument("q"); x.add_argument("--phase"); x.add_argument("-k", type=int, default=3)
    x.set_defaults(fn=cmd_query_all)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
