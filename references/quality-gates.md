# Calidad y control en cada etapa

Ninguna funcionalidad avanza sin cumplir los criterios de calidad, con validación humana y evidencia.

## Las seis puertas de aprobación
| Gate | Qué se verifica | Quién aprueba | Evidencia esperada |
|---|---|---|---|
| **G1 Requisitos** — historia, reglas y criterios | Historia completa · reglas de negocio · criterios de aceptación · dependencias y alcance | Product Owner + Dueño de proceso | Historia en el backlog · criterios de aceptación · trazabilidad de requisitos |
| **G2 Flujo** — BPMN/Mermaid con actores y escenarios | Flujo de proceso · actores y permisos · escenarios principales y excepciones · coherencia con requisitos | Dueño de proceso + Arquitecto de procesos | Diagrama BPMN/Mermaid · descripción de escenarios · validación del proceso |
| **G3 Diseño** — mockup, estados y UX | Mockup de alta fidelidad · estados (carga, vacío, error) · responsive · accesibilidad y consistencia | UX/UI + Product Owner + Dueño de proceso | Mockups aprobados · prototipo navegable · guía de estilos (si aplica) |
| **G4 Desarrollo** — código, pruebas y revisión técnica | Implementación completa · pruebas automatizadas · revisión de código (PR) · estándares · seguridad (SAST/DAST) | Líder técnico + QA/Seguridad | PR y revisión · resultados de pruebas · informe de seguridad · evidencia de buenas prácticas |
| **G5 Funcional** — UAT con evidencia | Funcionalidad según criterios · pruebas con usuarios clave · datos y escenarios reales · corrección de hallazgos · evidencia de aceptación | Usuarios clave + Product Owner | Plan y resultados de UAT · registro de hallazgos · evidencia de aceptación · checklist de criterios |
| **G6 Entrega** — release, seguridad, observabilidad, rollback | Despliegue en producción · monitoreo · observabilidad y alertas · plan de rollback · documentación operativa | Product Owner + Operaciones/TI | Release en producción · monitoreo y alertas activos · rollback probado · documentación de despliegue |

`sai.py gate <G#>` imprime esta definición. Antes de pedir aprobación, recorre el checklist y marca honestamente lo que no se cumple: es preferible presentar un pendiente que ocultarlo, porque el gate existe justamente para que la persona decida con información completa.

**Nivel de verificación.** Los gates son los mismos en `ligero` y `completo`; cambia quién ejecuta las pruebas. En `ligero` (por defecto), la evidencia de pruebas, linters y análisis de dependencias es la salida que pega la persona después de correr los comandos que propone el agente. Si falta, el ítem se presenta como «pendiente de ejecución manual» y no como cumplido. La revisión cruzada de Codex, en `ligero`, solo se adjunta si se pidió.

## Aprobar rápido (menos esperas, mismo control)

Cada aprobación es una espera humana. Para reducirlas, agrúpalas sin saltar ningún control.

**1. Puntos de aprobación agrupada.** Prepara todos los artefactos de un tramo y pide **una sola decisión**:

| Punto | Qué se prepara antes de pedir | Comando al aprobar |
|---|---|---|
| **Planeación** (inicio de sprint) | Fichas de todas las historias comprometidas | `gate US-1,US-2,US-3 G1 --decision aprobado` |
| **Diseño** (por historia o por épica) | Ficha, flujo y mockup juntos | `gate US-1 G1,G2,G3 --decision aprobado` (o `G2,G3` si G1 ya se aprobó en planeación) |
| **Entrega técnica** | Código, pruebas, revisión y scorecard preliminar | `gate US-1 G4 ...` |
| **Cierre** | UAT (si aplica), DoD, scorecard final y plan de release | `gate US-1 G5 ...` → `dod` / `score` → `gate US-1 G6 ...` |

En el perfil `completo`, si el proceso exige aprobadores distintos por gate, agrupa solo los gates con los mismos aprobadores.

**2. Aprobador registrado.** Si quien conversa es quien aprueba, regístralo una vez: `sai.py config --approver "Nombre (rol)"`. Desde entonces su «aprobado» basta y `gate` y `phase` usan ese nombre. Si aprueba otra persona, o si el gate exige un rol que el registrado no tiene, usa `--approver` explícito. Nunca registres una aprobación que la persona no haya escrito en la conversación.

**3. Lo que el script hace solo:**
- Al aprobar un gate, la historia avanza al siguiente estado. Al completar DoR, pasa a `ready`; con DoD y scorecard aprobados, pasa a `release`. Usa `--no-advance` para evitarlo.
- G1, G2 y G3 toman como evidencia la ficha, el flujo o el mockup si no pasas `--evidence`. Una plantilla sin completar nunca se acepta como evidencia.
- En una decisión agrupada, si un gate falla (falta evidencia, etapa omitida), se registra lo anterior y se reporta qué faltó.

**4. Formato corto de solicitud.** Usa máximo unas 10 líneas y enlaza los artefactos en vez de pegarlos:

```
## Aprobación — <G1+G2+G3 Diseño> · <US-1, US-2>
Evidencia: scrum-ai/backlog/US-1.md · scrum-ai/design/US-1/ · …
Autoverificación: ✔ criterios verificables · ✔ estados de UI · ✖ <pendiente honesto>
Codex: <hallazgos y acción · o "no aplica">
Riesgos: <si hay>
Aprueba: <roles> → responda "aprobado" o "rechazado: <motivo>"
```

## Definition of Ready / Definition of Done
- **DoR (entrada a desarrollo)**: historia definida · reglas de negocio · criterios de aceptación · flujo aprobado · mockup validado · dependencias identificadas · tamaño estimado.
- **DoD (salida a release o cierre)**: aceptación completa · PR revisado · pruebas OK · seguridad validada · responsive verificado · UAT completado · documentación al día.

Los gates marcan automáticamente parte de DoR/DoD (G1→historia/reglas/criterios; G2→flujo; G3→mockup; G4→PR/pruebas/seguridad; G5→UAT). El resto se marca con `sai.py dor|dod <ID> <items>`.

## Scorecard de calidad (ponderado)
| Criterio | Qué evalúa | Peso |
|---|---|---|
| Funcionalidad | Cumple los requisitos y el valor esperado | 30% |
| Calidad técnica | Arquitectura, código, estándares | 20% |
| Diseño / UX | Usabilidad, accesibilidad, consistencia | 15% |
| Pruebas | Cobertura, casos, resultados | 15% |
| Seguridad | Análisis de vulnerabilidades, cumplimiento | 15% |
| Documentación | Técnica, funcional y de usuario | 5% |

Puntaje = Σ peso × calificación/5. **Umbral de aprobación: ≥ 85/100 y ninguna dimensión menor a 3/5.**
Ejemplo del documento: 4,4,4,5,4,4 → 24+16+12+15+12+4 = **83/100 → No aprobada** (no alcanza el umbral).

### Controles críticos (binarios)
Si alguno falla, la entrega se bloquea automáticamente, sin importar el puntaje:
- Vulnerabilidad crítica (CVSS 9.0–10) → `--critical-vuln`
- Prueba obligatoria fallida (unitarias, integración, seguridad) → `--failed-test`
- Criterio obligatorio de la metodología incumplido → `--mandatory-missing`

### Cómo calificar con justicia
Justifica cada calificación con evidencia concreta (resultado de pruebas, informe de seguridad, revisión de UX). Claude puede **proponer** las calificaciones; el evaluador humano las confirma (`--evaluator "Nombre (rol)"`). Calcula: `sai.py score <ID> --func N --tec N --ux N --pruebas N --seg N --doc N [controles]`.
