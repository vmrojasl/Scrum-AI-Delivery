# Protocolo de vibecoding controlado — controlar la IA para desarrollar con evidencia

El desarrollo asistido por IA sigue un microciclo verificable, con supervisión humana y límites claros de actuación.

## Microciclo (por tarea del plan técnico)
1. **Preparar contexto** — ficha de la historia (criterios AC), flujo (G2), mockup (G3), plan técnico, `AGENTS.md`, `CONSTRAINTS.md`, ADRs y el código relevante. Si hay RAG técnico aprobado (documentación de APIs, arquitectura), consúltalo.
2. **Generar plan** — lista corta de pasos: archivos a crear/modificar, pruebas a escribir (una o más por AC), riesgos. Muéstralo si la tarea es grande o toca áreas sensibles.
3. **Desarrollar** — cambios pequeños e incrementales en `feature/<ID>`; si hay skill `incremental-implementation` o `tdd` aprobado, síguelo (TDD: prueba que falla → código mínimo → refactor).
4. **Probar** — en el lugar de pruebas registrado (`sai.py config`). Con verificación `ligero` (por defecto), escribe las pruebas y entrega los comandos para que la persona los ejecute; con `completo`, ejecútalas tú. En ambos casos conserva la salida y no declares "pasa" sin ella.
5. **Revisar** — autorrevisión contra estándares y CONSTRAINTS, en una sola pasada. Con `completo`, usa además los skills `code-review` y `security` aprobados y corre linters, análisis de dependencias y SAST; con `ligero`, propón esos comandos a la persona.
6. **Corregir** — corrige lo que muestre la salida de pruebas. Con `ligero`, no reintentes en bucle: corrige, entrega los comandos de nuevo y espera el resultado. Si algo bloquea, identifícalo con claridad.
7. **Presentar evidencia** — PR (plantilla en `.github/PULL_REQUEST_TEMPLATE.md`) con tabla AC → prueba → resultado, salida de pruebas, informe de seguridad, capturas responsive y nota de qué se generó con IA. Con verificación `completo` en Claude Code y el paquete `codex` aprobado, adjunta también la revisión cruzada de Codex (`sai.py xreview <ID> --point G4`) y cómo se atendió cada hallazgo. Con `ligero`, solo si el usuario la pidió.

## Reglas no negociables
- **El agente no puede cambiar el alcance.** Si descubres que algo del alcance es inviable o incompleto, detente y propón el cambio al PO (puede volver a G1).
- **No puede saltarse pruebas.** Sin pruebas ejecutadas (por el agente o, con verificación `ligero`, por la persona) no hay G4.
- **No puede usar el proyecto como banco de pruebas.** Prototipos y proyectos de prueba van al lugar registrado. Si probar parece exigir rehacer o reestructurar código fuera del alcance de la historia, detente y pide autorización.
- **No puede desplegar por iniciativa propia.** El release es G6, humano.
- **Toda decisión crítica requiere validación humana** — HUMAN APPROVAL REQUIRED.

Además: no introduzcas dependencias no previstas en el plan técnico sin anotarlo; no expongas secretos; no envíes datos institucionales sensibles a servicios externos no autorizados.

## Mapa de Agent Skills por fase
Los skills principales de cada fase. Las complementarias y las reglas de convivencia están en `capacidades-externas.md` → 1b. Úsalos solo si `cap for-phase` los lista para el perfil del proyecto.

| Fase | Skills principales | Entregables |
|---|---|---|
| 01 Define — levantamiento de requisitos | `agent-skills:interview-me`, `agent-skills:spec-driven-development` | Historias, reglas, criterios, dependencias |
| 02 Plan — planificación del sprint | `agent-skills:planning-and-task-breakdown`, `agent-skills:constraint-driven-development` | Plan del sprint, backlog priorizado, tareas, criterios de salida |
| 03 Design — diseño de solución | `diseno-web-integral`, `agent-skills:api-and-interface-design`, `agent-skills:documentation-and-adrs` | Wireframes y mockups, estados y responsive, diseño de APIs, ADR, prototipo |
| 04 Build — desarrollo incremental | `agent-skills:incremental-implementation`, `agent-skills:test-driven-development` | Código, pruebas unitarias, integración con APIs, despliegue en ambiente de pruebas |
| 05 Verify — diagnóstico y pruebas | `ecc:verification-loop`, `agent-skills:debugging-and-error-recovery` | Resultados de pruebas, informe PASS/FAIL, evidencia QA, reporte de hallazgos, correcciones |
| 06 Review — auditoría de calidad y seguridad | `agent-skills:code-review-and-quality`, `agent-skills:security-and-hardening` | Informe de revisión, evidencia de seguridad, cumplimiento de criterios, aprobación técnica (humana) |
| 07 Ship — publicación | `agent-skills:ci-cd-and-automation`, `agent-skills:shipping-and-launch` | Release, monitoreo y observabilidad, plan de rollback, documentación de despliegue |

En el microciclo de Build, `incremental-implementation` marca el ritmo: cada incremento pasa por TDD. Con verificación `completo`, antes de abrir el PR se corre `ecc:verification-loop` para adjuntar su informe a la evidencia de G4. Con `ligero`, ese informe se reemplaza por la salida de las pruebas que ejecuta la persona.

Vienen precargados en `scrum-ai/capabilities.json` y `init` detecta si están instalados. Después de que una persona los revisa (`cap approve --pack <paquete>`), Claude los invoca por su nombre con la herramienta Skill. Si un skill no está disponible, Claude ejecuta la fase con estas referencias: la metodología no depende de ningún skill externo para funcionar.
