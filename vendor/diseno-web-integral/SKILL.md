---
name: diseno-web-integral
description: 'Orquesta el ciclo completo de diseño web (diagnóstico, diseño, validación medida y aprobación del usuario) coordinando las skills de diseño instaladas (impeccable, design-taste-frontend, ui-ux-pro-max, design-system, animate, break-ui, mobile-native y otras) y 84 referencias de marca. Úsala cuando el usuario quiera diseñar, rediseñar, auditar o renovar de principio a fin un sitio web, landing, portal, portafolio, CV web, tienda o pantalla de app, o pida diagnóstico, propuesta, validación o aprobación del diseño, "dejarlo profesional" o "que no se vea hecho por IA", aunque no nombre ninguna skill. También en inglés: end-to-end web design, redesign this site, design sign-off. Prefiérela a una sola skill de diseño cuando la tarea abarque más de una fase; para un ajuste puntual de una sola fase usa directamente la skill especializada.'
---

# Diseño web integral: diagnóstico → diseño → validación → aprobación

Esta skill no diseña por sí misma: **dirige** a las skills especializadas, decide cuál toca en cada momento y
detiene el trabajo en puertas de aprobación donde el usuario decide. Su valor está en tres cosas que ninguna
skill suelta hace sola:

1. **Orden.** Nada se construye sin diagnóstico ni se entrega sin validación medida.
2. **Una sola fuente de verdad.** Todas las skills leen y escriben sobre los mismos archivos del proyecto
   (`PRODUCT.md`, `DESIGN.md`), así que las decisiones de una fase llegan a la siguiente.
3. **Aprobación explícita del usuario.** Las puertas son en el chat; el diseño no avanza a la siguiente fase
   sin un "aprobado" (o un cambio pedido) del usuario.

Conversa con el usuario en su idioma (normalmente español). Las skills que coordinas están en inglés; tradúcele
sus resultados, no le pegues informes crudos.

## Antes de empezar

Esta skill funciona igual en **Claude Code** y en **Codex**. Lo único que cambia entre ambos es dónde están
las skills y cómo se cargan; resuélvelo así antes de la fase 1:

1. **Ubica `<skills>`**, la carpeta donde están instaladas las skills que coordinas. Normalmente es la carpeta
   **padre de esta skill** (el instalador las pone juntas). Si ahí no está `impeccable`, busca en este orden:
   `.claude/skills/` y `.agents/skills/` del proyecto, luego `~/.claude/skills/`, `~/.agents/skills/` y
   `$CODEX_HOME/skills/` (o `~/.codex/skills/`). Usa la primera que contenga `impeccable/SKILL.md`. En el resto
   de esta skill y sus referencias, `<skills>/<nombre>` significa esa ruta.
2. **Carga cada skill leyendo su archivo.** La forma que funciona en ambos entornos es leer
   `<skills>/<nombre>/SKILL.md` y seguir sus instrucciones. En Claude Code también puedes invocarla con la
   herramienta Skill; en Codex el usuario puede nombrarla con `$<nombre>`. Las que tienen
   `disable-model-invocation` (`review-animations`, `prototype`, `pick-ui-library`) se usan siempre leyendo el
   archivo.
3. **Rutas internas de cada skill.** Cuando una skill diga `.claude/skills/<x>/...`, `.agents/skills/<x>/...`
   o `${CLAUDE_PLUGIN_ROOT}/...`, tradúcelo a `<skills>/<x>/...`.
4. **Subagentes.** Si tu entorno permite lanzar subagentes, úsalos para las evaluaciones independientes (por
   ejemplo, las dos evaluaciones de `impeccable critique`): un evaluador que no construyó la página es más
   honesto. Si no los tienes, hazlas en secuencia y dilo en el informe.
5. **Shell.** En Windows con PowerShell, el lanzador de impeccable es `impeccable.cmd`; con bash o en
   Mac/Linux, `impeccable`.

Después:
- Lee `references/mapa-skills.md`: cada skill, cuándo usarla, su comando exacto y sus trampas conocidas
  (por ejemplo, la ruta del buscador de ui-ux-pro-max difiere de la que dice su propio SKILL.md).
- No cargues todas las skills a la vez. Carga cada una en la fase en que se usa; el contexto es caro y cada
  skill trae su propio flujo detallado.
- Si falta alguna skill necesaria, dile al usuario cuál y cómo instalarla (`MANUAL.md` §3 o
  `scripts/instalar.py`), y sigue con las que sí están marcando lo que no se pudo medir.

## Elige el alcance

Ajusta el recorrido al pedido; no todas las tareas necesitan las cuatro fases completas.

| Pedido | Recorrido |
|---|---|
| Sitio o página nueva | Fases 1 → 4 completas |
| Rediseño de un sitio existente | Fases 1 → 4; el diagnóstico mide lo actual para comparar el antes/después |
| Mejorar una página sin cambiar su identidad | Diagnóstico corto → refinamiento (impeccable) → validación → aprobación |
| "Revisa / audita mi sitio" | Solo fase 1 y fase 3 sobre lo existente; entrega el informe y ofrece seguir |
| Pantalla de app (dashboard, admin, ajustes) | Igual que sitio nuevo, pero por la ruta "Operar" (ver fase 2) |

Si el pedido es ambiguo, decide, dile al usuario en una línea qué entendiste y sigue. Pregunta solo cuando falte
un dato que bloquee el trabajo (nombre del producto, qué debe lograr la página, si existe marca).

---

## Fase 1 — Diagnóstico

Objetivo: entender qué es real antes de proponer nada. El diagnóstico define el problema; un diseño sin él
resuelve el problema de la categoría, no el de este cliente.

1. **Contexto del proyecto.** Ejecuta `impeccable context` (ver mapa) desde la raíz del proyecto. Si falta
   `PRODUCT.md`, corre `impeccable init` para capturarlo: propósito, audiencia, la acción principal que la
   página debe provocar, tono, restricciones. Detecta el stack (package.json, etc.); no asumas uno.
2. **Inventario del sujeto** (paso 1 de design-taste-frontend): 8–12 cosas que pertenecen a este cliente y a
   ningún competidor (su nombre y lo que significa, su lugar, sus números, su restricción, sus materiales, sus
   rituales). De aquí sale la idea del diseño en la fase 2. Anota también qué imágenes existen de verdad.
3. **Si ya hay un sitio**, mídelo antes de opinar:
   - `impeccable critique <objetivo>` → puntaje Nielsen /40, problemas P0–P3.
   - `impeccable audit <objetivo>` → accesibilidad, rendimiento, theming, responsive: puntaje /20.
   - `node .../design-taste-frontend/scripts/inspect.mjs <url|index.html>` → medidas y capturas a 1440/768/390.
   - `impeccable document` si no hay `DESIGN.md`, para registrar el sistema visual actual.
   Mira las capturas tú mismo; un problema visible en una captura es real aunque el código diga otra cosa.
4. **Referencias.** Si el usuario menciona marcas o "que se parezca a X", busca en
   `references/marcas/INDICE.md` y abre solo esos archivos. Son interpretaciones para inspirar, no para copiar.
5. **Datos UX del sector**: `ui-ux-pro-max` con `--design-system` usando el tipo de producto y sector; úsalo como
   segunda opinión con datos (patrones, reglas UX, anti-patrones del sector).

**Entrega de la fase** (formato en `references/plantillas.md` §1): resumen del brief, hallazgos medidos con su
puntaje, los 3–5 problemas que más importan, oportunidades, y el inventario.

### 🚪 Puerta 1 — Aprobar el diagnóstico
Presenta el diagnóstico y pregunta si está bien entendido el problema y si hay algo que corregir o añadir.
No pases a diseñar hasta que el usuario lo confirme: un malentendido aquí se paga en todas las fases siguientes.

---

## Fase 2 — Diseño

### 2a. Dirección (antes de escribir código)

Decide el **modo** de la superficie (definición de impeccable): *Persuadir* (landing, marketing, precios),
*Operar* (app, dashboard, admin), *Leer* (docs, artículos), *Experiencia* (portafolio, galería).
El modo decide quién lidera la construcción:

| Modo | Lidera | Consultores |
|---|---|---|
| Persuadir / Experiencia | `design-taste-frontend` (su "run") | ui-ux-pro-max (datos), impeccable craft-floor, animate |
| Operar | `impeccable` (new-work + operate) con `design-taste-frontend` `--app` para el reparto de estilo | ui-ux-pro-max (stack + UX), ui-styling si es shadcn/Tailwind |
| Leer | `impeccable` (mode-read) | ui-ux-pro-max (tipografía) |
| Refinar algo existente | `impeccable` (el refinamiento preserva identidad) | el resto según el problema |

Un solo líder evita que dos skills impongan dos estéticas distintas sobre la misma página. Los consultores
aportan datos y controles, no una segunda dirección de arte.

Prepara **2–3 direcciones genuinamente distintas**:
- Para páginas: escribe el argumento (claims → secciones, `references/copy.md` de design-taste-frontend) y
  reparte direcciones con `draw.mjs --options 3`.
- Contrasta cada dirección con el inventario del diagnóstico y con el sistema sugerido por ui-ux-pro-max.
- Si hay marca existente, pásala con `--keep palette,type` y respétala: el brief gana sobre el gusto.

Para cada dirección muestra: nombre, la idea (una frase atada a algo del inventario), composición, tipografía,
paleta (hex), tratamiento de imágenes, movimiento característico, y por qué encaja (formato en plantillas §2).

### 🚪 Puerta 2 — Aprobar la dirección
Pide al usuario que elija una dirección (o combine/ajuste). Construir sin esta elección suele terminar en
rehacer la página entera, que es lo más caro de todo el ciclo.

### 2b. Sistema y construcción

1. **Tokens.** Con la dirección aprobada, define tokens en tres capas (primitivo → semántico → componente,
   skill `design-system`). Si el stack es shadcn/Tailwind, usa `ui-styling` para el tema.
2. **Construye** siguiendo el flujo del líder elegido (para design-taste-frontend: pasos 4–6 y 9 de su run;
   para impeccable: new-work o el comando de refinamiento). Lee `impeccable/reference/craft-floor.md` antes de
   la primera edición de UI: trae el piso de calidad y las prohibiciones absolutas.
3. **Imágenes reales**: las del cliente o las encontradas con `assets.mjs` (licencias libres, con crédito).
   Nunca inventes fotos de producto ni números de vanidad.
4. **Movimiento**: `animate` para decisiones de movimiento (propósito, curva, duración, reduced-motion);
   `apple-design` si hay gestos, hojas o resortes; `mobile-native` si se usará mucho en celular.
5. **Contenido**: textos reales y específicos. Todo contenido de muestra queda marcado para reemplazar.

---

## Fase 3 — Validación

Objetivo: demostrar con medidas, no con opinión, que el diseño está listo. Lee
`references/criterios-validacion.md`: contiene los umbrales de aprobación, qué herramienta mide cada uno y el
orden de ejecución.

Resumen del procedimiento:
1. **Controles automáticos**: `lint.mjs` + `inspect.mjs` (y `scenes.mjs` si hay escenas de scroll) de
   design-taste-frontend; `impeccable detect` sobre los archivos de UI.
2. **Evaluaciones de experto**: `impeccable audit`, `impeccable critique`, y la crítica /10 de
   design-taste-frontend (`references/critique.md`) mirando las capturas.
3. **Casos extremos**: `break-ui` con datos del peor caso en los componentes con datos variables.
4. **Movimiento**: revisa contra `review-animations` (y `animation-performance` si algo se traba).
5. **Corrige en lotes acotados**: junta todo lo encontrado, arregla en un solo lote, vuelve a medir. Máximo dos
   rondas de corrección; si algo sigue por debajo del umbral, no sigas puliendo en círculo: repórtalo con
   honestidad en la puerta 3. El pulido sin fin gasta el dinero del usuario y rara vez mejora lo que el
   usuario sí nota.
6. **Pasada final**: `impeccable polish` y, si va a producción, `impeccable harden` (errores, i18n, bordes).

**Entrega de la fase** (plantillas §3): tabla de criterios con valor medido, umbral y ✅/❌, comparación
antes/después si hubo diagnóstico de un sitio existente, rutas de las capturas, y pendientes.

No afirmes un control que no ejecutaste. Si una herramienta falló (sin Chrome, sin red), dilo y marca ese
criterio como "no medido", no como aprobado.

---

## Fase 4 — Aprobación

### 🚪 Puerta 3 — Aprobación final
Presenta en el chat (plantillas §4):
- qué se construyó y dónde están los archivos;
- la tabla de validación y lo que todavía queda por debajo del umbral;
- decisiones tomadas y supuestos;
- contenido o imágenes provisionales que hay que reemplazar antes de publicar;
- cómo verlo (ruta a `index.html` o comando del servidor de desarrollo).

Pide una respuesta explícita: **aprobado**, **aprobado con cambios** (lista) o **rechazado** (motivo).

- **Aprobado** → ejecuta `impeccable document` para que `DESIGN.md` refleje el sistema realmente entregado
  (no el planeado). Así futuras iteraciones parten del diseño aprobado. Cierra con un resumen breve.
- **Aprobado con cambios** → aplica los cambios, vuelve a medir solo lo afectado y presenta de nuevo la puerta 3.
- **Rechazado** → identifica a qué fase pertenece el motivo (malentendido del problema → fase 1; dirección →
  puerta 2; ejecución → 2b) y vuelve allí, no al principio por defecto.

## Cuando el usuario no puede responder en las puertas

Si se te pidió trabajar sin interrupciones (o corres de forma no interactiva), no te detengas: en cada puerta
escribe la decisión que tomaste y por qué, elige la dirección más fuerte frente al inventario, sigue hasta el
final, y presenta todo como **pendiente de aprobación** en el resumen. Nunca declares aprobado algo que el
usuario no aprobó.

## Archivos de esta skill

- `references/mapa-skills.md` — catálogo de skills, comandos exactos y trampas. Léelo al empezar.
- `references/criterios-validacion.md` — umbrales de aprobación y orden de la validación. Léelo en la fase 3.
- `references/plantillas.md` — formatos de las entregas de cada fase y de las puertas.
- `references/marcas/INDICE.md` — índice de 84 referencias de marca; abre solo la que necesites.
