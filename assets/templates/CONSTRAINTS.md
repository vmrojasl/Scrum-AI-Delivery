# CONSTRAINTS.md — {{PROYECTO}}

> Restricciones, políticas y límites operativos para personas y agentes. Entregable del Sprint 0. Fecha: {{FECHA}}

## Técnicas
- Lenguajes / frameworks permitidos: _(completar)_
- Versiones mínimas y dependencias aprobadas: _(completar)_
- Arquitectura objetivo: ver ADRs en `scrum-ai/adr/`
- Integraciones permitidas (APIs, sistemas institucionales): _(completar)_

## Seguridad y datos
- Sin secretos en el código ni en prompts; usar variables de entorno / gestor de secretos.
- Datos personales: cumplir Ley 1581 de 2012 (Habeas Data) y políticas institucionales; usar datos anonimizados en pruebas.
- Vulnerabilidades de severidad crítica (CVSS 9.0–10) **bloquean** la entrega.
- Análisis SAST/DAST obligatorio antes de G4.

## Calidad
- Umbral de aprobación: scorecard **≥ 85/100** y ninguna dimensión < 3/5.
- Controles críticos binarios: vulnerabilidad crítica, prueba obligatoria fallida, criterio obligatorio incumplido.
- Estados obligatorios de UI: carga, vacío, error, permisos, confirmación, responsive.
- Accesibilidad: _(nivel objetivo, p. ej. WCAG 2.1 AA)_

## Límites de los agentes de IA
- No modificar alcance, no omitir pruebas, no desplegar, no aprobar gates.
- Pruebas y prototipos solo en el lugar registrado (`python sai.py config`): _(sandbox en … / rama … / proyecto)_. Probar no autoriza a rehacer ni reestructurar el proyecto.
- Nivel de verificación: _(ligero: pruebas manuales · completo: el agente las ejecuta)_.
- No instalar dependencias nuevas sin registrarlo en el plan técnico.
- No usar skills/MCP/RAG que no estén `aprobado` en `scrum-ai/capabilities.json`.
- No enviar datos institucionales sensibles a servicios externos no autorizados.

## Operación
- Ambientes: _(dev / pruebas / producción)_
- Ventanas de despliegue y responsables de Operaciones/TI: _(completar)_
- Plan de rollback obligatorio para cada release.
