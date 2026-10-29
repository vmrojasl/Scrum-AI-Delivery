#!/usr/bin/env python3
"""Instala diseno-web-integral y las skills que coordina, para Claude Code, Codex o ambos.

Uso:
  python instalar.py --zips "<carpeta con los .zip>" --destino ambos
  python instalar.py --zips "<carpeta>" --destino codex --forzar --omitir impeccable

Zips esperados en --zips (los del proyecto "02 Skills - Diseno UI-UX"):
  impeccable-main.zip, taste-skill-main.zip, ui-ux-pro-max-skill-main.zip, skills-main.zip
Si falta alguno, se omiten sus skills y se avisa.

Destinos:
  claude -> ~/.claude/skills  (+ subagentes de impeccable en ~/.claude/agents)
  codex  -> ~/.agents/skills  (cámbialo con --dir-codex, p. ej. ~/.codex/skills)

Por defecto no sobrescribe skills ya instaladas; usa --forzar para reemplazarlas.
"""
import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ESTA_SKILL = Path(__file__).resolve().parent.parent  # carpeta diseno-web-integral

UI_UX_PRO_MAX = ["ui-ux-pro-max", "design-system", "brand", "ui-styling", "design", "banner-design", "slides"]


def raiz_del_zip(extraido: Path) -> Path:
    """Los zips de GitHub traen una sola carpeta '<repo>-main/' dentro."""
    hijos = [p for p in extraido.iterdir() if p.is_dir()]
    return hijos[0] if len(hijos) == 1 else extraido


def plan(repos: dict, destino: str) -> list:
    """Devuelve [(origen, nombre_destino, tipo)] donde tipo es 'skill' o 'agente'."""
    items = [(ESTA_SKILL, "diseno-web-integral", "skill")]

    imp = repos.get("impeccable-main")
    if imp:
        if destino == "claude":
            items.append((imp / ".claude/skills/impeccable", "impeccable", "skill"))
            agentes = imp / ".claude/agents"
            if agentes.is_dir():
                items += [(a, a.name, "agente") for a in sorted(agentes.glob("*.md"))]
        else:  # Codex trae sus subagentes .toml dentro de la propia skill
            items.append((imp / ".agents/skills/impeccable", "impeccable", "skill"))

    taste = repos.get("taste-skill-main")
    if taste:
        items.append((taste / "skills/taste-skill", "design-taste-frontend", "skill"))

    uupm = repos.get("ui-ux-pro-max-skill-main")
    if uupm:
        items += [(uupm / ".claude/skills" / n, n, "skill") for n in UI_UX_PRO_MAX]

    emil = repos.get("skills-main")
    if emil:
        items += [(d, d.name, "skill") for d in sorted((emil / "skills").iterdir()) if (d / "SKILL.md").is_file()]

    return items


def copiar(origen: Path, destino: Path, forzar: bool) -> str:
    if not origen.exists():
        return "falta en el zip"
    respaldo = None
    if destino.exists():
        if not forzar:
            return "ya existe (omitida)"
        # Apartar antes de borrar: si un archivo está en uso, el renombrado falla y la versión
        # instalada queda intacta en vez de quedar a medio borrar.
        respaldo = destino.with_name(destino.name + ".reemplazo-tmp")
        try:
            destino.rename(respaldo)
        except OSError:
            return "en uso por otro programa, no se tocó (cierra Codex/Claude y reintenta)"
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        if origen.is_dir():
            shutil.copytree(origen, destino, ignore=shutil.ignore_patterns("__pycache__", "*-workspace"))
        else:
            shutil.copy2(origen, destino)
    except OSError as e:
        if respaldo:
            shutil.rmtree(destino, ignore_errors=True)
            respaldo.rename(destino)
        return f"error al copiar, se dejó la versión anterior ({e})"
    if respaldo:
        shutil.rmtree(respaldo, ignore_errors=True) if respaldo.is_dir() else respaldo.unlink()
    return "reemplazada" if respaldo else "instalada"


CLAVES_SOLO_CLAUDE = ("argument-hint:", "disable-model-invocation:", "user-invocable:")


def adaptar_a_codex(skill: Path) -> str:
    """Codex solo acepta name, description, license, allowed-tools y metadata en el frontmatter.
    Quita las claves propias de Claude y traduce disable-model-invocation a la política de Codex."""
    archivo = skill / "SKILL.md"
    lineas = archivo.read_text(encoding="utf-8").split("\n")
    if not lineas or lineas[0].strip() != "---":
        return ""
    fin = next((i for i in range(1, len(lineas)) if lineas[i].strip() == "---"), None)
    if fin is None:
        return ""
    quitadas = [l for l in lineas[1:fin] if l.startswith(CLAVES_SOLO_CLAUDE)]
    if not quitadas:
        return ""
    archivo.write_text("\n".join([l for l in lineas[:fin] if l not in quitadas] + lineas[fin:]), encoding="utf-8")
    nota = "frontmatter adaptado"
    if any(l.startswith("disable-model-invocation:") and "true" in l for l in quitadas):
        yaml = skill / "agents" / "openai.yaml"
        if not yaml.exists():
            yaml.parent.mkdir(exist_ok=True)
            yaml.write_text("policy:\n  allow_implicit_invocation: false\n", encoding="utf-8")
        nota += ", solo invocación explícita ($nombre)"
    return f" ({nota})"


def instalar(destino: str, repos: dict, dir_skills: Path, dir_agentes: Path, forzar: bool, omitir: set) -> None:
    print(f"\n== {destino.upper()} -> {dir_skills}")
    for origen, nombre, tipo in plan(repos, destino):
        if nombre in omitir or (tipo == "agente" and "impeccable" in omitir):
            print(f"  {nombre:32} omitida a pedido")
            continue
        base = dir_agentes if tipo == "agente" else dir_skills
        if tipo == "skill" and origen.resolve() == (base / nombre).resolve():
            print(f"  {nombre:32} ya está aquí")
            continue
        estado = copiar(origen, base / nombre, forzar)
        if estado in ("instalada", "reemplazada") and destino == "codex" and tipo == "skill":
            estado += adaptar_a_codex(base / nombre)
        print(f"  {nombre:32} {estado}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos legibles en la consola de Windows
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zips", required=True, type=Path, help="carpeta con los .zip de los repos")
    ap.add_argument("--destino", choices=["claude", "codex", "ambos"], default="ambos")
    ap.add_argument("--dir-claude", type=Path, default=Path.home() / ".claude")
    ap.add_argument("--dir-codex", type=Path, default=Path.home() / ".agents" / "skills")
    ap.add_argument("--forzar", action="store_true", help="reemplaza skills ya instaladas")
    ap.add_argument("--omitir", default="", help="skills a no tocar, separadas por coma (p. ej. impeccable)")
    args = ap.parse_args()
    omitir = {s.strip() for s in args.omitir.split(",") if s.strip()}

    if not args.zips.is_dir():
        print(f"No existe la carpeta {args.zips}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="dwi-") as tmp:
        repos = {}
        for nombre in ["impeccable-main", "taste-skill-main", "ui-ux-pro-max-skill-main", "skills-main"]:
            z = args.zips / f"{nombre}.zip"
            if not z.is_file():
                print(f"Aviso: no encontré {z.name}; sus skills no se instalarán.")
                continue
            d = Path(tmp) / nombre
            with zipfile.ZipFile(z) as zf:
                zf.extractall(d)
            repos[nombre] = raiz_del_zip(d)

        if args.destino in ("claude", "ambos"):
            instalar("claude", repos, args.dir_claude / "skills", args.dir_claude / "agents", args.forzar, omitir)
        if args.destino in ("codex", "ambos"):
            instalar("codex", repos, args.dir_codex, args.dir_codex, args.forzar, omitir)

    print("\nListo. Abre una sesión nueva de Claude Code o Codex para que carguen las skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
