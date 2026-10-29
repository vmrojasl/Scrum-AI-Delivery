# Perfil, flags de ahorro, verificación y lugar de las pruebas

Lee esto al iniciar un proyecto, al cambiar la configuración o cuando el usuario use un flag.

## Perfiles

El perfil se elige en `init` y se cambia con `sai.py config`. Define cuánto de la metodología y de los skills externos se ejecuta.

| Perfil | Para qué proyectos | Skills externos | Etapas omitidas | Sprint 0 | Diseño | Detalle | Verificación |
|---|---|---|---|---|---|---|---|
| `esencial` | Prototipo, herramienta interna pequeña, proyecto personal o de aprendizaje | `ninguno` | `flujo`, `uat` | Mínimo: visión, DoR/DoD, AGENTS, CONSTRAINTS, backlog S1 (y diagnóstico si hay código) | `basico` | `breve` | `ligero` |
| `estandar` (por defecto) | Proyecto típico de equipo | `principal` | ninguna | Completo | `basico` | `breve` | `ligero` |
| `completo` | Institucional, crítico, con datos sensibles o normativa | `todos` | ninguna | Completo | `integral` | `completo` | `completo` |

Cómo recomendar: si hay datos personales, normativa, varios equipos o producción institucional, recomienda `completo`. Si es para aprender o probar una idea, `esencial`. En cualquier otro caso, `estandar`.

## Flags de ajuste

Se usan en `init` o `config`. `--profile` reinicia los valores y los demás flags lo ajustan después.

| Flag | Valores | Efecto |
|---|---|---|
| `--skills` | `ninguno` · `principal` · `todos` | Qué skills de los paquetes integrados lista `cap for-phase`. Los skills de terceros, MCP y RAG que registró el equipo se listan siempre |
| `--skip-stages` | `flujo,mockup,uat` · `ninguno` | Etapas omitidas por defecto en las historias nuevas: su gate (G2, G3 o G5) no aplica y su ítem de DoR/DoD queda `no_aplica` |
| `--design` | `basico` · `integral` | `basico`: wireframe y mockup simples en HTML o Markdown con los estados obligatorios. `integral`: el ciclo completo de `diseno-web-integral` |
| `--detail` | `breve` · `completo` | Extensión de artefactos y respuestas |
| `--verify` | `ligero` · `completo` | Ver «Nivel de verificación» |
| `--approver` | `"Nombre (rol)"` · `ninguno` | Persona que aprueba en el chat (ver `quality-gates.md` → «Aprobar rápido») |

**Por historia:** `story add <ID> "<título>" --skip mockup` o `story skip <ID> --skip flujo,uat|ninguno`. Las etapas en curso o ya superadas no cambian.

**Nunca se omiten:** G1, G4, G6, DoR, DoD, el scorecard ≥85, los controles críticos y la aprobación humana.

## Detalle `breve`

- Artefactos con solo las secciones de la plantilla y sin texto de relleno. Las tablas son preferibles a la prosa.
- Flujo solo en Mermaid. BPMN, únicamente si hay más de un actor con decisiones.
- ADR solo para decisiones difíciles de revertir.
- Ficha de historia con 4 a 6 criterios de aceptación: caso feliz, variante, vacío, error, borde y móvil, si aplican.

## Flags en la conversación

Valen solo para el paso en curso y no cambian `state.json`:

| Flag | Efecto |
|---|---|
| `--esencial` · `--completo` | Trata ese paso con ese perfil |
| `--sin-skills` | No invoques skills externos |
| `--con <skill>` | Usa ese skill aunque el perfil lo omita |
| `--breve` · `--detallado` | Ajusta la extensión de la respuesta |
| `--verificar` | Ejecuta tú las pruebas de ese paso |
| `--xreview` | Corre la revisión cruzada de Codex de ese paso |
| `--todo` | Prepara de una vez todos los artefactos hasta el siguiente punto de aprobación agrupada |

Si el usuario quiere que el cambio sea permanente, usa `sai.py config`.

## Nivel de verificación

| | `ligero` | `completo` |
|---|---|---|
| Pruebas | El agente **escribe** las pruebas por criterio (AC01..ACnn) y entrega los comandos exactos; **la persona los ejecuta** y pega la salida, que es la evidencia | El agente las ejecuta y adjunta la salida |
| Verify / Review | Solo los skills principales, en una pasada. `ecc:verification-loop` y los complementarios (E2E, navegador, regresión, rendimiento), solo a pedido | Principales y complementarios cuando el caso lo pida |
| Revisión cruzada de Codex | Solo a pedido | Automática en G1, DoR, G4 y G6 |
| Autoverificación | Checklist breve, sin reintentos en bucle | Checklist completo, iterando hasta cumplir |

En ambos niveles se mantiene la regla de no declarar «pasa» sin evidencia. Si la persona no entrega la salida, el ítem se presenta como «pendiente de ejecución manual».

## Lugar de las pruebas

Se registra con `--tests-in sandbox|rama|proyecto [--tests-path <ruta>]` y se respeta siempre:

- `sandbox`: pruebas exploratorias, prototipos y proyectos de prueba **solo** en la carpeta indicada.
- `rama`: rama de pruebas (por defecto `pruebas/<ID>`). Nada se fusiona sin el gate correspondiente.
- `proyecto`: solo archivos de prueba y los cambios mínimos de la historia en curso.

**Probar no autoriza a rehacer el proyecto.** Si una prueba parece exigir reescribir, reestructurar o regenerar código fuera del alcance de la historia, detente, explica qué tocarías y por qué, y pide autorización. Si `status` dice «sin definir», pregunta el lugar antes de escribir la primera prueba.
