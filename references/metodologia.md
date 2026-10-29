# Metodología Scrum-AI Delivery — panorama

Scrum + ingeniería asistida por IA + Spec-Driven Development + Quality Gates. Metodología para desarrollar el Ecosistema de Investigación y, en general, cualquier producto digital, plataforma, servicio o iniciativa institucional.

## Contenido
1. Por qué existe
2. Las tres dimensiones
3. Los cinco bloques
4. Arquitectura: seis etapas del requisito al release
5. Roadmap S0–S6
6. Roles, RACI y gobierno
7. Portafolio de referencia

## 1. Por qué existe
| Antes | Con Scrum-AI Delivery |
|---|---|
| Requisitos poco estructurados (historias ambiguas, criterios incompletos) | Ciclos cortos: sprints con entregas funcionales y revisables |
| Diseños que cambian durante el desarrollo | Diseño antes del código: flujos, mockups y criterios claros |
| Vibecoding sin controles (código sin trazabilidad ni validación) | IA controlada: Agent Skills y vibecoding con reglas, pruebas y revisión |
| Retrabajo y demoras | Menos retrabajo: iteraciones guiadas por especificaciones y feedback temprano |
| Aprobación incierta | Aprobación con evidencia: Quality Gates, UAT y pruebas |

Resultado: más claridad, mejor calidad y decisiones de aprobación basadas en evidencia.

## 2. Las tres dimensiones (ninguna funciona sola)
1. **Scrum — organiza el trabajo**: backlog priorizado, sprints, reviews y retrospectivas.
2. **Diseño orientado a especificaciones — define qué construir antes de programar**: requisitos, flujos y BPMN, mockups y criterios de aceptación.
3. **Agent Skills + vibecoding — acelera la ejecución bajo controles**: implementación asistida por IA, pruebas y validación, ajustes iterativos.

Resultado: incrementos funcionales verificables.

## 3. Los cinco bloques
| Bloque | Qué se hace | Resultado del bloque |
|---|---|---|
| 1. Visión y estrategia | Propósito, usuarios, problema y oportunidad, objetivos estratégicos, alcance y criterios | Visión clara, objetivos medibles y ruta alineada |
| 2. Modelo operativo | Flujo Descubrir → Diseñar → Construir → Verificar → Aprobar → Entregar alrededor del Product Backlog | Flujo claro, roles definidos y quality gates que ordenan cada sprint |
| 3. Diseño y desarrollo asistido por IA | Prompt y especificación, wireframes y flujos, diseño de componentes, generación de código, pruebas, iteración | Diseños claros, desarrollo acelerado y evidencia para iterar con control |
| 4. Implementación y control | Código, QA, CI/CD, trazabilidad, quality gates, seguridad, PR, release | Implementación confiable, validación continua y control del avance |
| 5. Puesta en marcha | Despliegue, monitoreo, soporte y adopción, mejora continua | Solución desplegada, adoptada, monitoreada y lista para evolucionar |

Para el Bloque 1 usa la plantilla `scrum-ai/vision/vision.md` (creada por `init`). Conduce una entrevista breve: una pregunta a la vez sobre propósito, usuarios, problema, objetivos medibles (indicador, línea base, meta, plazo), alcance dentro/fuera del MVP y stakeholders. Si hay un skill aprobado tipo `interview-me` en Define, úsalo.

## 4. Arquitectura: un flujo integrado del requisito al release
| # | Etapa | Contenido |
|---|---|---|
| 01 | Descubrir — requisitos y reglas | Historias de usuario, necesidades y alcance, reglas de negocio, criterios de aceptación |
| 02 | Diseñar — flujos y mockups | Diagramas de proceso (BPMN/Mermaid), arquitectura de información, mockups y prototipos, contratos técnicos (APIs) |
| 03 | Construir — código con IA | Agentes de IA especializados, desarrollo incremental, buenas prácticas y revisión de código, integración continua |
| 04 | Verificar — QA y seguridad | Pruebas automatizadas, revisión de seguridad, evaluación de calidad, evidencia de pruebas |
| 05 | Aprobar — UAT y aceptación | Validación con usuarios, ajustes, criterios de aceptación, aprobación del incremento |
| 06 | Entregar — release y monitoreo | Despliegue en producción, monitoreo y alertas, documentación, medición de impacto |

Retroalimentación continua (aprendizajes, métricas, nuevas oportunidades) hacia el Product Backlog priorizado.

## 5. Roadmap de implementación para cualquier proyecto (S0–S6)
Fases secuenciales e iterativas; `sai.py phase --set` impide saltarlas sin `--force`.

| Fase | Objetivo | Entregable | Dependencia principal |
|---|---|---|---|
| S0 Descubrimiento y estrategia | Entender el problema, validar la necesidad y definir la visión | Documento de visión, alcance inicial, caso de negocio | Alineación de stakeholders y disponibilidad de recursos |
| S1 Planificación | Definir requerimientos, priorizar, estimar y planear | Backlog priorizado, roadmap detallado, criterios de éxito | Resultados de S0 y validación de stakeholders |
| S2 Diseño | Diseñar la solución técnica y la experiencia de usuario | Arquitectura técnica, flujos y prototipos (UX/UI), diseño de datos y APIs | Requerimientos y prioridades definidas en S1 |
| S3 Desarrollo | Construir de forma incremental y controlada | Código funcional, integraciones, build desplegable | Diseños aprobados y entornos habilitados |
| S4 Pruebas y validación | Verificar calidad, seguridad y cumplimiento | Pruebas unitarias y de integración, resultados de QA, validación de seguridad | Código estable y datos de prueba |
| S5 Despliegue | Liberar en producción de forma segura | Despliegue, plan de monitoreo, comunicación a usuarios | Validación completa en S4 |
| S6 Operación y mejora continua | Monitorear, medir y evolucionar | Indicadores de uso y desempeño, plan de mejoras, nuevas versiones | Solución en producción y retroalimentación |

Nota: el roadmap es la vista macro del proyecto; dentro de S1–S5 el trabajo real ocurre en sprints de 2 semanas donde cada historia recorre su propio ciclo (ver `ciclo-sprint.md`). Cambia de fase solo con aprobación del PO (`--approver`).

## 6. Roles, RACI y gobierno
| Rol | Responsabilidades |
|---|---|
| Product Owner | Define prioridades, aprueba entregables, acepta el incremento |
| Scrum Master | Facilita el proceso, gestiona el sprint, elimina bloqueos |
| Responsable técnico | Define arquitectura, revisa código y seguridad, valida estándares |
| Dueños de proceso | Aportan conocimiento de negocio, validan reglas y excepciones, aseguran adopción |
| UX/UI | Diseña experiencias, crea mockups y prototipos, valida consistencia de diseño |
| QA / Seguridad | Diseña y ejecuta pruebas, valida seguridad y calidad, emite evidencia |
| Usuarios clave | Validan en UAT, dan retroalimentación, confirman valor |
| Agentes de IA | Ejecutan tareas de desarrollo; generan código, pruebas y documentación; **no aprueban entregables** |

RACI simplificado (R ejecuta · A aprueba · C consulta · I informa): ver `assets/templates/roles-raci.md`.

Gobierno de la metodología: criterios y estándares, gestión de riesgos, control de calidad y seguridad, métricas y mejora continua.

## 7. Portafolio de referencia (Ecosistema de Investigación)
ResearchHUB (portal institucional de la investigación, investigación formativa) · ResearchOS (gestión de la investigación aplicada y transferencia) · CRIS (información científica institucional) · CRAI (recursos para el aprendizaje y la investigación) · Convocatorias (oportunidades y financiación) · Servicios (marketplace de servicios) · Integraciones (conexión con sistemas externos y datos).

Ejemplo canónico de historia: `US-CONV-001 Consultar convocatorias` (ver `ciclo-sprint.md`).
