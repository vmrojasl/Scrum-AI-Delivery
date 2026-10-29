# AGENTS.md — {{PROYECTO}}

> Guía para agentes de IA que trabajan en este repositorio. Metodología: **Scrum-AI Delivery**.
> Versión inicial: {{FECHA}}. Se aprueba como entregable del Sprint 0 (Product Owner + Responsable técnico).

## Principio clave
Los agentes de IA **ejecutan, no aprueban**. Toda decisión crítica (priorización, diseño, aprobación, release) es humana.

## Reglas no negociables
1. El agente **no puede cambiar el alcance**: implementa solo lo que dice la historia aprobada (G1–G3) y su plan técnico.
2. El agente **no puede saltarse pruebas**: toda entrega trae pruebas ejecutadas y su resultado. Con verificación `ligero`, el agente las escribe y la persona las ejecuta.
   Las pruebas se hacen solo en el lugar registrado (`python sai.py config`); nunca se rehace el proyecto para probar.
3. El agente **no puede desplegar por iniciativa propia**: el release requiere G6 aprobado por personas.
4. Toda decisión crítica requiere validación humana registrada (`python sai.py gate ...`).

## Microciclo de vibecoding controlado
1. Preparar contexto (historia, criterios, flujo, mockup, CONSTRAINTS.md, ADRs)
2. Generar plan (tareas pequeñas, archivos a tocar, pruebas a escribir)
3. Desarrollar (incremental, en rama `feature/<ID-historia>`)
4. Probar (unitarias/integración; cubrir criterios AC01..ACnn)
5. Revisar (autorrevisión + skill de code-review/security si está aprobado)
6. Corregir
7. Presentar evidencia (PR con enlaces a pruebas, capturas, reporte de seguridad)

## Convenciones del repositorio
- Ramas: `feature/<ID>`, `fix/<ID>`, `chore/<tema>`
- Commits: `<tipo>(<ID>): descripción` — ej. `feat(US-CONV-001): filtro de convocatorias`
- Cada PR enlaza su historia y su evidencia en `scrum-ai/evidence/<ID>/`
- Stack, comandos de build/test y estructura: _(completar en Sprint 0)_

## Capacidades externas
Solo se usan skills, MCP y fuentes RAG con estado `aprobado` en `scrum-ai/capabilities.json`.
Consultar: `python sai.py cap for-phase <Fase>`.
