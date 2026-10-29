---
name: scrum-ai-delivery
description: Conduce paso a paso proyectos con la metodología Scrum-AI Delivery (Scrum + IA + Spec-Driven Development + Quality Gates), de la visión y el Sprint 0 al release, con historias de usuario, flujos, mockups, vibecoding controlado, gates G1–G6 con aprobación humana, DoR/DoD, scorecard ≥85/100 y trazabilidad en GitHub. Funciona en Claude Code y en Codex, con perfiles (esencial, estándar, completo) que ajustan el gasto de tokens a la complejidad del proyecto y aprobaciones agrupadas. Úsalo cuando el usuario mencione Scrum-AI, Sprint 0, quality gates, historias con criterios de aceptación, DoR/DoD, backlog, roadmap S0–S6, vibecoding controlado o el Ecosistema de Investigación, o pida planear, especificar, construir, verificar o liberar software "con la metodología", aunque no la nombre.
---

# Scrum-AI Delivery

El agente (Claude Code o Codex) facilita y ejecuta la metodología: produce los artefactos, usa las capacidades aprobadas y **se detiene en cada punto de aprobación hasta que una persona decide con evidencia**. `SKILL_DIR` es la carpeta de este skill. En Codex, todos los comandos llevan `--harness codex`: `python SKILL_DIR/scripts/sai.py --harness codex <comando>`.

## Principios

1. **Los agentes ejecutan, no aprueban.** Nunca registres una aprobación que una persona no haya escrito en la conversación, ni uses el nombre de un agente como aprobador (el script lo rechaza).
2. **Nada avanza sin evidencia.** Un "se ve bien" no aprueba. Una plantilla sin completar no es evidencia (el script la rechaza).
3. **Diseño antes del código.** Historia → flujo → mockup → plan técnico → código, salvo las etapas que el perfil omite. Sin DoR no hay desarrollo.
4. **Ejecuta solo lo que el perfil fija.** Los skills, etapas, nivel de detalle y verificación dependen del perfil (`esencial`, `estandar`, `completo`). Ir más allá requiere un pedido del usuario.
5. **Pruebas en su lugar.** Con verificación `ligero` (la de los perfiles `esencial` y `estandar`), tú escribes las pruebas y la persona las ejecuta. Nunca uses el proyecto real como banco de pruebas: probar no autoriza a rehacerlo.
6. **Agrupa las aprobaciones, no las saltes.** Prepara todo un tramo y pide una sola decisión (ver «Bucle»). G1, G4, G6, DoR, DoD, el scorecard y la aprobación humana nunca se omiten.

## Presupuesto de tokens (siempre)

- La fuente de verdad es la salida de `sai.py` (`status`, `story show`, `cap for-phase`). No abras `state.json` ni `capabilities.json`.
- Lee **una** referencia, la del paso en curso, y solo la sección que necesitas. No leas `MANUAL.md` (es para personas) ni releas archivos que ya tienes en contexto.
- En el chat, enlaza los artefactos (`scrum-ai/...`) en vez de pegarlos, y muestra diffs en vez de archivos completos.
- Respuestas en 3 partes: una línea de contexto, el resultado y la decisión o el siguiente paso. Sin repetir lo ya dicho ni resumir los skills usados.
- Invoca un skill externo solo si `cap for-phase` lo lista. Si dos skills hacen lo mismo, usa uno.
- Reúne las preguntas al usuario en una sola tanda.

## Arranque

1. `python SKILL_DIR/scripts/sai.py status`
   - **Si no hay proyecto**, pregunta en una sola tanda: nombre; si ya hay código (`existente`) o no (`nuevo`); si usarán GitHub; dónde se harán las pruebas (`sandbox` con ruta, `rama` o `proyecto`; recomienda `sandbox` o `rama` si ya hay código); la complejidad del proyecto, para recomendar un perfil; y si quien conversa es quien aprueba (nombre y rol). Luego:
     `sai.py init --name "<n>" --mode nuevo|existente [--github] --tests-in <lugar> [--tests-path <ruta>] --profile esencial|estandar|completo [--approver "Nombre (rol)"]`
   - Si `status` dice «Pruebas: sin definir», pregunta el lugar y regístralo con `sai.py config --tests-in ...` antes de cualquier prueba.
   - Si dice que el registro es de una versión anterior: `sai.py cap sync`.
2. Si faltan paquetes que el perfil va a usar, `sai.py cap install` muestra el plan. Ejecuta `--yes` solo con autorización. `codex login` lo ejecuta la persona. Un paquete `pendiente_revision` necesita aprobación humana antes de usarse (ver `references/capacidades-externas.md`). Con perfil `esencial` (skills `ninguno`), omite este paso.
3. Di en 2 líneas dónde está el proyecto y qué propones, y hazlo.

## Mapa: lee solo lo que el paso necesita

| Situación | Referencia | Fase |
|---|---|---|
| Perfiles, flags, verificación, lugar de pruebas | `references/perfiles.md` | — |
| Visión, roadmap S0–S6, roles | `references/metodologia.md` | Define |
| Sprint 0 y auditoría de código existente | `references/sprint0.md` | Define / Plan |
| Qué hacer en cada estado de la historia | `references/ciclo-sprint.md` (solo la sección del paso) | según estado |
| Gates, aprobación agrupada, DoR/DoD, scorecard | `references/quality-gates.md` | Verify / Review |
| Programar: microciclo y reglas | `references/vibecoding.md` | Build |
| GitHub: issues, ramas, PR, Actions | `references/github.md` | Plan / Ship |
| Paquetes de skills, entornos, Codex, MCP, RAG | `references/capacidades-externas.md` | todas |

## Bucle por historia

```
backlog → especificacion ─G1→ flujo ─G2→ mockup ─G3→ plan_tecnico ─DoR→ ready → desarrollo
        → pruebas ─G4→ uat ─G5→ aceptacion ─DoD+scorecard→ release ─G6→ done
```

`flujo`, `mockup` y `uat` pueden estar omitidas por el perfil o con `story skip`. Al aprobar un gate, completar el DoR o aprobar DoD y scorecard, el script **avanza la historia solo**. `story move` solo se usa para iniciar (`backlog → especificacion`), para `ready → desarrollo → pruebas` y para retroceder.

**Cuatro puntos de aprobación por historia, no seis** (detalle en `quality-gates.md` → «Aprobar rápido»):

| Punto | Prepara antes de pedir | Registra |
|---|---|---|
| Planeación | Fichas de todas las historias del sprint | `gate US-1,US-2 G1 --decision aprobado` |
| Diseño | Flujo y mockup (y la ficha, si G1 no se aprobó en planeación) + plan técnico | `gate US-1 G2,G3 --decision aprobado` → `dor US-1 dependencias_identificadas tamano_estimado` |
| Entrega técnica | Código, pruebas, revisión, scorecard preliminar | `gate US-1 G4 --decision aprobado --evidence <PR/salida>` |
| Cierre | UAT, DoD, scorecard final, plan de release | `gate US-1 G5 ...` · `dod` · `score` · `gate US-1 G6 ...` |

En cada punto:
1. **Contexto mínimo:** la ficha y los artefactos previos de la historia, más `CONSTRAINTS.md`. Usa RAG solo si la regla depende de normativa (`rag.py query-all "<q>" --phase <Fase>`) y cita la fuente.
2. **Capacidades:** `sai.py cap for-phase <Fase>` y usa solo lo que lista.
3. **Artefactos** con las plantillas que copia el script. Si el usuario pide `--todo` o el perfil es `esencial`, prepara de una vez todos los artefactos del punto.
4. **Autoverificación:** una pasada contra el checklist del gate, honesta.
5. **Revisión cruzada de Codex**, solo con verificación `completo` o a pedido: `sai.py xreview <ID> --point G1|DoR|G4|G6`.
6. **Pide la decisión** en el formato corto (abajo) y **detente**.
7. **Registra** lo que la persona dijo. Si el aprobador está registrado (`config --approver`), basta su «aprobado»; si aprueba otra persona, usa `--approver "Nombre (rol)"`. Si rechaza, corrige y vuelve al paso 3.

### Formato de solicitud (máximo unas 10 líneas)

```
## Aprobación — <G2+G3 Diseño> · <US-1>
Evidencia: <rutas o enlaces, sin pegar contenido>
Autoverificación: ✔ … · ✖ <pendiente honesto>
Codex: <hallazgos y acción · o "no aplica">
Riesgos: <si hay>
Aprueba: <roles> → "aprobado" o "rechazado: <motivo>"
```

## Comandos

```
sai.py status | config [--profile P --skills S --skip-stages E --design D --detail D --verify V --tests-in L --approver A]
sai.py init --name N --mode nuevo|existente [--github] --tests-in L [--tests-path R] --profile P [--approver A]
sai.py phase [--set S1]          · sprint0 [item]  · audit <comp> --state 1-5 --value 1-5
sai.py sprint start --goal "…" | close  · report
sai.py story add <ID> "<t>" [--skip E] | move <ID> <estado> [--reason] | skip <ID> --skip E | show <ID> | list
sai.py gate <ID[,ID…]> <G#[,G#…]> --decision aprobado|rechazado [--approver A] [--evidence R] [--notes] [--no-advance]
sai.py dor|dod <ID> <items>      · score <ID> --func --tec --ux --pruebas --seg --doc [controles]  · adr "<t>"
sai.py xreview <ID> --point G1|DoR|G4|G6   · cap for-phase <Fase> [--all] | install | approve | add-skill|add-mcp|add-rag
```

Si alguien con autoridad decide omitir un control obligatorio, explica el riesgo y registra la excepción con su nombre y la justificación en `--notes`.
