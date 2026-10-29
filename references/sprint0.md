# Sprint 0 — conocer antes de construir

Objetivo: alinear visión, personas, tecnología y proceso para iniciar el desarrollo con una base sólida, reduciendo riesgos y maximizando la predictibilidad. Si hay código existente, obtener un diagnóstico claro y accionable que alimente el backlog real.

## Entregables (checklist `sai.py sprint0`)
| Clave | Entregable | Cómo lo produce Claude |
|---|---|---|
| `vision_mvp` | Visión / MVP: alcance, valor y primera versión funcional | Entrevista guiada → `scrum-ai/vision/vision.md` |
| `inventario_funcional` | Listado de funcionalidades y componentes existentes | Recorrido del repo / sistema actual; tabla en la auditoría o en `vision/` |
| `matriz_roles` | Equipos, responsabilidades y forma de trabajo | Completar `scrum-ai/vision/roles-raci.md` con nombres reales |
| `diagnostico_tecnico` | Estado del código, arquitectura, dependencias y riesgos (solo modo existente) | Auditoría (abajo) |
| `adr` | Decisiones técnicas clave documentadas | `sai.py adr "<título>"` por cada decisión |
| `dor_dod` | Criterios de entrada y salida de historias | Revisar `scrum-ai/dor-dod.md` con el equipo |
| `estructura_repositorio` | Carpetas, ramas y convenciones | Proponer estructura y convenciones (ver `github.md`) |
| `agents_md` | Guía para agentes de IA en el proyecto | Completar `AGENTS.md` (stack, comandos, convenciones) |
| `constraints_md` | Restricciones, políticas y límites operativos | Completar `CONSTRAINTS.md` |
| `pipeline_ci_cd` | Automatización, quality gates y despliegue | Adaptar `.github/workflows/quality-gates.yml` al stack |
| `sprint1_refinado` | Backlog priorizado y listo para iniciar | Historias del Sprint 1 con ficha y DoR en curso |

Marca cada uno cuando la persona responsable lo valide: `sai.py sprint0 <clave> --evidence <ruta>`.

## Auditoría del código existente (modo `existente`)
Proceso: **Analizar repositorio → Evaluar estado → Definir acción → Documentar hallazgos → Generar backlog real.**

0. **La auditoría es de solo lectura.** No corrijas, migres ni regeneres nada durante el Sprint 0: los hallazgos se convierten en historias del backlog. Si para evaluar hace falta un experimento, hazlo en el lugar de pruebas registrado (`sai.py config`), nunca sobre el repositorio auditado.
1. **Inventario**: árbol del repositorio (frontend, backend, database/migrations, docs, tests, .github/workflows, manifiestos de dependencias, docker-compose, README) con semáforo por carpeta. Lee archivos clave; no inventes: si no puedes ver algo, márcalo como "no evaluado".
2. **Evaluación por componente** (Arquitectura, Frontend, Backend, Datos, Componentes, Dependencias, Seguridad, Pruebas, CI/CD, Documentación, Deuda técnica): estado actual 1–5 y semáforo en calidad, mantenibilidad, seguridad, cobertura de pruebas, dependencias y riesgo. Apóyate en evidencia objetiva cuando sea posible: pruebas, `npm audit`/`pip-audit`, linters, cobertura, antigüedad de dependencias. Con verificación `ligero`, entrega esos comandos para que la persona los ejecute y pegue la salida; con `completo`, ejecútalos tú.
3. **Criterios de decisión** (valor de negocio × estado técnico):
   - Valor alto + estado bueno → **Conservar** (usar como base)
   - Valor alto + estado malo → **Refactorizar** (mejorar y modernizar)
   - Valor bajo + estado bueno → **Retirar** (eliminar)
   - Valor bajo + estado malo → **Reconstruir** (desarrollar de nuevo)
   Registra: `sai.py audit <Componente> --state N --value N [--action X --notes "..."]`. El valor de negocio lo confirma el PO; la acción final la decide el equipo.
4. **Resultado**: distribución porcentual por acción (`sai.py audit` la calcula) y hallazgos (riesgos, oportunidades, recomendaciones) en `scrum-ai/audit/auditoria.md`.
5. **Salida principal — backlog real**: épicas, historias y tareas técnicas y funcionales derivadas (`sai.py story add ...`).

Capacidades útiles: skills de `code-review`/`security` en Review, MCP de GitHub para leer el repositorio e issues, RAG sobre documentación existente.

## Indicadores clave (seguimiento desde Sprint 1)
| Indicador | Descripción | Meta sugerida |
|---|---|---|
| Cumplimiento Sprint Goal | Entrega de los objetivos del sprint | ≥ 90% |
| Predictibilidad | Historias completadas vs. planificadas | ≥ 85% |
| Lead time | Desde la solicitud hasta producción | ≤ 10 días |
| Cycle time | Tiempo de desarrollo por historia | ≤ 5 días |
| First-pass acceptance | Historias aceptadas en primera revisión | ≥ 80% |
| Retrabajo IA | Historias que requieren retrabajo por hallazgos IA | ≤ 15% |
| Defectos escapados | Defectos en producción no detectados en QA | ≤ 5% |
| Frecuencia de despliegue | Despliegues en el periodo | ≥ 1 por semana |
| Satisfacción del equipo | Valoración 1–5 | ≥ 4.0 |

## Próximas decisiones para iniciar el Sprint 1 (todas humanas)
Validación de visión y alcance del MVP · asignación final de roles · aprobación de la arquitectura objetivo (ADR) · definición de entornos y accesos · confirmación del lugar de las pruebas y del nivel de verificación (`sai.py config`) · aprobación de DoR/DoD · activación del pipeline CI/CD · priorización y aprobación del backlog S1 · aprobación de AGENTS.md y CONSTRAINTS.md.

Preséntalas como una lista de pendientes con responsable; cuando estén resueltas: `sai.py phase --set S1 --approver "Nombre (PO)"` y `sai.py sprint start --goal "..."`.
