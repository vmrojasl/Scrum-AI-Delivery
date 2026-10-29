#!/usr/bin/env python3
"""
sai.py — CLI de la metodología Scrum-AI Delivery.

Mantiene el estado del proyecto en ./scrum-ai/ (versionable en Git) y hace
cumplir las reglas de la metodología: gates G1–G6 con aprobación humana,
DoR/DoD, scorecard ponderado (≥85/100, ninguna dimensión <3/5, controles
críticos binarios) y registro de capacidades externas (skills, MCP, RAG).

Solo usa la biblioteca estándar de Python 3.8+.

Uso rápido:
  python sai.py init --name "Ecosistema de Investigación" --mode existente
  python sai.py status
  python sai.py story add US-CONV-001 "Consultar convocatorias"
  python sai.py story move US-CONV-001 especificacion
  python sai.py gate US-CONV-001 G1 --decision aprobado --approver "Ana (PO)" --evidence scrum-ai/backlog/US-CONV-001.md
  python sai.py score US-CONV-001 --func 4 --tec 4 --ux 4 --pruebas 5 --seg 4 --doc 4
  python sai.py cap detect
  python sai.py cap approve --pack agent-skills --by "Ana (Líder técnico)"
  python sai.py cap for-phase Build
Ejecute `python sai.py -h` o `python sai.py <comando> -h` para ver todo.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIRNAME = "scrum-ai"
SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"

# --------------------------------------------------------------------------
# Modelo de la metodología
# --------------------------------------------------------------------------
ROADMAP = {
    "S0": "Descubrimiento y estrategia",
    "S1": "Planificación",
    "S2": "Diseño",
    "S3": "Desarrollo",
    "S4": "Pruebas y validación",
    "S5": "Despliegue",
    "S6": "Operación y mejora continua",
}

# Fases del ciclo de desarrollo donde actúan los Agent Skills
PHASES = ["Define", "Plan", "Design", "Build", "Verify", "Review", "Ship"]

# Estados de una historia (ciclo de sprint de 11 pasos)
STATUSES = [
    "backlog",        # 01 Selección del backlog
    "especificacion", # 02 Especificación      -> sale con G1
    "flujo",          # 03 Flujo BPMN/Mermaid  -> sale con G2
    "mockup",         # 04 Mockup              -> sale con G3
    "plan_tecnico",   # 05 Plan técnico        -> sale con DoR
    "ready",          #    Ready
    "desarrollo",     # 06 Desarrollo IA
    "pruebas",        # 07 Pruebas             -> sale con G4
    "uat",            # 08 UAT                 -> sale con G5
    "aceptacion",     # 09 Aceptación PO       -> sale con DoD + scorecard
    "release",        # 10 Release             -> sale con G6
    "done",           # 11 (Retrospectiva a nivel de sprint)
]

STATUS_PHASE = {
    "backlog": "Plan", "especificacion": "Define", "flujo": "Design",
    "mockup": "Design", "plan_tecnico": "Design", "ready": "Plan",
    "desarrollo": "Build", "pruebas": "Verify", "uat": "Verify",
    "aceptacion": "Review", "release": "Ship", "done": "Ship",
}

# Requisito para SALIR de cada estado hacia el siguiente
EXIT_REQUIREMENT = {
    "especificacion": "G1",
    "flujo": "G2",
    "mockup": "G3",
    "plan_tecnico": "DoR",
    "pruebas": "G4",
    "uat": "G5",
    "aceptacion": "DoD+SCORE",
    "release": "G6",
}

GATES = {
    "G1": {"nombre": "Requisitos", "aprueban": ["Product Owner", "Dueño de proceso"],
           "verifica": ["Historia de usuario completa", "Reglas de negocio", "Criterios de aceptación", "Dependencias y alcance"],
           "evidencia": ["Historia en el backlog", "Criterios de aceptación", "Trazabilidad de requisitos"]},
    "G2": {"nombre": "Flujo", "aprueban": ["Dueño de proceso", "Arquitecto de procesos"],
           "verifica": ["Flujo de proceso", "Actores y permisos", "Escenarios principales y excepciones", "Coherencia con requisitos"],
           "evidencia": ["Diagrama BPMN / Mermaid", "Descripción de escenarios", "Validación del proceso"]},
    "G3": {"nombre": "Diseño", "aprueban": ["UX/UI", "Product Owner", "Dueño de proceso"],
           "verifica": ["Mockup de alta fidelidad", "Estados (carga, vacío, error)", "Diseño responsive", "Accesibilidad y consistencia"],
           "evidencia": ["Mockups aprobados", "Prototipo navegable", "Guía de estilos (si aplica)"]},
    "G4": {"nombre": "Desarrollo", "aprueban": ["Líder técnico", "QA / Seguridad"],
           "verifica": ["Implementación completa", "Pruebas automatizadas", "Revisión de código (PR)", "Cumplimiento de estándares", "Seguridad (SAST/DAST)"],
           "evidencia": ["Pull Request y revisión", "Resultados de pruebas", "Informe de análisis de seguridad", "Evidencia de buenas prácticas"]},
    "G5": {"nombre": "Funcional", "aprueban": ["Usuarios clave", "Product Owner"],
           "verifica": ["Funcionalidad según criterios", "Pruebas con usuarios clave", "Datos y escenarios reales", "Corrección de hallazgos", "Evidencia de aceptación"],
           "evidencia": ["Plan y resultados de UAT", "Registro de hallazgos", "Evidencia de aceptación", "Checklist de criterios"]},
    "G6": {"nombre": "Entrega", "aprueban": ["Product Owner", "Operaciones / TI"],
           "verifica": ["Despliegue en producción", "Configuración de monitoreo", "Observabilidad y alertas", "Plan de rollback", "Documentación operativa"],
           "evidencia": ["Release en producción", "Monitoreo y alertas activos", "Plan de rollback probado", "Documentación de despliegue"]},
}

DOR = ["historia_definida", "reglas_de_negocio", "criterios_de_aceptacion", "flujo_aprobado",
       "mockup_validado", "dependencias_identificadas", "tamano_estimado"]
DOD = ["aceptacion_completa", "pr_revisado", "pruebas_ok", "seguridad_validada",
       "responsive_verificado", "uat_completado", "documentacion_al_dia"]

SCORECARD = [  # clave, nombre, peso
    ("func", "Funcionalidad", 30),
    ("tec", "Calidad técnica", 20),
    ("ux", "Diseño / UX", 15),
    ("pruebas", "Pruebas", 15),
    ("seg", "Seguridad", 15),
    ("doc", "Documentación", 5),
]
SCORE_THRESHOLD = 85
MIN_DIMENSION = 3

# Nombres que nunca pueden figurar como aprobadores: los agentes ejecutan, no aprueban.
AI_APPROVER_PATTERN = re.compile(r"\b(claude|codex|openai|agente|agent|ia|ai|bot|gpt|copilot|llm|asistente)\b", re.I)

# Revisión cruzada (solo en Claude Code): Codex revisa lo que produjo Claude antes de pedir la decisión humana.
# Estado de la historia → punto de revisión. Codex revisa; no aprueba.
XREVIEW_AT = {"especificacion": "G1", "plan_tecnico": "DoR", "pruebas": "G4", "release": "G6"}
XREVIEW_PROMPTS = {
    "G1": ("Revisa la especificación de la historia {id} en scrum-ai/backlog/{id}.md. Señala ambigüedades, reglas de "
           "negocio faltantes o contradictorias, criterios de aceptación que no se puedan probar, casos de borde sin "
           "cubrir (sin resultados, error del servidor, uso móvil, permisos) y dependencias omitidas."),
    "DoR": ("Revisa el plan técnico de la historia {id}: scrum-ai/backlog/{id}.md, scrum-ai/design/{id}/ y los ADR de "
            "scrum-ai/adr/. Contrástalo con los criterios de aceptación y el mockup aprobado. Señala supuestos riesgosos, "
            "contratos de API incompletos, riesgos de datos y seguridad, tareas faltantes y estimaciones poco realistas."),
    "G6": ("Revisa la preparación del release de la historia {id}: plan de rollback, monitoreo y alertas, migraciones, "
           "configuración por ambiente y documentación de despliegue (scrum-ai/evidence/{id}/, CONSTRAINTS.md, "
           ".github/workflows/). Señala lo que podría fallar en producción y lo que no se puede revertir."),
}
XREVIEW_RULES = ("Es una revisión de solo lectura: no modifiques archivos. Responde en español con hallazgos "
                 "concretos (archivo y sección), severidad (alta/media/baja) y una recomendación por hallazgo. "
                 "Si no encuentras problemas, dilo explícitamente.")


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def find_root(start=None):
    p = Path(start or os.getcwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / ROOT_DIRNAME / "state.json").exists():
            return cand
    return None


def require_root():
    root = find_root()
    if not root:
        die("No se encontró ./scrum-ai/state.json. Ejecute primero: python sai.py init --name \"...\"")
    return root


def die(msg, code=1):
    print(f"✖ {msg}", file=sys.stderr)
    sys.exit(code)


def ok(msg):
    print(f"✔ {msg}")


def load(root, name):
    f = root / ROOT_DIRNAME / name
    return json.loads(f.read_text(encoding="utf-8"))


def save(root, name, data):
    f = root / ROOT_DIRNAME / name
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def log_event(state, kind, **data):
    state.setdefault("log", []).append({"fecha": now(), "evento": kind, **data})


def copy_template(src_rel, dst: Path, replacements=None, overwrite=False):
    src = ASSETS / src_rel
    if dst.exists() and not overwrite:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    for k, v in (replacements or {}).items():
        text = text.replace("{{" + k + "}}", v)
    dst.write_text(text, encoding="utf-8")
    return True


def validate_approvers(approvers):
    if not approvers:
        die("Se requiere al menos un --approver humano (nombre y rol).")
    for a in approvers:
        if AI_APPROVER_PATTERN.search(a):
            die(f"'{a}' parece un agente de IA. Principio clave: los agentes ejecutan, NO aprueban. "
                "Registre el nombre y rol de la persona que aprobó.")


# --------------------------------------------------------------------------
# init
# --------------------------------------------------------------------------
def cmd_init(a):
    root = Path(a.path).resolve()
    sai = root / ROOT_DIRNAME
    if (sai / "state.json").exists() and not a.force:
        die(f"Ya existe {sai/'state.json'}. Use --force para reinicializar.")
    for d in ["backlog", "evidence", "sprints", "audit", "adr", "vision", "rag", "vendor-skills", "design"]:
        (sai / d).mkdir(parents=True, exist_ok=True)
    state = {
        "metodologia": "Scrum-AI Delivery",
        "proyecto": {"nombre": a.name, "modo": a.mode, "creado": now()},
        "fase": "S0",
        "fase_historial": [{"fase": "S0", "inicio": now()}],
        "sprint": {"numero": 0, "objetivo": "Sprint 0: alinear visión, personas, tecnología y proceso",
                   "duracion_semanas": 2, "inicio": None, "fin": None},
        "sprint0": {k: False for k in [
            "vision_mvp", "inventario_funcional", "matriz_roles", "diagnostico_tecnico", "adr",
            "dor_dod", "estructura_repositorio", "agents_md", "constraints_md", "pipeline_ci_cd",
            "sprint1_refinado"]},
        "historias": {},
        "decisiones": [],
        "roles": {},
        "log": [],
        "verificacion": {"nivel": a.verify or PROFILES[a.profile]["verificacion"]},
        "pruebas": _test_place(a.tests_in, a.tests_path) if a.tests_in else None,
    }
    _apply_profile_flags(state, a)
    if a.verify:
        state["verificacion"] = {"nivel": a.verify}
    if a.approver:
        validate_approvers([a.approver])
        state["aprobador"] = a.approver
    if a.mode == "nuevo":
        state["sprint0"].pop("diagnostico_tecnico")
        state["sprint0"]["diagnostico_tecnico"] = "no_aplica"
    _apply_sprint0_profile(state)
    log_event(state, "init", modo=a.mode)
    save(root, "state.json", state)

    caps = json.loads((ASSETS / "capabilities.default.json").read_text(encoding="utf-8"))
    if not (sai / "capabilities.json").exists() or a.force:
        print("Paquetes de skills (agent-skills, ecc, diseno-web-integral y, en Claude Code, codex):")
        _detect(root, caps)
        save(root, "capabilities.json", caps)

    repl = {"PROYECTO": a.name, "FECHA": dt.date.today().isoformat()}
    created = []
    for src, dst in [
        ("templates/AGENTS.md", root / "AGENTS.md"),
        ("templates/CONSTRAINTS.md", root / "CONSTRAINTS.md"),
        ("templates/vision.md", sai / "vision" / "vision.md"),
        ("templates/roles-raci.md", sai / "vision" / "roles-raci.md"),
        ("templates/dor-dod.md", sai / "dor-dod.md"),
    ]:
        if copy_template(src, dst, repl):
            created.append(str(dst.relative_to(root)))
    if a.mode == "existente":
        if copy_template("templates/auditoria-sprint0.md", sai / "audit" / "auditoria.md", repl):
            created.append(f"{ROOT_DIRNAME}/audit/auditoria.md")
    if a.github:
        for src, dst in [
            ("github/ISSUE_TEMPLATE/historia.md", root / ".github/ISSUE_TEMPLATE/historia.md"),
            ("github/PULL_REQUEST_TEMPLATE.md", root / ".github/PULL_REQUEST_TEMPLATE.md"),
            ("github/workflows/quality-gates.yml", root / ".github/workflows/quality-gates.yml"),
        ]:
            if copy_template(src, dst, repl):
                created.append(str(dst.relative_to(root)))
    ok(f"Proyecto '{a.name}' inicializado en {sai} (modo: {a.mode}, fase S0, "
       f"verificación {_verify_level(state)}).")
    print(f"Perfil: {_describe_profile(state)}")
    for c in created:
        print(f"   + {c}")
    if not a.tests_in:
        print("⚠ Falta definir dónde se hacen las pruebas: python sai.py config --tests-in sandbox|rama|proyecto")
    print("Siguiente: python sai.py status")


# --------------------------------------------------------------------------
# config: nivel de verificación y lugar de las pruebas
# --------------------------------------------------------------------------
VERIFY_LEVELS = {
    "ligero": "pruebas manuales: el agente escribe las pruebas y los comandos, la persona los ejecuta y "
              "pega el resultado; revisión cruzada y skills complementarios de Verify solo a pedido",
    "completo": "el agente ejecuta pruebas, verification-loop y revisión cruzada de Codex en G1, DoR, G4 y G6",
}
TEST_PLACES = {
    "sandbox": "carpeta o proyecto de pruebas aparte; el proyecto real no se toca para probar",
    "rama": "rama de git dedicada a pruebas; nada se fusiona sin el gate correspondiente",
    "proyecto": "en el propio proyecto, solo dentro del alcance de la historia",
}


# Perfil del proyecto: cuánto de la metodología y de los skills externos se ejecuta, según la complejidad.
# Lo no negociable no depende del perfil: G1, G4, G6, DoR, DoD, scorecard y aprobación humana.
PROFILES = {
    "esencial": {"skills": "ninguno", "omitir": ["flujo", "uat"], "diseno": "basico", "detalle": "breve",
                 "verificacion": "ligero"},
    "estandar": {"skills": "principal", "omitir": [], "diseno": "basico", "detalle": "breve",
                 "verificacion": "ligero"},
    "completo": {"skills": "todos", "omitir": [], "diseno": "integral", "detalle": "completo",
                 "verificacion": "completo"},
}
PROFILE_HELP = {
    "esencial": "prototipo, herramienta interna o proyecto personal: sin skills externos, sin flujo BPMN ni UAT",
    "estandar": "proyecto típico: solo skills principales, mockup básico, artefactos breves",
    "completo": "proyecto institucional, crítico o con datos sensibles: toda la metodología y todos los skills",
}
SKILL_LEVELS = ["ninguno", "principal", "todos"]
# Etapas que se pueden omitir → gate que desaparece e ítem de DoR/DoD que queda "no_aplica"
OPTIONAL_STAGES = {"flujo": ("G2", "dor", "flujo_aprobado"), "mockup": ("G3", "dor", "mockup_validado"),
                   "uat": ("G5", "dod", "uat_completado")}
DESIGN_PACK = "diseno-web-integral"
VERIFY_ON_DEMAND = {"ecc-verification-loop"}  # principal en Verify, pero con verificación ligera solo a pedido


def _parse_skip(value):
    if value is None:
        return None
    if value.strip().lower() in ("", "ninguno", "ninguna", "none"):
        return []
    stages = [x.strip() for x in value.split(",") if x.strip()]
    bad = [x for x in stages if x not in OPTIONAL_STAGES]
    if bad:
        die(f"Etapa no omitible: {', '.join(bad)}. Solo se pueden omitir: {', '.join(OPTIONAL_STAGES)} "
            "(G1, G4, G6, DoR, DoD y scorecard son obligatorios).")
    return stages


def _profile(state):
    """Perfil efectivo; los proyectos creados antes de esta opción usan 'estandar'."""
    p = {k: v for k, v in PROFILES["estandar"].items() if k != "verificacion"}
    p["nombre"] = "estandar"
    p.update(state.get("perfil") or {})
    return p


def _apply_profile_flags(state, a):
    """--profile reinicia todo a ese perfil; los flags individuales lo ajustan después."""
    changed = False
    if getattr(a, "profile", None):
        base = PROFILES[a.profile]
        state["perfil"] = {"nombre": a.profile, **{k: (list(v) if isinstance(v, list) else v)
                                                   for k, v in base.items() if k != "verificacion"}}
        if not getattr(a, "verify", None):
            state["verificacion"] = {"nivel": base["verificacion"], "cambiado": now()}
        changed = True
    p = _profile(state)
    for key, val in (("skills", getattr(a, "skills", None)), ("omitir", _parse_skip(getattr(a, "skip_stages", None))),
                     ("diseno", getattr(a, "design", None)), ("detalle", getattr(a, "detail", None))):
        if val is not None:
            p[key] = val
            if not p["nombre"].endswith("(ajustado)"):
                p["nombre"] += " (ajustado)"
            changed = True
    if changed:
        state["perfil"] = p
    return changed


def _describe_profile(state):
    p = _profile(state)
    return (f"{p['nombre']} · skills {p['skills']} · omite {', '.join(p['omitir']) or 'nada'} · "
            f"diseño {p['diseno']} · detalle {p['detalle']}")


# Sprint 0 mínimo del perfil esencial; el resto de entregables queda "no_aplica".
SPRINT0_ESENCIAL = {"vision_mvp", "diagnostico_tecnico", "dor_dod", "agents_md", "constraints_md", "sprint1_refinado"}


def _apply_sprint0_profile(state):
    esencial = _profile(state)["nombre"].startswith("esencial")
    for k, v in state["sprint0"].items():
        if k == "diagnostico_tecnico" and state["proyecto"]["modo"] == "nuevo":
            continue
        if esencial and k not in SPRINT0_ESENCIAL and v is False:
            state["sprint0"][k] = "no_aplica"
        elif not esencial and v == "no_aplica":
            state["sprint0"][k] = False


def _set_story_skip(s, stages):
    """Aplica las etapas omitidas a una historia: sus ítems de DoR/DoD pasan a 'no_aplica' (o vuelven a pendiente)."""
    for st, (_, kind, item) in OPTIONAL_STAGES.items():
        if st in stages:
            s[kind][item] = "no_aplica"
        elif s[kind].get(item) == "no_aplica":
            s[kind][item] = False
    s["omitir"] = list(stages)


def _next_status(s, cur):
    for st in STATUSES[STATUSES.index(cur) + 1:]:
        if st not in s.get("omitir", []):
            return st
    return None


def _test_place(where, path):
    if where == "sandbox" and not path:
        die("Con --tests-in sandbox indique la carpeta con --tests-path <ruta>.")
    if where == "rama" and not path:
        path = "pruebas/<ID>"
    return {"donde": where, "ruta": path, "definido": now()}


def _verify_level(state):
    return state.get("verificacion", {}).get("nivel", "ligero")


def _describe_tests(p):
    if not p:
        return "sin definir (pregunte al usuario antes de probar)"
    return p["donde"] + (f" → {p['ruta']}" if p.get("ruta") else "") + f" ({TEST_PLACES[p['donde']]})"


def cmd_config(a):
    root = require_root()
    state = load(root, "state.json")
    changed = _apply_profile_flags(state, a)
    if changed:
        log_event(state, "config", perfil=state["perfil"])
    if a.verify:
        state["verificacion"] = {"nivel": a.verify, "cambiado": now()}
        log_event(state, "config", verificacion=a.verify)
    if a.tests_in:
        state["pruebas"] = _test_place(a.tests_in, a.tests_path)
        log_event(state, "config", pruebas=state["pruebas"])
    elif a.tests_path:
        die("Indique también --tests-in sandbox|rama|proyecto.")
    if changed and state["fase"] == "S0":
        _apply_sprint0_profile(state)
    if a.approver:
        if a.approver.lower() == "ninguno":
            state.pop("aprobador", None)
        else:
            validate_approvers([a.approver])
            state["aprobador"] = a.approver
        log_event(state, "config", aprobador=state.get("aprobador"))
    if changed or a.verify or a.tests_in or a.approver:
        save(root, "state.json", state)
        ok("Configuración actualizada.")
        if changed:
            print("  (las etapas omitidas aplican a historias nuevas; para una existente: python sai.py story skip <ID> --skip ...)")
    nivel = _verify_level(state)
    print(f"Perfil: {_describe_profile(state)}")
    print(f"Verificación: {nivel} — {VERIFY_LEVELS[nivel]}")
    print(f"Pruebas: {_describe_tests(state.get('pruebas'))}")
    print(f"Aprobador en el chat: {state.get('aprobador') or 'sin definir (se pide nombre y rol en cada gate)'}")


# --------------------------------------------------------------------------
# status / next
# --------------------------------------------------------------------------
def _xreview_on(root):
    """La revisión cruzada automática aplica en Claude Code, con el paquete codex aprobado y verificación completa.
    En verificación ligera se ejecuta solo si el usuario la pide (xreview sigue disponible)."""
    if _harness() != "claude":
        return False
    try:
        if _verify_level(load(root, "state.json")) != "completo":
            return False
        caps = load(root, "capabilities.json")
    except (OSError, ValueError):
        return False
    return any(c["id"] == "codex-revision-cruzada" and c.get("estado") == "aprobado" for c in caps.get("skills", []))


def next_action_for_story(sid, s, xreview=False):
    base = _next_action(sid, s)
    point = XREVIEW_AT.get(s["estado"])
    if xreview and point and point not in s.get("revisiones_cruzadas", {}) \
            and s["gates"].get(point, {}).get("estado") != "aprobado":
        return f"Revisión cruzada pendiente: python sai.py xreview {sid} --point {point}. Luego: {base}"
    return base


def _next_action(sid, s):
    st = s["estado"]
    req = EXIT_REQUIREMENT.get(st)
    nxt = _next_status(s, st) if st != "done" else None
    if st == "backlog":
        return "Seleccionar para el sprint y pasar a 'especificacion' (ficha de historia)."
    if st == "done":
        return "Cerrada con evidencia."
    if req and req.startswith("G"):
        g = s["gates"].get(req, {})
        if g.get("estado") == "aprobado":
            return f"{req} aprobado → mover a '{nxt}'."
        if g.get("estado") == "rechazado":
            return f"{req} rechazado → ajustar y volver a presentar evidencia."
        return f"Producir evidencia de {req} ({GATES[req]['nombre']}) y pedir aprobación a: {', '.join(GATES[req]['aprueban'])}."
    if req == "DoR":
        faltan = [k for k in DOR if not s["dor"].get(k)]
        return "DoR completo → mover a 'ready'." if not faltan else f"Completar DoR: {', '.join(faltan)}."
    if req == "DoD+SCORE":
        faltan = [k for k in DOD if not s["dod"].get(k)]
        sc = s.get("score")
        parts = []
        if faltan:
            parts.append("DoD pendiente: " + ", ".join(faltan))
        if not sc:
            parts.append("calcular scorecard (python sai.py score ...)")
        elif not sc["aprobado"]:
            parts.append(f"scorecard {sc['total']}/100 NO aprobado → corregir")
        return "; ".join(parts) + "." if parts else "Aceptación lista → mover a 'release'."
    return f"Trabajo en curso → mover a '{nxt}' al terminar."


def cmd_status(a):
    root = require_root()
    state = load(root, "state.json")
    caps = load(root, "capabilities.json")
    p = state["proyecto"]
    xr = _xreview_on(root)
    print(f"Proyecto: {p['nombre']}  (modo {p['modo']})")
    print(f"Entorno: {'Claude Code' if _harness() == 'claude' else 'Codex'}"
          + (" · revisión cruzada con Codex activa" if xr else ""))
    print(f"Perfil: {_describe_profile(state)}")
    print(f"Verificación: {_verify_level(state)} · Pruebas: {_describe_tests(state.get('pruebas'))}"
          f" · Aprobador en el chat: {state.get('aprobador') or 'sin definir'}")
    if not state.get("pruebas"):
        print("  ⚠ Pregunte dónde se harán las pruebas y regístrelo: python sai.py config --tests-in sandbox|rama|proyecto")
    print(f"Fase del roadmap: {state['fase']} — {ROADMAP[state['fase']]}")
    sp = state["sprint"]
    print(f"Sprint actual: {sp['numero']} — {sp.get('objetivo') or '(sin objetivo)'}")
    if sp["numero"] == 0:
        pend = [k for k, v in state["sprint0"].items() if v is False]
        print(f"Entregables Sprint 0 pendientes ({len(pend)}): {', '.join(pend) or 'ninguno'}")
    hs = state["historias"]
    if hs:
        print("\nHistorias:")
        for sid, s in hs.items():
            print(f"  {sid:<16} [{s['estado']:<14}] {s['titulo']}")
            print(f"  {'':<16} → {next_action_for_story(sid, s, xr)}")
    else:
        print("\nSin historias registradas aún.")
    pending = [c for kind in ("skills", "mcp", "rag") for c in caps.get(kind, []) if c.get("estado") == "pendiente_revision"]
    if pending:
        packs = {}
        for c in pending:
            packs.setdefault(c.get("paquete") or c["id"], []).append(c)
        resumen = ", ".join(f"{p} ({len(v)})" if len(v) > 1 else p for p, v in packs.items())
        print(f"\nCapacidades pendientes de revisión humana: {resumen}")
    if not caps.get("paquetes"):
        print("\nEl registro de capacidades es de una versión anterior. Actualícelo con: python sai.py cap sync")


def cmd_phase(a):
    root = require_root()
    state = load(root, "state.json")
    if a.set:
        a.approver = a.approver or state.get("aprobador")
        if not a.approver:
            die('Indique --approver "Nombre (rol)" de quien autoriza el cambio de fase.')
        validate_approvers([a.approver])
        if a.set not in ROADMAP:
            die(f"Fase inválida. Opciones: {', '.join(ROADMAP)}")
        cur = state["fase"]
        if list(ROADMAP).index(a.set) > list(ROADMAP).index(cur) + 1 and not a.force:
            die(f"No se puede saltar de {cur} a {a.set} sin --force (las fases son secuenciales).")
        if a.set != "S0" and cur == "S0" and state["sprint"]["numero"] == 0:
            pend = [k for k, v in state["sprint0"].items() if v is False]
            if pend and not a.force:
                die(f"Sprint 0 incompleto ({', '.join(pend)}). Complete o use --force con justificación.")
        state["fase_historial"][-1]["fin"] = now()
        state["fase_historial"].append({"fase": a.set, "inicio": now(), "aprobado_por": a.approver})
        state["fase"] = a.set
        log_event(state, "fase", fase=a.set, aprobado_por=a.approver)
        save(root, "state.json", state)
        ok(f"Fase → {a.set} ({ROADMAP[a.set]})")
    else:
        for k, v in ROADMAP.items():
            mark = "▶" if k == state["fase"] else " "
            print(f" {mark} {k} {v}")


def cmd_sprint0(a):
    root = require_root()
    state = load(root, "state.json")
    if a.item:
        if a.item not in state["sprint0"]:
            die(f"Entregable desconocido. Opciones: {', '.join(state['sprint0'])}")
        state["sprint0"][a.item] = True if not a.undo else False
        log_event(state, "sprint0", item=a.item, valor=state["sprint0"][a.item], evidencia=a.evidence)
        save(root, "state.json", state)
        ok(f"{a.item} = {state['sprint0'][a.item]}")
    for k, v in state["sprint0"].items():
        print(f"  [{'x' if v is True else ('-' if v == 'no_aplica' else ' ')}] {k}")


def cmd_sprint(a):
    root = require_root()
    state = load(root, "state.json")
    if a.action == "start":
        n = state["sprint"]["numero"] + 1
        start = dt.date.today()
        end = start + dt.timedelta(weeks=state["sprint"].get("duracion_semanas", 2))
        state.setdefault("sprints_previos", []).append(state["sprint"])
        state["sprint"] = {"numero": n, "objetivo": a.goal or "", "duracion_semanas": 2,
                           "inicio": start.isoformat(), "fin": end.isoformat()}
        d = root / ROOT_DIRNAME / "sprints" / f"sprint-{n}"
        copy_template("templates/sprint-plan.md", d / "plan.md",
                      {"PROYECTO": state["proyecto"]["nombre"], "N": str(n), "OBJETIVO": a.goal or "",
                       "INICIO": start.isoformat(), "FIN": end.isoformat(), "FECHA": start.isoformat()})
        copy_template("templates/retrospectiva.md", d / "retro.md", {"N": str(n), "FECHA": end.isoformat()})
        log_event(state, "sprint_start", numero=n, objetivo=a.goal)
        save(root, "state.json", state)
        ok(f"Sprint {n} iniciado ({start} → {end}). Plan: {ROOT_DIRNAME}/sprints/sprint-{n}/plan.md")
    elif a.action == "close":
        n = state["sprint"]["numero"]
        hs = state["historias"]
        en = [s for s in hs.values() if s.get("sprint") == n]
        done = [s for s in en if s["estado"] == "done"]
        pred = round(100 * len(done) / len(en)) if en else 0
        state["sprint"]["cerrado"] = now()
        state["sprint"]["predictibilidad"] = pred
        log_event(state, "sprint_close", numero=n, planificadas=len(en), completadas=len(done))
        save(root, "state.json", state)
        ok(f"Sprint {n} cerrado. Predictibilidad {pred}% (meta ≥85%). Complete la retrospectiva: "
           f"{ROOT_DIRNAME}/sprints/sprint-{n}/retro.md")


# --------------------------------------------------------------------------
# historias
# --------------------------------------------------------------------------
def cmd_story(a):
    root = require_root()
    state = load(root, "state.json")
    hs = state["historias"]
    if a.action == "add":
        if a.id in hs:
            die(f"{a.id} ya existe.")
        hs[a.id] = {"titulo": a.title, "estado": "backlog", "sprint": None, "epica": a.epic,
                    "gates": {}, "dor": {k: False for k in DOR}, "dod": {k: False for k in DOD},
                    "score": None, "creada": now(), "historial": [{"estado": "backlog", "fecha": now()}]}
        skip = _parse_skip(a.skip)
        _set_story_skip(hs[a.id], _profile(state)["omitir"] if skip is None else skip)
        ficha = root / ROOT_DIRNAME / "backlog" / f"{a.id}.md"
        if copy_template("templates/historia-usuario.md", ficha,
                         {"ID": a.id, "TITULO": a.title, "EPICA": a.epic or "", "FECHA": dt.date.today().isoformat()}):
            _remember_template(root, hs[a.id], ficha)
        log_event(state, "story_add", id=a.id)
        save(root, "state.json", state)
        ok(f"{a.id} creada en backlog → {ROOT_DIRNAME}/backlog/{a.id}.md")
        if hs[a.id]["omitir"]:
            print(f"   Etapas omitidas: {', '.join(hs[a.id]['omitir'])}")
    elif a.action == "skip":
        s = hs.get(a.id) or die(f"{a.id} no existe.")
        stages = _parse_skip(a.skip)
        if stages is None:
            die("Indique --skip flujo,mockup,uat (o --skip ninguno para no omitir ninguna).")
        # Las etapas en curso o ya superadas conservan lo que tenían; el cambio aplica a las que faltan.
        ci = STATUSES.index(s["estado"])
        kept = [st for st in OPTIONAL_STAGES if STATUSES.index(st) <= ci]
        ignored = [st for st in kept if (st in stages) != (st in s.get("omitir", []))]
        if ignored:
            print(f"   (sin cambio en etapas en curso o superadas: {', '.join(ignored)})")
        stages = [st for st in stages if st not in kept] + [st for st in kept if st in s.get("omitir", [])]
        _set_story_skip(s, stages)
        log_event(state, "story_skip", id=a.id, omitir=stages, motivo=a.reason)
        save(root, "state.json", state)
        ok(f"{a.id}: etapas omitidas → {', '.join(stages) or 'ninguna'}")
        print("Siguiente:", next_action_for_story(a.id, s, _xreview_on(root)))
    elif a.action == "list":
        for sid, s in hs.items():
            print(f"{sid:<16} {s['estado']:<14} sprint={s['sprint']}  {s['titulo']}")
    elif a.action == "show":
        s = hs.get(a.id) or die(f"{a.id} no existe.")
        print(json.dumps({a.id: s}, ensure_ascii=False, indent=2))
        print("Siguiente:", next_action_for_story(a.id, s, _xreview_on(root)))
    elif a.action == "move":
        s = hs.get(a.id) or die(f"{a.id} no existe.")
        target = a.to
        if target not in STATUSES:
            die(f"Estado inválido. Opciones: {', '.join(STATUSES)}")
        cur = s["estado"]
        ci, ti = STATUSES.index(cur), STATUSES.index(target)
        nxt = _next_status(s, cur)
        if target in s.get("omitir", []):
            die(f"'{target}' está omitida para {a.id}" + (f"; avance a '{nxt}'." if ti > ci else "."))
        if ti > ci and target != nxt:
            die(f"No se puede saltar de '{cur}' a '{target}'. Avance un estado a la vez (siguiente: '{nxt}').")
        if ti > ci:
            block = _exit_block(s, cur)
            if block:
                die(block)
        elif ti < ci and not a.reason:
            die("Retroceder requiere --reason (ej. 'Mockup no aprobado: ajustar diseño').")
        _do_move(root, state, a.id, s, target, a.reason)
        save(root, "state.json", state)
        print("Siguiente:", next_action_for_story(a.id, s, _xreview_on(root)))


def _exit_block(s, cur):
    """Motivo por el que la historia no puede salir de 'cur', o None si puede."""
    req = EXIT_REQUIREMENT.get(cur)
    if req and req.startswith("G") and s["gates"].get(req, {}).get("estado") != "aprobado":
        return f"Bloqueado: salir de '{cur}' requiere {req} ({GATES[req]['nombre']}) aprobado por humanos."
    if req == "DoR":
        faltan = [k for k in DOR if not s["dor"].get(k)]
        if faltan:
            return f"Bloqueado por Definition of Ready. Falta: {', '.join(faltan)}"
    if req == "DoD+SCORE":
        faltan = [k for k in DOD if not s["dod"].get(k)]
        if faltan:
            return f"Bloqueado por Definition of Done. Falta: {', '.join(faltan)}"
        if not s.get("score") or not s["score"]["aprobado"]:
            return "Bloqueado: el scorecard debe estar aprobado (≥85/100, ninguna dimensión <3, sin controles críticos)."
    return None


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _remember_template(root, s, path):
    """Guarda la huella de la plantilla recién copiada: una plantilla sin editar no sirve de evidencia."""
    s.setdefault("plantillas", {})[path.relative_to(root).as_posix()] = _sha(path)


def _is_untouched_template(root, s, rel):
    h = s.get("plantillas", {}).get(rel)
    return bool(h) and (root / rel).exists() and _sha(root / rel) == h


def _do_move(root, state, sid, s, target, reason=None):
    cur = s["estado"]
    if cur == "backlog":
        s["sprint"] = state["sprint"]["numero"]
    s["estado"] = target
    s["historial"].append({"estado": target, "fecha": now(), "motivo": reason})
    tpl = {"flujo": ("templates/flujo.md", "flujo.md"), "mockup": ("templates/diseno-ui.md", "diseno-ui.md")}.get(target)
    if tpl:
        dst = root / ROOT_DIRNAME / "design" / sid / tpl[1]
        if copy_template(tpl[0], dst, {"ID": sid, "TITULO": s["titulo"]}):
            _remember_template(root, s, dst)
            print(f"   + {dst.relative_to(root)}")
    log_event(state, "story_move", id=sid, de=cur, a=target, motivo=reason)
    ok(f"{sid}: {cur} → {target}  (fase {STATUS_PHASE[target]})")


def _auto_advance(root, state, sid, s):
    """Avanza mientras el requisito de salida del estado actual ya se cumple (gate aprobado, DoR o DoD+score).
    Ahorra un comando y una vuelta por cada aprobación; nunca salta un control."""
    while s["estado"] != "done" and EXIT_REQUIREMENT.get(s["estado"]) and not _exit_block(s, s["estado"]):
        _do_move(root, state, sid, s, _next_status(s, s["estado"]), "avance automático")


def cmd_check(a, kind):
    root = require_root()
    state = load(root, "state.json")
    s = state["historias"].get(a.id) or die(f"{a.id} no existe.")
    keys = DOR if kind == "dor" else DOD
    for item in a.items or []:
        if item not in keys:
            die(f"Ítem inválido '{item}'. Opciones: {', '.join(keys)}")
        s[kind][item] = not a.undo
    if a.items:
        log_event(state, kind, id=a.id, items=a.items, valor=not a.undo)
    print(f"{kind.upper()} de {a.id}:")
    for k in keys:
        mark = "n/a" if s[kind][k] == "no_aplica" else ("x" if s[kind][k] else " ")
        print(f"  [{mark}] {k}")
    if a.items:
        if not a.no_advance:
            _auto_advance(root, state, a.id, s)
        save(root, "state.json", state)
        print("Siguiente:", next_action_for_story(a.id, s, _xreview_on(root)))


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------
GATE_DEFAULT_EVIDENCE = {  # artefacto que el gate revisa; se usa si no se pasa --evidence
    "G1": "{d}/backlog/{id}.md", "G2": "{d}/design/{id}/flujo.md", "G3": "{d}/design/{id}/diseno-ui.md",
}


def cmd_gate(a):
    root = require_root()
    state = load(root, "state.json")
    gates = [x.strip().upper() for x in a.gate.split(",") if x.strip()]
    bad = [x for x in gates if x not in GATES]
    if bad:
        die(f"Gate inválido: {', '.join(bad)}. Opciones: {', '.join(GATES)}")
    if a.info or not a.id:
        for gid in gates:
            g = GATES[gid]
            print(f"{gid} — {g['nombre']}")
            print("  Qué se verifica: " + "; ".join(g["verifica"]))
            print("  Quién aprueba:   " + " + ".join(g["aprueban"]))
            print("  Evidencia:       " + "; ".join(g["evidencia"]))
        return
    if not a.decision:
        die("Indique --decision aprobado|rechazado. Recuerde: solo después de que el/los aprobador(es) humano(s) lo confirmen.")
    approvers = a.approver or ([state["aprobador"]] if state.get("aprobador") else [])
    validate_approvers(approvers)
    if len(gates) > 1 and a.no_advance:
        die("Varios gates en una decisión requieren el avance automático (quite --no-advance).")
    ids = [x.strip() for x in a.id.split(",") if x.strip()]
    errors = []
    for sid in ids:  # aprobación agrupada: misma decisión, mismos aprobadores, un acta por historia y gate
        s = state["historias"].get(sid)
        if not s:
            errors.append(f"{sid} no existe.")
            continue
        for gid in gates:
            stage = [k for k, v in EXIT_REQUIREMENT.items() if v == gid][0]
            if len(gates) > 1 and stage in s.get("omitir", []):
                print(f"   ({gid} no aplica a {sid}: etapa '{stage}' omitida)")
                continue
            err = _record_gate(root, state, sid, s, gid, a.decision, approvers, a.evidence, a.notes, a.force)
            if err:
                errors.append(f"{sid} {gid}: {err}")
                break
            if a.decision == "rechazado":
                break
            if not a.no_advance:
                _auto_advance(root, state, sid, s)
        print("Siguiente:", next_action_for_story(sid, s, _xreview_on(root)))
    save(root, "state.json", state)
    if errors:
        die("No registrado: " + " | ".join(errors))


def _record_gate(root, state, sid, s, gid, decision, approvers, evidence, notes, force):
    """Registra un gate de una historia. Devuelve un mensaje de error o None."""
    g = GATES[gid]
    expected_status = [k for k, v in EXIT_REQUIREMENT.items() if v == gid][0]
    if expected_status in s.get("omitir", []):
        return f"no aplica: la etapa '{expected_status}' está omitida."
    if s["estado"] != expected_status and not force:
        return f"se decide cuando la historia está en '{expected_status}' (actual: '{s['estado']}')."
    evidence = list(evidence or [])
    if not evidence and gid in GATE_DEFAULT_EVIDENCE:
        default = GATE_DEFAULT_EVIDENCE[gid].format(d=ROOT_DIRNAME, id=sid)
        if (root / default).exists():
            evidence = [default]
    missing = [e for e in evidence if not (root / e).exists() and not re.match(r"^https?://", e)]
    if missing:
        return f"evidencia no encontrada: {', '.join(missing)} (use rutas relativas al repo o URLs)."
    blank = [e for e in evidence if _is_untouched_template(root, s, e.replace("\\", "/"))]
    if decision == "aprobado" and blank:
        return f"{', '.join(blank)} sigue siendo la plantilla sin completar; complétela antes de aprobar."
    if decision == "aprobado" and not evidence:
        return "un gate no se aprueba sin evidencia. Pase al menos un --evidence."
    if decision == "aprobado" and gid == "G4":
        sc = s.get("score")
        if sc and sc.get("bloqueado"):
            return "G4 no puede aprobarse: hay un control crítico fallido en el scorecard."
    s["gates"][gid] = {"estado": decision, "aprobado_por": approvers, "evidencia": evidence,
                       "observaciones": notes, "fecha": now()}
    ev_dir = root / ROOT_DIRNAME / "evidence" / sid
    ev_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"# {gid} — {g['nombre']} · {sid}", "",
             f"- Decisión: **{decision}**", f"- Fecha: {now()}",
             f"- Aprobador(es): {', '.join(approvers)}", "", "## Qué se verificó"]
    lines += [f"- {v}" for v in g["verifica"]]
    lines += ["", "## Evidencia"] + [f"- {e}" for e in (evidence or ["(ninguna)"])]
    xr = s.get("revisiones_cruzadas", {}).get(gid)
    if xr:
        lines += ["", "## Revisión cruzada (Codex — revisa, no aprueba)", f"- {xr['archivo']} ({xr['fecha']})"]
    elif gid in XREVIEW_AT.values() and _xreview_on(root):
        print(f"⚠ {gid} se registra sin revisión cruzada de Codex (python sai.py xreview {sid} --point {gid}).")
        lines += ["", "## Revisión cruzada (Codex)", "- No se ejecutó."]
    if notes:
        lines += ["", "## Observaciones", notes]
    (ev_dir / f"{gid}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Actualizaciones automáticas de DoR/DoD derivadas de gates
    if decision == "aprobado":
        if gid == "G1":
            s["dor"].update(historia_definida=True, reglas_de_negocio=True, criterios_de_aceptacion=True)
        elif gid == "G2":
            s["dor"]["flujo_aprobado"] = True
        elif gid == "G3":
            s["dor"]["mockup_validado"] = True
        elif gid == "G4":
            s["dod"].update(pr_revisado=True, pruebas_ok=True, seguridad_validada=True)
        elif gid == "G5":
            s["dod"]["uat_completado"] = True
    log_event(state, "gate", id=sid, gate=gid, decision=decision, aprobado_por=approvers)
    ok(f"{gid} {decision} para {sid}. Acta: {ROOT_DIRNAME}/evidence/{sid}/{gid}.md")
    return None


def cmd_xreview(a):
    """Revisión cruzada: Codex revisa lo que produjo Claude antes de pedir la decisión humana."""
    root = require_root()
    if _harness() != "claude":
        ok("La revisión cruzada con Codex solo aplica cuando el skill corre en Claude Code. En Codex no aplica.")
        return
    state = load(root, "state.json")
    s = state["historias"].get(a.id) or die(f"{a.id} no existe.")
    if a.point not in XREVIEW_AT.values():
        die(f"Punto inválido. Opciones: {', '.join(XREVIEW_AT.values())}")
    caps = load(root, "capabilities.json")
    c = next((x for x in caps.get("skills", []) if x["id"] == "codex-revision-cruzada"), None)
    if not c:
        die("El registro no tiene el paquete codex. Ejecute: python sai.py cap sync")
    if not c.get("ruta_local"):
        die("El plugin de Codex no está instalado. Vea el plan con: python sai.py cap install --pack codex")
    if c.get("estado") != "aprobado":
        die('El paquete codex no está aprobado: python sai.py cap approve --pack codex --by "Nombre (rol)"')
    script = Path(c["ruta_local"]) / c["script"]
    if not script.exists():
        die("No se encuentra el script del plugin (¿se actualizó?). Ejecute: python sai.py cap detect")
    if not shutil.which("codex"):
        die("Falta el CLI de Codex: npm install -g @openai/codex  y luego  codex login")
    if a.point == "G4":
        args = ["review", "--wait"] + (["--base", a.base] if a.base else [])
        what = "codex review (código, revisión nativa)"
    else:
        prompt = XREVIEW_PROMPTS[a.point].format(id=a.id) + " " + XREVIEW_RULES
        if a.focus:
            prompt += " Foco adicional: " + a.focus
        args = ["task", "--fresh", prompt]
        what = "codex task (solo lectura)"
    print(f"Revisión cruzada {a.point} de {a.id} con {what}. Puede tardar varios minutos…")
    rc, out = _run(["node", str(script)] + args, cwd=str(root))
    ev = root / ROOT_DIRNAME / "evidence" / a.id
    ev.mkdir(parents=True, exist_ok=True)
    f = ev / f"codex-{a.point}.md"
    f.write_text("\n".join([f"# Revisión cruzada {a.point} — {a.id}", "",
                            f"- Fecha: {now()}", f"- Revisor: Codex ({what})", f"- Resultado del comando: {rc}",
                            "- Codex revisa, no aprueba: la decisión del gate es humana.", "",
                            "## Salida de Codex (sin editar)", "", out, ""]), encoding="utf-8")
    rel = f.relative_to(root).as_posix()
    if rc != 0:
        print(out)
        die(f"Codex terminó con error ({rc}). Salida guardada en {rel}. Si pide sesión: codex login")
    s.setdefault("revisiones_cruzadas", {})[a.point] = {"fecha": now(), "archivo": rel}
    log_event(state, "xreview", id=a.id, punto=a.point, archivo=rel)
    save(root, "state.json", state)
    print(out)
    ok(f"Revisión cruzada guardada en {rel}. Atienda o justifique cada hallazgo antes de pedir la aprobación.")


# --------------------------------------------------------------------------
# scorecard
# --------------------------------------------------------------------------
def compute_score(ratings, critical):
    rows, total = [], 0.0
    for key, name, w in SCORECARD:
        r = ratings[key]
        if not 1 <= r <= 5:
            die(f"{name}: la calificación debe estar entre 1 y 5.")
        pts = w * r / 5
        total += pts
        rows.append({"criterio": name, "peso": w, "calificacion": r, "puntaje": round(pts, 1)})
    total = round(total, 1)
    low = [r["criterio"] for r in rows if r["calificacion"] < MIN_DIMENSION]
    blocked = [k for k, v in critical.items() if v]
    approved = total >= SCORE_THRESHOLD and not low and not blocked
    return {"filas": rows, "total": total, "dimensiones_bajas": low, "controles_criticos_fallidos": blocked,
            "bloqueado": bool(blocked), "aprobado": approved}


def cmd_score(a):
    ratings = {k: getattr(a, k) for k, _, _ in SCORECARD}
    critical = {"vulnerabilidad_critica": a.critical_vuln, "prueba_obligatoria_fallida": a.failed_test,
                "criterio_obligatorio_incumplido": a.mandatory_missing}
    res = compute_score(ratings, critical)
    print(f"{'Criterio':<18}{'Peso':>6}{'Calif.':>8}{'Puntaje':>9}")
    for r in res["filas"]:
        print(f"{r['criterio']:<18}{r['peso']:>5}%{r['calificacion']:>6}/5{r['puntaje']:>9}")
    print(f"{'TOTAL':<18}{'':>6}{'':>8}{res['total']:>9}/100")
    if res["controles_criticos_fallidos"]:
        print("⛔ Controles críticos fallidos (bloqueo automático): " + ", ".join(res["controles_criticos_fallidos"]))
    if res["dimensiones_bajas"]:
        print("⚠ Dimensiones < 3/5: " + ", ".join(res["dimensiones_bajas"]))
    if res["total"] < SCORE_THRESHOLD:
        print(f"⚠ No alcanza el umbral mínimo de {SCORE_THRESHOLD}/100.")
    print("ESTADO:", "APROBADA" if res["aprobado"] else "NO APROBADA")
    if a.id:
        root = require_root()
        state = load(root, "state.json")
        s = state["historias"].get(a.id) or die(f"{a.id} no existe.")
        res["fecha"] = now()
        res["evaluado_por"] = a.evaluator
        s["score"] = res
        log_event(state, "score", id=a.id, total=res["total"], aprobado=res["aprobado"])
        ev = root / ROOT_DIRNAME / "evidence" / a.id
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "scorecard.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        ok(f"Scorecard guardado en {ROOT_DIRNAME}/evidence/{a.id}/scorecard.json")
        if not a.no_advance:
            _auto_advance(root, state, a.id, s)
        save(root, "state.json", state)
        print("Siguiente:", next_action_for_story(a.id, s, _xreview_on(root)))


# --------------------------------------------------------------------------
# decisiones (ADR) y auditoría
# --------------------------------------------------------------------------
def cmd_adr(a):
    root = require_root()
    state = load(root, "state.json")
    d = root / ROOT_DIRNAME / "adr"
    n = len(list(d.glob("ADR-*.md"))) + 1
    slug = re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")[:50]
    f = d / f"ADR-{n:03d}-{slug}.md"
    copy_template("templates/adr.md", f, {"N": f"{n:03d}", "TITULO": a.title, "FECHA": dt.date.today().isoformat()})
    state["decisiones"].append({"id": f"ADR-{n:03d}", "titulo": a.title, "archivo": str(f.relative_to(root)), "fecha": now()})
    save(root, "state.json", state)
    ok(f"ADR creado: {f.relative_to(root)}")


def cmd_audit(a):
    """Registra la evaluación de un componente en la auditoría de Sprint 0."""
    root = require_root()
    state = load(root, "state.json")
    aud = state.setdefault("auditoria", {})
    if a.component:
        vals = dict(estado=a.state, valor_negocio=a.value)
        # Matriz de decisión: valor de negocio vs estado técnico
        good = a.state >= 3
        high = a.value >= 3
        sugerida = ("Conservar" if good and high else "Refactorizar" if (not good) and high
                    else "Retirar" if good and not high else "Reconstruir")
        # Matriz del documento (valor de negocio × estado técnico). La sugerencia orienta;
        # la acción final la decide el equipo (--action).
        vals["accion_sugerida"] = sugerida
        vals["accion"] = a.action or sugerida
        vals["notas"] = a.notes
        aud[a.component] = vals
        save(root, "state.json", state)
        ok(f"{a.component}: estado {a.state}/5, valor {a.value}/5 → sugerida {sugerida}, decidida {vals['accion']}")
    if aud:
        tot = len(aud)
        from collections import Counter
        c = Counter(v["accion"] for v in aud.values())
        print(f"{'Componente':<20}{'Estado':>7}{'Valor':>7}  Acción")
        for k, v in aud.items():
            print(f"{k:<20}{v['estado']:>7}{v['valor_negocio']:>7}  {v['accion']}")
        print("Distribución: " + ", ".join(f"{k} {round(100*n/tot)}%" for k, n in c.items()))


# --------------------------------------------------------------------------
# capacidades externas: skills de terceros, MCP, RAG
# --------------------------------------------------------------------------
def _caps(root):
    return load(root, "capabilities.json")


def _find_cap(caps, cid):
    for kind in ("skills", "mcp", "rag"):
        for c in caps.get(kind, []):
            if c["id"] == cid:
                return kind, c
    return None, None


def _check_phases(phases):
    for p in phases:
        if p not in PHASES and p != "*":
            die(f"Fase '{p}' inválida. Opciones: {', '.join(PHASES)} o '*'")


def _claude_home():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def _codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def _harness():
    """Entorno que ejecuta el skill: 'claude' (Claude Code) o 'codex'. SAI_HARNESS o --harness lo fijan."""
    h = os.environ.get("SAI_HARNESS", "").lower()
    if h in ("claude", "codex"):
        return h
    if os.environ.get("CLAUDECODE"):
        return "claude"
    if any(os.environ.get(k) for k in ("CODEX_SANDBOX", "CODEX_THREAD_ID", "CODEX_CI", "CODEX_MANAGED_BY_NPM")):
        return "codex"
    return "claude"


def _skills_target():
    """Carpeta de usuario donde se instalan skills para el entorno actual."""
    return _claude_home() / "skills" if _harness() == "claude" else Path.home() / ".agents" / "skills"


def _skill_bases(root):
    if _harness() == "claude":
        return [root / ".claude" / "skills", _claude_home() / "skills"]
    return [root / ".agents" / "skills", Path.home() / ".agents" / "skills", _codex_home() / "skills"]


def _applies(item):
    return item.get("solo_harness") in (None, _harness())


def _plugin_install_paths():
    # {"agent-skills@addy-agent-skills": Path(...)} según ~/.claude/plugins/installed_plugins.json
    f = _claude_home() / "plugins" / "installed_plugins.json"
    out = {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    for key, installs in data.get("plugins", {}).items():
        for inst in installs or []:
            if inst.get("installPath"):
                out[key] = Path(inst["installPath"])
    return out


def _native_skill_dir(root, c, pack, plugins):
    """(carpeta, nombre de invocación) donde el entorno tiene instalado el skill, o (None, None)."""
    name = c.get("nombre") or c["id"]
    cands = []
    if _harness() == "claude" and pack and pack.get("plugin") in plugins:
        cands.append((plugins[pack["plugin"]] / "skills" / name, f"{pack['plugin'].split('@')[0]}:{name}"))
    for base in _skill_bases(root):
        cands.append((base / name, name if _harness() == "claude" else f"${name}"))
    for d, invocation in cands:
        if (d / "SKILL.md").exists():
            return d, invocation
    return None, None


def _detect(root, caps, quiet=False):
    """Marca como detectados los skills instalados en el entorno actual. No aprueba nada: eso es humano."""
    plugins = _plugin_install_paths()
    packs = caps.get("paquetes", {})
    found, missing = [], []
    for c in caps.get("skills", []):
        if c.get("invocacion") not in ("nativa", "script") or not _applies(c):
            continue
        pack = packs.get(c.get("paquete")) or {}
        if c["invocacion"] == "script":  # plugin que se usa por su script (revisión cruzada con Codex)
            base = plugins.get(pack.get("plugin"))
            d = base if base and (base / c["script"]).exists() else None
            invocation = f"node {base / c['script']}" if d else None
            c["cli_listo"] = bool(shutil.which(pack.get("instalacion", {}).get("cli", {}).get("comando", "")))
        else:
            d, invocation = _native_skill_dir(root, c, pack, plugins)
        if d:
            c["ruta_local"] = str(d)
            c["skill"] = invocation
            c["instalado"] = True
            if c.get("estado") == "por_configurar":
                c["estado"] = "pendiente_revision"
            found.append(c)
        else:
            c["instalado"] = False
            missing.append(c)
    if not quiet:
        print(f"  (entorno: {'Claude Code' if _harness() == 'claude' else 'Codex'})")
        by_pack = {}
        for c in found + missing:
            by_pack.setdefault(c.get("paquete") or "-", [0, 0])[0 if c in found else 1] += 1
        for p, (f, m) in by_pack.items():
            print(f"  {p:<22} instalados {f}  ·  faltan {m}")
            if m and packs.get(p, {}).get("instalar"):
                print(f"  {'':<22} instale con: {packs[p]['instalar']}")
        for c in found:
            if c.get("invocacion") == "script" and not c.get("cli_listo"):
                cli = packs[c["paquete"]]["instalacion"]["cli"]
                print(f"  {c['paquete']:<22} falta el CLI '{cli['comando']}': {' '.join(cli['instalar'])} y luego {cli['login']}")
    return found, missing


def _find_claude_cli():
    """Ejecutable de Claude Code: PATH, o el que traen las extensiones de VS Code / Cursor / Windsurf."""
    p = os.environ.get("CLAUDE_CODE_EXECPATH") or shutil.which("claude")
    if p and Path(p).is_file():
        return p
    home = Path.home()
    cands = []
    for ide in (".vscode", ".vscode-insiders", ".cursor", ".windsurf"):
        cands += (home / ide / "extensions").glob("anthropic.claude-code-*/resources/native-binary/claude*")
    cands += [home / ".local" / "bin" / "claude", home / ".claude" / "local" / "claude"]
    cands = [c for c in cands if c.is_file() and c.suffix in ("", ".exe")]
    return str(max(cands, key=lambda c: c.stat().st_mtime)) if cands else None


def _run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    return r.returncode, (r.stdout + r.stderr).strip()


CLAUDE_ONLY_KEYS = ("argument-hint:", "disable-model-invocation:", "user-invocable:")


def _adapt_for_codex(skill_dir):
    """Codex solo acepta name, description, license, allowed-tools y metadata en el frontmatter."""
    f = skill_dir / "SKILL.md"
    lines = f.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is not None:
        keep = [l for l in lines[1:end] if not l.startswith(CLAUDE_ONLY_KEYS)]
        f.write_text("\n".join([lines[0]] + keep + lines[end:]), encoding="utf-8")


def _missing_deps(info):
    base = _skills_target()
    return [d for d in info.get("dependencias", []) if not (base / d["verifica"] / "SKILL.md").exists()]


def _install_plan(caps, missing, pack_id, cli):
    """Pasos (texto) para instalar lo que falta de un paquete en el entorno actual."""
    pack = caps["paquetes"][pack_id]
    info = pack.get("instalacion") or {}
    if not _applies(pack):
        return []
    faltan = [c for c in missing if c.get("paquete") == pack_id]
    target = _skills_target()
    steps = []
    if info.get("tipo") == "plugin":
        if faltan and _harness() == "claude" and cli:
            steps.append(f"claude plugin marketplace add {info['marketplace']}")
            steps.append(f"claude plugin install {pack['plugin']} --scope user"
                         + ("" if info.get("solo_plugin") else " (si falla, se copian los skills desde el repositorio)"))
        elif faltan and info.get("solo_plugin"):
            steps.append(f"✖ requiere el CLI de Claude Code para instalar el plugin {pack['plugin']} (o /plugin dentro de Claude Code)")
        elif faltan:
            why = "adaptadas a Codex" if _harness() == "codex" else "no se encontró el CLI de Claude Code"
            steps.append(f"git clone https://github.com/{info['repo']} y copiar {len(faltan)} skills a {target} ({why})")
        cli_req = info.get("cli")
        if cli_req and not shutil.which(cli_req["comando"]):
            steps.append(f"{' '.join(cli_req['instalar'])}   (CLI '{cli_req['comando']}' requerido por el plugin)")
            steps.append(f"después, una persona inicia sesión: {cli_req['login']}")
        if faltan and info.get("aviso") and _harness() == "claude":
            steps.append("⚠ " + info["aviso"])
    elif info.get("tipo") == "incluido":
        if faltan:
            steps.append(f"copiar {SKILL_DIR / info['ruta']} → {target / 'diseno-web-integral'}")
        deps = _missing_deps(info)
        if deps:
            steps.append("descargar de GitHub e instalar con su scripts/instalar.py: "
                         + ", ".join(f"{d['repo']} ({d['licencia']})" for d in deps))
    return steps


def _install_pack(caps, missing, pack_id, cli):
    pack = caps["paquetes"][pack_id]
    info = pack.get("instalacion") or {}
    faltan = [c for c in missing if c.get("paquete") == pack_id]
    target = _skills_target()
    codex = _harness() == "codex"
    if info.get("tipo") == "plugin":
        done = not faltan
        if faltan and not codex and cli:
            _run([cli, "plugin", "marketplace", "add", info["marketplace"]])  # falla si ya existe: no importa
            rc, out = _run([cli, "plugin", "install", pack["plugin"], "--scope", "user"])
            done = rc == 0
            if done:
                print(f"  {pack_id}: plugin instalado")
            else:
                print(f"  {pack_id}: falló la instalación del plugin")
                print("    " + (out.splitlines()[-1] if out else ""))
        if faltan and not done and not info.get("solo_plugin"):
            print(f"  {pack_id}: se copian los skills desde {info['repo']}")
            with tempfile.TemporaryDirectory() as tmp:
                rc, out = _run(["git", "-c", "core.longpaths=true", "clone", "--depth", "1",
                                f"https://github.com/{info['repo']}.git", tmp + "/r"])
                if rc != 0:
                    print(f"  {pack_id}: git clone falló: {out}")
                    return
                for c in faltan:
                    src, dst = Path(tmp) / "r" / info["ruta_skills"] / c["nombre"], target / c["nombre"]
                    if dst.exists():
                        print(f"  {c['nombre']:<36} ya existe otra skill con ese nombre: no se tocó")
                    elif (src / "SKILL.md").exists():
                        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git"))
                        if codex:
                            _adapt_for_codex(dst)
                        print(f"  {c['nombre']:<36} instalada")
                    else:
                        print(f"  {c['nombre']:<36} no está en {info['repo']}")
        cli_req = info.get("cli")
        if cli_req and not shutil.which(cli_req["comando"]):
            npm = shutil.which("npm")
            if not npm:
                print(f"  {pack_id}: falta npm para instalar '{cli_req['comando']}' ({' '.join(cli_req['instalar'])})")
            else:
                rc, out = _run([npm] + cli_req["instalar"][1:])
                print(f"  {pack_id}: CLI '{cli_req['comando']}' {'instalado' if rc == 0 else 'no se pudo instalar: ' + out[-300:]}")
            print(f"  {pack_id}: inicie sesión (interactivo, lo hace una persona): {cli_req['login']}")
    elif info.get("tipo") == "incluido":
        src, dst = SKILL_DIR / info["ruta"], target / "diseno-web-integral"
        if faltan and not dst.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*-workspace"))
            if codex:
                _adapt_for_codex(dst)
            print(f"  diseno-web-integral instalada en {dst}")
        deps = _missing_deps(info)
        if not deps:
            return
        import urllib.request
        with tempfile.TemporaryDirectory() as tmp:
            for d in deps:
                url = f"https://codeload.github.com/{d['repo']}/zip/refs/heads/main"
                try:
                    urllib.request.urlretrieve(url, str(Path(tmp) / f"{d['zip']}.zip"))
                except OSError as e:
                    print(f"  {d['repo']}: no se pudo descargar ({e})")
            installer = (dst if dst.exists() else src) / "scripts" / "instalar.py"
            dest_args = (["--destino", "codex", "--dir-codex", str(target)] if codex
                         else ["--destino", "claude", "--dir-claude", str(_claude_home())])
            rc, out = _run([sys.executable, str(installer), "--zips", tmp] + dest_args)
            print("  " + out.replace("\n", "\n  "))


def _sync(caps, defaults):
    """Agrega al registro del proyecto los paquetes y skills nuevos del skill, sin tocar decisiones previas."""
    ids = {c["id"] for c in caps.get("skills", [])}
    caps.setdefault("paquetes", {}).update(defaults.get("paquetes", {}))
    added = [c for c in defaults.get("skills", []) if c["id"] not in ids]
    caps.setdefault("skills", []).extend(added)
    # Marcadores antiguos sin fuente (versión previa del registro): se retiran si nadie los configuró
    default_ids = {c["id"] for c in defaults.get("skills", [])}
    legacy = [c for c in caps["skills"] if c["id"] not in default_ids and c.get("estado") == "por_configurar"
              and not c.get("fuente") and not c.get("registrado")]
    caps["skills"] = [c for c in caps["skills"] if c not in legacy]
    return added, legacy


def parse_github_source(src):
    # github:owner/repo[/subdir][@ref]
    m = re.match(r"^github:([^/]+)/([^/@]+)(/[^@]*)?(?:@(.+))?$", src)
    if not m:
        return None
    owner, repo, sub, ref = m.groups()
    return owner, repo, (sub or "").strip("/"), ref


def cmd_cap(a):
    root = require_root()
    caps = _caps(root)
    act = a.action

    if act == "list":
        for kind in ("skills", "mcp", "rag"):
            items = caps.get(kind, [])
            if a.kind and a.kind != kind:
                continue
            print(f"\n[{kind}]")
            for c in items:
                if a.pack and c.get("paquete") != a.pack:
                    continue
                ph = ",".join(c.get("fases", []))
                print(f"  {c['id']:<36} {c.get('estado',''):<20} fases={ph:<28} {c.get('skill') or c.get('fuente') or c.get('url') or c.get('comando') or c.get('ruta') or c.get('endpoint') or ''}")
        return

    if act == "for-phase":
        _check_phases([a.phase])
        state = load(root, "state.json")
        prof, verify = _profile(state), _verify_level(state)

        def by_profile(c):
            """Recorta las capacidades según el perfil; --all muestra todas (uso a pedido)."""
            if a.all:
                return True
            if c.get("paquete") == DESIGN_PACK and prof["diseno"] != "integral":
                return False
            if c.get("rol") == "revisor":
                return verify == "completo"
            if c["id"] in VERIFY_ON_DEMAND and verify != "completo":
                return False
            if c.get("paquete"):  # paquetes integrados
                return prof["skills"] == "todos" or (prof["skills"] == "principal" and c.get("rol") == "principal")
            return True  # skills de terceros, MCP y RAG registrados por el equipo

        print(f"Capacidades para la fase {a.phase} (perfil: {_describe_profile(state)}; verificación {verify}):")
        found = hidden = 0
        for kind in ("skills", "mcp", "rag"):
            items = [c for c in caps.get(kind, []) if (a.phase in c.get("fases", []) or "*" in c.get("fases", []))
                     and _applies(c)]
            kept = [c for c in items if by_profile(c)]
            hidden += len(items) - len(kept)
            items = kept
            items.sort(key=lambda c: {"principal": 0, "revisor": 2}.get(c.get("rol"), 1))
            how = "herramienta Skill" if _harness() == "claude" else "mencione $nombre"
            for c in items:
                usable = c.get("estado") in ("aprobado", "activo")
                found = True
                flag = "✔ usar" if usable else f"· {c.get('estado')}"
                rol = f"({c['rol']})" if c.get("rol") else ""
                print(f"  [{kind}] {c['id']:<36} {flag:<22} {rol:<16} {c.get('proposito','')}")
                if kind == "skills" and usable and c.get("invocacion") == "script":
                    note = "" if c.get("cli_listo") else "  ⚠ falta el CLI de Codex o su sesión"
                    print(f"           → python sai.py xreview <ID> --point <G1|DoR|G4|G6>{note}")
                elif kind == "skills" and usable and c.get("invocacion") == "nativa" and c.get("instalado"):
                    print(f"           → invoque el skill «{c['skill']}» ({how}) o lea {c['ruta_local']}/SKILL.md")
                elif kind == "skills" and usable and c.get("ruta_local"):
                    print(f"           → lea {c['ruta_local']}/SKILL.md y siga sus instrucciones")
        if not found:
            print("  (ninguna para este perfil; trabaje con las referencias del skill)")
        if hidden:
            print(f"  {hidden} más omitidas por el perfil (úselas solo si el usuario las pide: cap for-phase {a.phase} --all)")
        return

    if act == "detect":
        print("Skills nativos detectados en este entorno:")
        _detect(root, caps)
        save(root, "capabilities.json", caps)
        pend = [c["id"] for c in caps.get("skills", []) if c.get("instalado") and c.get("estado") == "pendiente_revision"]
        if pend:
            print(f"Pendientes de revisión humana: {len(pend)}. Apruebe por paquete con:")
            print('  python sai.py cap approve --pack <paquete> --by "Nombre (rol)"')
        return

    if act == "install":
        if not caps.get("paquetes"):
            die("El registro es de una versión anterior. Ejecute primero: python sai.py cap sync")
        if a.pack and a.pack not in caps["paquetes"]:
            die(f"Paquete desconocido. Opciones: {', '.join(caps['paquetes'])}")
        _, missing = _detect(root, caps, quiet=True)
        cli = _find_claude_cli()
        if a.pack and not _applies(caps["paquetes"][a.pack]):
            ok(f"El paquete '{a.pack}' no aplica en este entorno ({_harness()}).")
            return
        plans = {p: _install_plan(caps, missing, p, cli) for p in ([a.pack] if a.pack else caps["paquetes"])}
        plans = {p: s for p, s in plans.items() if s}
        if not plans:
            ok(f"Todos los paquetes y sus dependencias ya están instalados (entorno: {_harness()}).")
            return
        print("Plan de instalación (fuentes originales):")
        for p, steps in plans.items():
            print(f"  [{p}]")
            for s in steps:
                print(f"     - {s}")
        if not a.yes:
            print("\nInstalar código de terceros es una decisión humana. Cuando una persona lo autorice:")
            print("  python sai.py" + (" --harness codex" if _harness() == "codex" else "") + " cap install"
                  + (f" --pack {a.pack}" if a.pack else "") + " --yes")
            return
        print("\nInstalando…")
        for p in plans:
            _install_pack(caps, missing, p, cli)
        print("\nResultado:")
        _detect(root, caps)
        save(root, "capabilities.json", caps)
        print("Recargue Claude Code (/reload-plugins o sesión nueva) para que la herramienta Skill vea lo instalado."
              if _harness() == "claude" else "Abra una sesión nueva de Codex para que cargue las skills instaladas.")
        print('Instalado no es aprobado: revise y apruebe con  python sai.py cap approve --pack <paquete> --by "Nombre (rol)"')
        return

    if act == "sync":
        defaults = json.loads((ASSETS / "capabilities.default.json").read_text(encoding="utf-8"))
        added, legacy = _sync(caps, defaults)
        ok(f"Registro sincronizado: {len(added)} skills nuevos" + (f", {len(legacy)} marcadores antiguos retirados" if legacy else ""))
        _detect(root, caps)
        save(root, "capabilities.json", caps)
        return

    if act == "add-skill":
        _check_phases(a.phases)
        if _find_cap(caps, a.id)[1]:
            die(f"Ya existe una capacidad con id {a.id}")
        entry = {"id": a.id, "nombre": a.name or a.id, "fuente": a.source, "fases": a.phases,
                 "proposito": a.purpose or "", "estado": "pendiente_revision", "ruta_local": None,
                 "registrado": now()}
        caps.setdefault("skills", []).append(entry)
        save(root, "capabilities.json", caps)
        ok(f"Skill '{a.id}' registrado (pendiente_revision). Descárguelo con: python sai.py cap fetch {a.id}")
        return

    if act == "fetch":
        kind, c = _find_cap(caps, a.id)
        if kind != "skills":
            die("fetch solo aplica a skills.")
        src = c.get("fuente") or die("La capacidad no tiene 'fuente'.")
        dest = root / ROOT_DIRNAME / "vendor-skills" / c["id"]
        if dest.exists():
            shutil.rmtree(dest)
        gh = parse_github_source(src)
        if gh:
            owner, repo, sub, ref = gh
            with tempfile.TemporaryDirectory() as tmp:
                cmd = ["git", "-c", "core.longpaths=true", "clone", "--depth", "1"] + (["--branch", ref] if ref else []) + \
                      [f"https://github.com/{owner}/{repo}.git", tmp + "/r"]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    die("git clone falló: " + r.stderr.strip())
                srcdir = Path(tmp) / "r" / sub
                if not srcdir.exists():
                    die(f"No existe el subdirectorio '{sub}' en {owner}/{repo}")
                shutil.copytree(srcdir, dest, ignore=shutil.ignore_patterns(".git"))
        elif Path(src).expanduser().exists():
            p = Path(src).expanduser()
            if p.suffix in (".zip", ".skill"):
                shutil.unpack_archive(str(p), str(dest), "zip")
            else:
                shutil.copytree(p, dest)
        else:
            die("Fuente no soportada. Use github:owner/repo[/subdir][@ref] o una ruta local (carpeta, .zip, .skill).")
        # Si el zip trae una carpeta raíz, aplanar
        kids = [k for k in dest.iterdir()]
        if len(kids) == 1 and kids[0].is_dir() and not (dest / "SKILL.md").exists():
            inner = kids[0]
            for item in inner.iterdir():
                shutil.move(str(item), dest / item.name)
            inner.rmdir()
        skill_md = list(dest.rglob("SKILL.md"))
        c["ruta_local"] = str(dest.relative_to(root))
        c["estado"] = "pendiente_revision"
        c["descargado"] = now()
        c["skill_md"] = [str(p.relative_to(root)) for p in skill_md]
        save(root, "capabilities.json", caps)
        ok(f"Descargado en {c['ruta_local']}")
        if not skill_md:
            print("⚠ No se encontró SKILL.md: puede no ser un skill válido.")
        print("Archivos a revisar antes de aprobar (lea SKILL.md y TODO script):")
        for f in sorted(dest.rglob("*")):
            if f.is_file():
                print(f"   {f.relative_to(root)}  ({f.stat().st_size} B)")
        flagged = _scan_risky(dest)
        if flagged:
            print("⚠ Patrones sensibles detectados (revisar con atención):")
            for f, pat in flagged:
                print(f"   {f.relative_to(root)}: {pat}")
        print(f"Cuando una persona lo revise: python sai.py cap approve {c['id']} --by \"Nombre (rol)\"")
        return

    if act == "add-mcp":
        _check_phases(a.phases)
        if _find_cap(caps, a.id)[1]:
            die(f"Ya existe una capacidad con id {a.id}")
        if not (a.url or a.command):
            die("Indique --url (servidor HTTP/SSE remoto) o --command (servidor stdio local).")
        entry = {"id": a.id, "nombre": a.name or a.id, "transporte": "http" if a.url else "stdio",
                 "url": a.url, "comando": a.command, "args": a.args or [], "env": a.env or [],
                 "fases": a.phases, "proposito": a.purpose or "", "estado": "pendiente_revision", "registrado": now()}
        caps.setdefault("mcp", []).append(entry)
        save(root, "capabilities.json", caps)
        ok(f"MCP '{a.id}' registrado.")
        if a.write_mcp_json:
            _write_mcp_json(root, entry)
        return

    if act == "add-rag":
        _check_phases(a.phases)
        if _find_cap(caps, a.id)[1]:
            die(f"Ya existe una capacidad con id {a.id}")
        if not (a.path or a.endpoint or a.mcp):
            die("Indique --path (carpeta local a indexar), --endpoint (API RAG HTTP) o --mcp (id de un MCP que expone búsqueda).")
        entry = {"id": a.id, "nombre": a.name or a.id,
                 "tipo": "local" if a.path else ("http" if a.endpoint else "mcp"),
                 "ruta": a.path, "endpoint": a.endpoint, "mcp": a.mcp, "auth_env": a.auth_env,
                 "fases": a.phases, "proposito": a.purpose or "", "estado": "pendiente_revision", "registrado": now()}
        caps.setdefault("rag", []).append(entry)
        save(root, "capabilities.json", caps)
        ok(f"RAG '{a.id}' registrado. "
           + (f"Indexe con: python rag.py index {a.id}" if a.path else "Consulte con: python rag.py query " + a.id + " \"pregunta\""))
        return

    if act in ("approve", "disable") and a.pack:
        sel = [c for c in caps.get("skills", []) if c.get("paquete") == a.pack]
        if not sel:
            die(f"No hay skills del paquete '{a.pack}'. Paquetes: {', '.join(caps.get('paquetes', {})) or '(ninguno)'}")
        if act == "approve":
            validate_approvers([a.by] if a.by else [])
            sel = [c for c in sel if c.get("ruta_local") and c.get("estado") != "deshabilitado"]
            if not sel:
                die("Ningún skill del paquete está instalado o descargado. Ejecute: python sai.py cap detect")
        for c in sel:
            if act == "approve":
                c.update(estado="aprobado", aprobado_por=a.by, aprobado_fecha=now())
            else:
                c["estado"] = "deshabilitado"
        save(root, "capabilities.json", caps)
        ok(f"{len(sel)} skills de '{a.pack}' → {'aprobado' if act == 'approve' else 'deshabilitado'}")
        return

    if act in ("approve", "disable"):
        kind, c = _find_cap(caps, a.id)
        if not c:
            die(f"No existe {a.id}")
        if act == "approve":
            validate_approvers([a.by] if a.by else [])
            if kind == "skills" and not c.get("ruta_local"):
                die("Instale o descargue y revise el skill antes de aprobarlo (cap detect / cap fetch).")
            c["estado"] = "aprobado"
            c["aprobado_por"] = a.by
            c["aprobado_fecha"] = now()
        else:
            c["estado"] = "deshabilitado"
        save(root, "capabilities.json", caps)
        ok(f"{a.id} → {c['estado']}")
        return

    if act == "set-source":
        kind, c = _find_cap(caps, a.id)
        if not c:
            die(f"No existe {a.id}")
        c["fuente"] = a.source
        c["estado"] = "pendiente_revision"
        save(root, "capabilities.json", caps)
        ok(f"Fuente de {a.id} = {a.source}. Ahora: python sai.py cap fetch {a.id}")
        return


RISKY = [
    (re.compile(r"curl[^\n|]*\|\s*(ba)?sh"), "curl | sh"),
    (re.compile(r"rm\s+-rf\s+(/|~|\$HOME)"), "rm -rf sobre raíz/home"),
    (re.compile(r"base64\s+(-d|--decode)"), "decodificación base64"),
    (re.compile(r"(AWS_SECRET|GITHUB_TOKEN|API_KEY|PASSWORD)\s*="), "credenciales en claro"),
    (re.compile(r"eval\(|exec\("), "eval/exec dinámico"),
    (re.compile(r"(ignore|ignora)\s+(all\s+)?(previous|anteriores)", re.I), "posible inyección de instrucciones"),
]


def _scan_risky(dest):
    out = []
    for f in dest.rglob("*"):
        if f.is_file() and f.stat().st_size < 2_000_000:
            try:
                t = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for rx, label in RISKY:
                if rx.search(t):
                    out.append((f, label))
    return out


def _write_mcp_json(root, entry):
    f = root / ".mcp.json"
    data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"mcpServers": {}}
    if entry["transporte"] == "http":
        cfg = {"type": "http", "url": entry["url"]}
    else:
        cfg = {"command": entry["comando"], "args": entry["args"]}
        if entry["env"]:
            cfg["env"] = {e: "${" + e + "}" for e in entry["env"]}
    data.setdefault("mcpServers", {})[entry["id"]] = cfg
    f.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ok(f".mcp.json actualizado con '{entry['id']}' (Claude Code lo cargará al reiniciar la sesión).")


# --------------------------------------------------------------------------
# reporte
# --------------------------------------------------------------------------
def cmd_report(a):
    root = require_root()
    state = load(root, "state.json")
    hs = state["historias"]
    n = state["sprint"]["numero"]
    en = {k: v for k, v in hs.items() if v.get("sprint") == n}
    done = [k for k, v in en.items() if v["estado"] == "done"]
    first_pass = [k for k, v in en.items()
                  if v["estado"] in ("release", "done") and not any(g.get("estado") == "rechazado" for g in v["gates"].values())]
    out = [f"# Reporte Scrum-AI Delivery — {state['proyecto']['nombre']}", "",
           f"- Fecha: {now()}", f"- Fase: {state['fase']} {ROADMAP[state['fase']]}",
           f"- Sprint: {n} — {state['sprint'].get('objetivo','')}", "",
           "## Indicadores", "",
           "| Indicador | Valor | Meta |", "|---|---|---|",
           f"| Predictibilidad (completadas/planificadas) | {len(done)}/{len(en)} | ≥85% |",
           f"| First-pass acceptance | {len(first_pass)}/{len([1 for v in en.values() if v['estado'] in ('release','done')])} | ≥80% |",
           "", "## Historias", "", "| ID | Título | Estado | Gates aprobados | Score |", "|---|---|---|---|---|"]
    for k, v in hs.items():
        gates = ",".join(g for g, d in sorted(v["gates"].items()) if d.get("estado") == "aprobado") or "—"
        sc = f"{v['score']['total']}" if v.get("score") else "—"
        out.append(f"| {k} | {v['titulo']} | {v['estado']} | {gates} | {sc} |")
    text = "\n".join(out) + "\n"
    dst = root / ROOT_DIRNAME / "sprints" / f"reporte-sprint-{n}.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    print(text)
    ok(f"Guardado en {dst.relative_to(root)}")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(description="Scrum-AI Delivery — gestor de estado, gates y capacidades")
    p.add_argument("--harness", choices=["claude", "codex"],
                   help="Entorno que ejecuta el skill (por defecto se detecta; también SAI_HARNESS)")
    sp = p.add_subparsers(dest="cmd", required=True)

    x = sp.add_parser("init", help="Inicializa ./scrum-ai en el proyecto")
    x.add_argument("--name", required=True)
    x.add_argument("--mode", choices=["nuevo", "existente"], default="nuevo",
                   help="existente = hay código previo → Sprint 0 incluye auditoría")
    x.add_argument("--path", default=".")
    x.add_argument("--github", action="store_true", help="Copia plantillas de issue/PR y workflow de quality gates")
    x.add_argument("--tests-in", choices=list(TEST_PLACES), help="Dónde se hacen las pruebas")
    x.add_argument("--tests-path", help="Carpeta del sandbox o nombre de la rama de pruebas")
    x.add_argument("--force", action="store_true")
    x.add_argument("--approver", help='Persona que aprueba en el chat, "Nombre (rol)"')
    x.set_defaults(fn=cmd_init, profile="estandar")

    x = sp.add_parser("config", help="Ver o cambiar perfil, verificación y lugar de las pruebas")
    x.add_argument("--tests-in", choices=list(TEST_PLACES))
    x.add_argument("--tests-path")
    x.add_argument("--approver", help='Persona que aprueba en el chat, "Nombre (rol)"; se usa cuando ella responde '
                                      '"aprobado" sin repetir nombre y rol ("ninguno" para borrarla)')
    x.set_defaults(fn=cmd_config, profile=None)
    for x in (sp.choices["init"], sp.choices["config"]):
        x.add_argument("--profile", choices=list(PROFILES),
                       help="; ".join(f"{k} = {v}" for k, v in PROFILE_HELP.items()) + " (init: estandar)")
        x.add_argument("--skills", choices=SKILL_LEVELS,
                       help="Skills externos por fase: ninguno, solo principales o todos")
        x.add_argument("--skip-stages", help="Etapas omitidas por defecto: flujo,mockup,uat | ninguno")
        x.add_argument("--design", choices=["basico", "integral"],
                       help="basico = wireframe/mockup simple; integral = diseno-web-integral completo")
        x.add_argument("--detail", choices=["breve", "completo"], help="Extensión de los artefactos y respuestas")
        x.add_argument("--verify", choices=list(VERIFY_LEVELS),
                       help="ligero = pruebas manuales y revisión cruzada a pedido; completo = todo automático")

    x = sp.add_parser("status", help="Estado y siguiente paso")
    x.set_defaults(fn=cmd_status)

    x = sp.add_parser("phase", help="Ver o avanzar la fase del roadmap S0–S6")
    x.add_argument("--set")
    x.add_argument("--approver", help="Persona que autoriza el cambio de fase")
    x.add_argument("--force", action="store_true")
    x.set_defaults(fn=cmd_phase)

    x = sp.add_parser("sprint0", help="Checklist de entregables del Sprint 0")
    x.add_argument("item", nargs="?")
    x.add_argument("--evidence")
    x.add_argument("--undo", action="store_true")
    x.set_defaults(fn=cmd_sprint0)

    x = sp.add_parser("sprint", help="Iniciar/cerrar sprint")
    x.add_argument("action", choices=["start", "close"])
    x.add_argument("--goal")
    x.set_defaults(fn=cmd_sprint)

    x = sp.add_parser("story", help="Historias de usuario")
    x.add_argument("action", choices=["add", "list", "show", "move", "skip"])
    x.add_argument("id", nargs="?")
    x.add_argument("title", nargs="?")
    x.add_argument("--epic")
    x.add_argument("--skip", help="add/skip: etapas omitidas para esta historia (flujo,mockup,uat | ninguno)")
    x.add_argument("--to")
    x.add_argument("--reason")
    x.set_defaults(fn=lambda a: (a.action == "move" and not a.to and setattr(a, "to", a.title)) or cmd_story(a))

    for kind in ("dor", "dod"):
        x = sp.add_parser(kind, help=f"Marcar ítems de {kind.upper()}")
        x.add_argument("id")
        x.add_argument("items", nargs="*")
        x.add_argument("--undo", action="store_true")
        x.add_argument("--no-advance", action="store_true", help="No mover la historia aunque quede completo")
        x.set_defaults(fn=(lambda k: (lambda a: cmd_check(a, k)))(kind))

    x = sp.add_parser("gate", help="Registrar decisión humana de un gate G1–G6 (o ver su definición)")
    x.add_argument("id", nargs="?", help="ID de historia (omitir para ver la definición del gate)")
    x.add_argument("gate", nargs="?")
    x.add_argument("--decision", choices=["aprobado", "rechazado"])
    x.add_argument("--approver", action="append", default=[], help="Nombre (rol). Repetible.")
    x.add_argument("--evidence", action="append", help="Ruta o URL. Repetible.")
    x.add_argument("--notes")
    x.add_argument("--info", action="store_true")
    x.add_argument("--force", action="store_true")
    x.add_argument("--no-advance", action="store_true", help="No mover la historia al aprobar")

    def _gate(a):
        if a.id in GATES and not a.gate:
            a.gate, a.id = a.id, None
        if not a.gate:
            die("Indique el gate (G1–G6).")
        cmd_gate(a)
    x.set_defaults(fn=_gate)

    x = sp.add_parser("score", help="Scorecard ponderado de calidad")
    x.add_argument("id", nargs="?")
    for k, n, w in SCORECARD:
        x.add_argument(f"--{k}", type=int, required=True, help=f"{n} (peso {w}%%), 1–5")
    x.add_argument("--critical-vuln", action="store_true", help="Vulnerabilidad CVSS 9.0–10")
    x.add_argument("--failed-test", action="store_true", help="Prueba obligatoria fallida")
    x.add_argument("--mandatory-missing", action="store_true", help="Criterio obligatorio incumplido")
    x.add_argument("--evaluator")
    x.add_argument("--no-advance", action="store_true", help="No mover la historia aunque DoD y scorecard se cumplan")
    x.set_defaults(fn=cmd_score)

    x = sp.add_parser("adr", help="Nuevo Architecture Decision Record")
    x.add_argument("title")
    x.set_defaults(fn=cmd_adr)

    x = sp.add_parser("audit", help="Auditoría de código existente (Sprint 0)")
    x.add_argument("component", nargs="?")
    x.add_argument("--state", type=int, help="Estado técnico 1–5 (5 = excelente)")
    x.add_argument("--value", type=int, help="Valor de negocio 1–5")
    x.add_argument("--action", choices=["Conservar", "Refactorizar", "Reconstruir", "Retirar"])
    x.add_argument("--notes")
    x.set_defaults(fn=cmd_audit)

    x = sp.add_parser("cap", help="Capacidades externas: skills de terceros, MCP, RAG")
    x.add_argument("action", choices=["list", "for-phase", "detect", "install", "sync", "add-skill", "fetch", "set-source",
                                      "add-mcp", "add-rag", "approve", "disable"])
    x.add_argument("phase_or_id", nargs="?")
    x.add_argument("--id")
    x.add_argument("--name")
    x.add_argument("--kind", choices=["skills", "mcp", "rag"])
    x.add_argument("--source", help="github:owner/repo[/subdir][@ref] | carpeta | .zip | .skill")
    x.add_argument("--phases", nargs="+", default=["*"])
    x.add_argument("--purpose")
    x.add_argument("--url")
    x.add_argument("--command")
    x.add_argument("--args", nargs="*")
    x.add_argument("--env", nargs="*", help="Nombres de variables de entorno requeridas (sin valores)")
    x.add_argument("--write-mcp-json", action="store_true")
    x.add_argument("--path")
    x.add_argument("--endpoint")
    x.add_argument("--mcp")
    x.add_argument("--auth-env", help="Variable de entorno con el token del RAG HTTP")
    x.add_argument("--by")
    x.add_argument("--pack", help="Paquete (agent-skills, ecc, diseno-web-integral, codex) para list/install/approve/disable")
    x.add_argument("--yes", action="store_true", help="install: ejecuta el plan (sin esto solo lo muestra)")
    x.add_argument("--all", action="store_true", help="for-phase: muestra también lo que el perfil omite")

    def _cap(a):
        if a.action == "for-phase":
            a.phase = a.phase_or_id
        elif a.phase_or_id and not a.id:
            a.id = a.phase_or_id
        if a.action not in ("list", "for-phase", "detect", "install", "sync") and not a.id \
                and not (a.pack and a.action in ("approve", "disable")):
            die("Indique el id de la capacidad.")
        cmd_cap(a)
    x.set_defaults(fn=_cap)

    x = sp.add_parser("xreview", help="Revisión cruzada de Codex antes de G1, DoR, G4 o G6 (solo en Claude Code)")
    x.add_argument("id")
    x.add_argument("--point", required=True, choices=list(XREVIEW_AT.values()))
    x.add_argument("--focus", help="Foco adicional para la revisión (G1, DoR, G6)")
    x.add_argument("--base", help="G4: rama o commit base del diff (p. ej. main)")
    x.set_defaults(fn=cmd_xreview)

    x = sp.add_parser("report", help="Reporte del sprint con indicadores")
    x.set_defaults(fn=cmd_report)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    if a.harness:
        os.environ["SAI_HARNESS"] = a.harness
    a.fn(a)


if __name__ == "__main__":
    main()
