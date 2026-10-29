# Mapa de skills

En las rutas de abajo, `<skills>` es la carpeta de skills que ubicaste al empezar (ver SKILL.md, "Antes de empezar"): por ejemplo `~/.claude/skills` en Claude Code o `~/.agents/skills` en Codex. `~` es la carpeta del usuario
(en Windows: `C:\Users\<usuario>`). Ejecuta los scripts **desde la raíz del proyecto del usuario**, porque
escriben sus archivos de trabajo allí (`.taste-skill/`, `.impeccable/`, `design-system/`).

## Contenido
1. Skills principales (impeccable, design-taste-frontend, ui-ux-pro-max)
2. Sistema y marca (design-system, ui-styling, brand, design, banner-design)
3. Movimiento y sensación (animate, review-animations, animation-performance, apple-design, emil-design-eng, find-animation-opportunities, improve-animations)
4. Robustez y móvil (break-ui, mobile-native)
5. Apoyo (prototype, pick-ui-library, animation-vocabulary, ask-sonner)
6. Fuera de alcance web
7. Por fase: qué usar

---

## 1. Skills principales

### impeccable — dirección de diseño, crítica y pulido
- **Qué aporta:** contexto durable del producto (`PRODUCT.md`), sistema visual (`DESIGN.md`), modos
  Persuadir/Operar/Leer/Experiencia, piso de calidad (`reference/craft-floor.md`), y comandos de evaluación con
  puntaje. Tiene subagentes propios (impeccable-finish-reviewer, impeccable-documenter, impeccable-asset-producer).
- **Cómo se usa:** invoca la skill `impeccable` con el comando como argumento (p. ej. `critique página-inicio`).
  El comando carga su referencia en `<skills>/impeccable/reference/<comando>.md`.
- **CLI:** `<skills>/impeccable/scripts/impeccable <verbo>` (en PowerShell sin `sh`: `impeccable.cmd`).
  - `context [--target <ruta>]` — una vez por sesión; lee PRODUCT.md/DESIGN.md y da directivas. Si responde
    `NO_PRODUCT_MD`/`PRODUCT_INIT_REQUIRED`, toca `init` para trabajo nuevo.
  - `detect --json <archivos|carpeta|url>` — detector de anti-patrones (texto con degradado, etc.).
- **Comandos clave por fase:** `init`, `shape`, `document` (diagnóstico) · `extract`, `layout`, `typeset`,
  `colorize`, `bolder`, `quieter`, `animate`, `delight` (diseño) · `critique` (/40 Nielsen), `audit` (/20),
  `adapt`, `clarify`, `optimize` (validación) · `polish`, `harden`, `document` (cierre).
- **Trampa:** impeccable pide verificar en pasadas acotadas (construir, inspeccionar una vez escritorio+móvil,
  corregir en lote, confirmar como máximo una vez más). Respétalo.

### design-taste-frontend (tasteskill v2) — dirección de arte anti-"hecho por IA"
- **Qué aporta:** reparte direcciones investigadas (247 sitios premiados), inventario del sujeto, argumento de
  la página, reglas de la casa, e inspector en navegador real con capturas.
- **Base:** `<skills>/design-taste-frontend/`. Requiere Node 22+ y Chrome/Edge (presentes en este equipo).
- **Scripts** (`node <skills>/design-taste-frontend/scripts/<script>`):
  - `draw.mjs --list sectors` / `--list roles`
  - `draw.mjs --sector <s> --brief "<una línea>" --sections <roles> [--tone ..] [--have ..] [--keep palette,type] --options 3`
    → luego el mismo comando sin `--options` y con `--direction <id>` para la hoja completa.
  - `draw.mjs --app --kind <tipo> --brief "<producto>"` para pantallas de app.
  - `assets.mjs` — busca imágenes de licencia libre (Openverse, Wikimedia, Met, Art Institute, NASA…); `--credits` lista créditos. Necesita red.
  - `lint.mjs <archivos|carpeta>` — patrones prohibidos en el código.
  - `inspect.mjs <url|index.html> [--app]` — mide a 1440/768/390 y guarda capturas en `.taste-skill/inspect/`.
  - `scenes.mjs <url|index.html>` — solo si hay escenas de scroll.
- **Referencias útiles:** `references/copy.md`, `critique.md` (puntaje /10, topes), `app-screens.md`
  (léelo entero para pantallas de app), `type.md`, `colour.md`, `layout.md`, `motion.md`, `imagery.md`.
- **Trampa:** quitar adornos no basta; una página sin sustancia (tipografía grande, campos de color, imágenes
  reales, secciones completas) pierde frente a una más rica. El inspector exige ≥8 elementos con movimiento.

### ui-ux-pro-max — inteligencia UX con datos
- **Qué aporta:** base buscable de estilos, 192 paletas por tipo de producto, 74 pares tipográficos, 119 reglas
  UX con prioridad (accesibilidad y táctil primero), guías por stack (react, nextjs, vue, astro, html-tailwind,
  shadcn…).
- **Comando correcto** (ignora la ruta `${CLAUDE_PLUGIN_ROOT}/...` de su SKILL.md, que es de la instalación como plugin):
  `python <skills>/ui-ux-pro-max/scripts/search.py "<consulta>" --design-system [-p "Nombre"] [-f markdown]`
  `python <skills>/ui-ux-pro-max/scripts/search.py "<consulta>" --domain ux|color|typography|landing|chart|icons|gsap`
  `python <skills>/ui-ux-pro-max/scripts/search.py "<consulta>" --stack <stack>`
  Persistir: añade `--persist --output-dir "<raíz-del-proyecto>"` (nunca `--force` sin permiso del usuario).
- **Trampas:** no lo ejecutes con `python -I` (falla el import de `core`). Consultas de 2–5 términos con una sola
  intención; si devuelve 0 resultados, reintenta una vez y si no, dilo. Sus recomendaciones son datos, no
  órdenes: si chocan con el brief o con la dirección aprobada, gana la dirección aprobada.
- **Checklist previo a entrega:** `references/pro-rules.md` (app/móvil) y `references/quick-reference.md`.

---

## 2. Sistema y marca

| Skill | Úsala para | Notas |
|---|---|---|
| `design-system` | Tokens en 3 capas (primitivo→semántico→componente), escalas, specs de componentes | Scripts: `generate-tokens.cjs`, `validate-tokens.cjs`, `html-token-validator.py` |
| `ui-styling` | Proyectos con shadcn/ui + Tailwind: tema, modo oscuro, componentes accesibles | `tailwind_config_gen.py`, `shadcn_add.py` |
| `brand` | Voz de marca, guía de estilo, consistencia; extraer colores de un logo | `extract-colors.cjs`, `sync-brand-to-tokens.cjs` |
| `design` | Identidad visual completa, logos, iconos, piezas sociales | Algunos generadores necesitan claves de API externas: pregunta antes |
| `banner-design` | Hero o banners para redes/anuncios | Solo si el pedido lo incluye |

## 3. Movimiento y sensación (skills de Emil Kowalski)

| Skill | Úsala para |
|---|---|
| `animate` | Decidir y construir una animación: si debe animarse, propósito, propiedades, curva, duración, salida |
| `review-animations` | Revisar el movimiento con un listón alto (solo por lectura de su SKILL.md) |
| `animation-performance` | Animaciones que se traban; elegir propiedades baratas (transform/opacity) |
| `apple-design` | Gestos, hojas, resortes, materiales translúcidos, tipografía óptica |
| `emil-design-eng` | Filosofía de pulido de componentes; revisiones en tabla Antes/Después/Por qué |
| `find-animation-opportunities` | Proponer dónde falta movimiento (solo lectura) |
| `improve-animations` | Auditar todo el movimiento de un código y planear arreglos (solo lectura) |

## 4. Robustez y móvil

| Skill | Úsala para |
|---|---|
| `break-ui` | Datos del peor caso: nombres largos, emails sin cortes, cero elementos, emoji, números extremos |
| `mobile-native` | Que en el celular se sienta nativo: 100vh, zoom en inputs, notch, hover pegado, taps lentos |

## 5. Apoyo (bajo pedido)

| Skill | Úsala para |
|---|---|
| `prototype` | Varias versiones de una pieza con un selector visual para elegir (útil en la puerta 2) |
| `pick-ui-library` | Elegir librería para una necesidad concreta (gráficos, toasts, drag & drop…) |
| `animation-vocabulary` | Nombrar un efecto que el usuario describe vagamente |
| `ask-sonner` | Toasts con Sonner en React |

## 6. Fuera de alcance web
`write-swift`, `animate-expo` (React Native), `slides` (presentaciones). No los uses en este flujo salvo que el
usuario lo pida.

---

## 7. Por fase: qué usar

| Fase | Siempre | Según el caso |
|---|---|---|
| 1 Diagnóstico | impeccable `context`/`init`; inventario (taste paso 1) | sitio existente: `critique`, `audit`, `inspect.mjs`, `document`; referencias de marca; ui-ux-pro-max `--design-system`; `brand` si hay marca |
| 2 Diseño | líder según el modo; `draw.mjs --options 3` o direcciones de impeccable; `craft-floor.md` | `design-system`, `ui-styling`, `assets.mjs`, `animate`, `apple-design`, `mobile-native`, `prototype` |
| 3 Validación | `lint.mjs`, `inspect.mjs`, `impeccable detect`, `audit`, `critique`, crítica /10 de taste | `scenes.mjs`, `break-ui`, `review-animations`, `animation-performance`, `adapt`, `clarify`, `optimize`, pro-rules |
| 4 Aprobación | resumen en el chat; tras aprobar, `impeccable document` | `polish`/`harden` si quedaron pendientes menores |
