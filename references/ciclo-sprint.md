# Ciclo de trabajo de cada sprint — de la historia al incremento en dos semanas

Una historia avanza por etapas con aprobaciones y evidencia. Debajo, para cada paso: estado en `sai.py`, fase de capacidades, qué hace Claude y cómo se sale.

**Lee solo la sección del paso en curso.** Al aprobar un gate, completar el DoR o aprobar DoD y scorecard, el script mueve la historia solo; no hace falta `story move` en esos pasos. Los gates se piden agrupados en cuatro puntos (planeación, diseño, entrega técnica y cierre; ver `quality-gates.md` → «Aprobar rápido»).

Las etapas 03 Flujo, 04 Mockup y 08 UAT se saltan cuando están omitidas para la historia, según el perfil o `story skip`. Los skills que se mencionan en cada paso se usan solo si `cap for-phase` los lista para el perfil del proyecto. Con diseño `basico`, el paso 04 produce un wireframe y un mockup simples, sin `diseno-web-integral`.

Las revisiones cruzadas de Codex que se mencionan abajo son automáticas solo con verificación `completo`; en `ligero` (por defecto) se corren solo si el usuario las pide. Las pruebas se hacen siempre en el lugar registrado (`sai.py config`); ver `perfiles.md`.

## Contenido
1. Selección del backlog · 2. Especificación · 3. Flujo · 4. Mockup · 5. Plan técnico · 6. Desarrollo IA · 7. Pruebas · 8. UAT · 9. Aceptación · 10. Release · 11. Retrospectiva · Actividades continuas · Ejemplo US-CONV-001

---

### 01 Selección del backlog — `backlog` · Plan
- Revisa el backlog priorizado con el PO y propone el Sprint Goal y las historias que caben (capacidad del equipo).
- `sai.py sprint start --goal "..."`; por cada historia comprometida: `sai.py story move <ID> especificacion`.
- Si hay skills `planning-and-task-breakdown` / `constraint-driven-development` aprobados, úsalos para desglosar y estimar; registra el plan en `scrum-ai/sprints/sprint-N/plan.md`.

### 02 Especificación — `especificacion` · Define → sale con **G1 Requisitos**
- Completa `scrum-ai/backlog/<ID>.md`: Como/Quiero/Para, valor esperado, reglas de negocio, dependencias, criterios de aceptación verificables (tabla ID/Condición/Resultado esperado) y evidencia requerida.
- Buenas prácticas para criterios: cubrir caso feliz, filtros/variantes, sin resultados (estado vacío útil), regla de negocio de borde, error del servidor (mensaje comprensible + reintento) y uso móvil. Cada criterio debe poder probarse.
- Pregunta lo que falte en vez de inventar reglas; consulta RAG de normativa cuando la regla dependa de documentos institucionales y cita la fuente.
- Antes de pedir G1, revisión cruzada (solo en Claude Code con el paquete `codex` aprobado; en Codex no aplica): `sai.py xreview <ID> --point G1`.
- **Sin esta ficha, la historia no entra a desarrollo.** Aprueban: PO + Dueño de proceso.

### 03 Flujo — `flujo` · Design → sale con **G2 Flujo**
- Archivo: `scrum-ai/design/<ID>/flujo.md` (se crea al mover). Dos miradas:
  - **BPMN 2.0 (negocio)**: carriles por actor, decisiones, excepciones, permisos, rutas alternativas.
  - **Mermaid / estados (interacción)**: navegación, estados de pantalla (carga, vacío, error, permisos) y respuestas del sistema.
- Verifica que cada criterio AC aparezca en algún camino. Aprueban: Dueño de proceso + Arquitecto de procesos.
- Decisión "¿Flujo aprobado?": No → ajustar diseño y volver a presentar.

### 04 Mockup — `mockup` · Design → sale con **G3 Diseño**
- Archivo: `scrum-ai/design/<ID>/diseno-ui.md`. Tres niveles: **wireframe** (estructura), **mockup visual** (contrato visual del desarrollo, con el sistema de diseño institucional) y **prototipo navegable** (interacción real).
- Si `diseno-web-integral` está aprobado, conduce este paso con él: su diagnóstico, diseño y validación medida producen el wireframe, el mockup y el prototipo, y lo que decida `DESIGN.md` se resume en `diseno-ui.md`. Si no está, Claude produce wireframes/prototipos en HTML o con el skill/MCP de diseño aprobado (p. ej. Figma vía MCP, `agent-skills:frontend-ui-engineering`). Incluye los estados obligatorios: carga, vacío, error, permisos, confirmación, responsive. Para accesibilidad, `ecc:accessibility`.
- La puerta de aprobación final de `diseno-web-integral` no reemplaza a G3: su resultado se adjunta como evidencia y G3 se registra con los aprobadores del gate.
- Aprueban: UX/UI + PO + Dueño de proceso. "¿Mockup aprobado?": No → ajustar diseño.

### 05 Plan técnico — `plan_tecnico` · Design/Plan → sale con **DoR**
- Arquitectura afectada, tareas y estimación, contratos de API (OpenAPI cuando aplique), datos, riesgos. Decisiones relevantes → `sai.py adr`.
- Antes de cerrar el DoR, revisión cruzada (solo en Claude Code con el paquete `codex` aprobado; en Codex no aplica): `sai.py xreview <ID> --point DoR`.
- Completa DoR: `sai.py dor <ID> dependencias_identificadas tamano_estimado` (G1–G3 ya marcaron el resto). Luego `story move <ID> ready`.

### 06 Desarrollo IA — `desarrollo` · Build
- Sigue el **microciclo de vibecoding controlado** (`vibecoding.md`): contexto → plan → desarrollar → probar → revisar → corregir → presentar evidencia.
- Rama `feature/<ID>`, commits `feat(<ID>): ...`, desarrollo incremental y TDD si hay skill aprobado. Nunca cambies el alcance ni despliegues.
- Toca solo los archivos de la historia. Los prototipos o proyectos de prueba van al lugar de pruebas registrado, nunca sobre el proyecto real.

### 07 Pruebas — `pruebas` · Verify + Review → sale con **G4 Desarrollo**
- Pruebas automatizadas por criterio (AC01..ACnn), revisión de seguridad (SAST/DAST, dependencias), revisión de código (PR), cumplimiento de estándares.
- **Verificación `ligero`**: escribe las pruebas y entrega a la persona los comandos exactos (pruebas, linter, `npm audit`/`pip-audit`) y qué esperar de cada uno. La persona los ejecuta y pega la salida, que se guarda en `scrum-ai/evidence/<ID>/` como evidencia de G4. No repitas la ejecución ni entres en bucles de verificación por tu cuenta.
- **Verificación `completo`**: ejecuta tú las pruebas y los análisis y adjunta la salida.
- Calcula el scorecard preliminar (`quality-gates.md`); un control crítico fallido bloquea G4.
- Antes de pedir G4, revisión cruzada del código (solo en Claude Code con el paquete `codex` aprobado; en Codex no aplica): `sai.py xreview <ID> --point G4 [--base main]`.
- "¿Cumple criterios?": No → corregir e iterar. Aprueban: Líder técnico + QA/Seguridad.

### 08 UAT — `uat` · Verify → sale con **G5 Funcional**
- Prepara plan de UAT con usuarios clave (escenarios y datos reales/anonimizados), registra hallazgos y correcciones, recoge evidencia de aceptación. Aprueban: Usuarios clave + PO.

### 09 Aceptación — `aceptacion` · Review → sale con **DoD + scorecard ≥85**
- Revisión del Product Owner contra criterios de aceptación. Completa DoD (`sai.py dod <ID> aceptacion_completa responsive_verificado documentacion_al_dia`) y el scorecard final (`sai.py score <ID> ...`).
- "¿Aceptación PO?": No → ajustar y volver.

### 10 Release — `release` · Ship → sale con **G6 Entrega**
- Despliegue en producción (lo ejecuta una persona o un pipeline con revisores requeridos), monitoreo y alertas, plan de rollback probado, documentación de despliegue. Antes de pedir G6, revisión cruzada (solo en Claude Code con el paquete `codex` aprobado; en Codex no aplica): `sai.py xreview <ID> --point G6`. Aprueban: PO + Operaciones/TI.

### 11 Retrospectiva — nivel sprint
- `sai.py sprint close` y `sai.py report`; completa `scrum-ai/sprints/sprint-N/retro.md`: qué funcionó, qué mejorar, aprendizajes sobre IA (prompts, skills, MCP, RAG) y acciones para el siguiente sprint.

## Actividades continuas durante el sprint
Daily (15 min) · actualización del tablero · revisión con agentes de IA · control de calidad y seguridad · gestión en GitHub (issues, PR, CI/CD) · documentación y evidencia.

Resultado del sprint: incremento funcional verificable, evidencia de calidad, listo para producción (o siguiente sprint).

## Ejemplo de referencia: US-CONV-001 Consultar convocatorias
- **Como** investigador **quiero** consultar las convocatorias disponibles y filtrar las oportunidades **para** identificar aquellas a las que puedo postularme.
- **Valor**: acceso claro y oportuno a oportunidades de investigación.
- **Reglas**: solo se publican convocatorias autorizadas; los estados se determinan por fechas y decisiones administrativas; una convocatoria cerrada permanece consultable cuando corresponda; los documentos publicados tienen control de versiones.
- **Dependencias**: fuente de datos, aprobación editorial, permisos, diseño de la ficha.
- **Criterios**: AC01 existen convocatorias → listado con título, plazo y estado · AC02 se aplica filtro → solo coincidencias · AC03 no hay resultados → estado vacío útil · AC04 convocatoria vencida → no se presenta como abierta · AC05 error del servidor → mensaje comprensible y reintento · AC06 uso móvil → interfaz operable sin desbordamiento.
- **Evidencia**: ejecución de pruebas AC01–AC06, captura o registro del resultado, versión aprobada, enlace al PR.
