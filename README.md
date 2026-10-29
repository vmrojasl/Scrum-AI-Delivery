# Scrum-AI Delivery

Skill para Claude Code y Codex que conduce proyectos con la metodología **Scrum-AI Delivery**: Scrum + ingeniería asistida por IA + Spec-Driven Development + Quality Gates (G1–G6) con aprobación humana.

**Del requisito al release, con evidencia en cada paso.**

## Contenido

| Ruta | Qué es |
|---|---|
| [`MANUAL.md`](MANUAL.md) | Manual de usuario: instalación, ciclo completo, gates, comandos y solución de problemas |
| [`SKILL.md`](SKILL.md) | Definición del skill e instrucciones para el agente |
| [`references/`](references/) | Metodología, Sprint 0, ciclo de sprint, quality gates, GitHub, vibecoding, capacidades externas |
| [`assets/templates/`](assets/templates/) | Plantillas: visión, historia de usuario, DoR/DoD, flujo, diseño UI, ADR, sprint, retrospectiva, RACI, AGENTS.md, CONSTRAINTS.md |
| [`assets/github/`](assets/github/) | Plantillas de issue y PR, workflow de quality gates |
| [`scripts/sai.py`](scripts/sai.py) | CLI de la metodología (estado, historias, gates, scorecard) |
| [`scripts/rag.py`](scripts/rag.py) | Consulta a fuentes RAG locales o HTTP |
| [`vendor/diseno-web-integral/`](vendor/diseno-web-integral/) | Skill propietario de diseño web incluido; `sai.py cap install` lo instala con sus dependencias |

## Instalación

Claude Code:

```bash
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git ~/.claude/skills/scrum-ai-delivery
```

Codex:

```bash
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git ~/.agents/skills/scrum-ai-delivery
```

Al iniciar, el skill revisa los paquetes que usa (agent-skills, ECC, diseno-web-integral y, en Claude Code, el plugin de Codex para la revisión cruzada) y propone instalar los que falten desde sus repositorios originales (`sai.py cap install`). Detalles en [`MANUAL.md`](MANUAL.md).

Sitio: <https://vmrojasl.github.io/Scrum-AI-Delivery/>
