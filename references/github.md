# GitHub que organiza, valida y deja trazabilidad

Cada historia avanza por estados claros, activa quality gates con GitHub Actions y mantiene evidencia desde la épica hasta el release.

## Estados del tablero (GitHub Projects)
**Planificación:** Backlog → Refinamiento → Flujo → Mockup → Ready
**Ejecución y validación:** Desarrollo → QA → UAT → Done (cerrada con evidencia)

Equivalencia con `sai.py`: backlog/especificacion → Backlog/Refinamiento · flujo → Flujo · mockup/plan_tecnico → Mockup · ready → Ready · desarrollo → Desarrollo · pruebas → QA · uat/aceptacion → UAT · release/done → Done.

## Trazabilidad de una historia
Épica (objetivo de negocio) → Historia → Requisito (criterio de aceptación) → Flujo → Mockup → Código → Prueba → PR → Aprobación → Release.
Mantén los enlaces: el issue referencia `scrum-ai/backlog/<ID>.md`; el PR cierra el issue y enlaza `scrum-ai/evidence/<ID>/`; el release lista los IDs incluidos.

## Flujo con GitHub Actions
Issue → Branch → Pull Request → [Lint/Tipado → Tests → QA/Visual → Seguridad → Build → Deploy] → Merge a main → Release (versión liberada con evidencia).
Plantilla: `.github/workflows/quality-gates.yml` (con `init --github`). Ajusta los `TODO` al stack en Sprint 0. Usa un *environment* `produccion` con revisores requeridos (PO + Operaciones/TI) para que el despliegue a producción sea siempre una decisión humana (G6).

## Comandos útiles (gh CLI o MCP de GitHub)
Con el MCP de GitHub aprobado, usa sus herramientas equivalentes; sin él, `gh`:

```bash
# Etiquetas de estado (una vez, Sprint 0)
for l in backlog refinamiento flujo mockup ready desarrollo qa uat done; do gh label create "estado:$l" --force; done
for g in G1 G2 G3 G4 G5 G6; do gh label create "gate:$g-aprobado" --color 2ea44f --force; done
gh label create historia --force

# Crear issue desde la ficha
gh issue create --title "US-CONV-001: Consultar convocatorias" --body-file scrum-ai/backlog/US-CONV-001.md --label historia,estado:backlog

# Cambiar estado / registrar gate
gh issue edit <n> --remove-label estado:flujo --add-label estado:mockup --add-label gate:G2-aprobado

# Rama y PR
git switch -c feature/US-CONV-001
gh pr create --fill --body-file .github/PULL_REQUEST_TEMPLATE.md
```

Crear issues, etiquetas o PR modifica un repositorio compartido: confirma con el usuario antes de hacerlo la primera vez.

## Resultado
Más visibilidad (estado de cada historia en tiempo real) · mejor control (estados, revisiones y quality gates) · entregas confiables · historial auditable (evidencia de la épica al release) · automatización con GitHub Actions.
