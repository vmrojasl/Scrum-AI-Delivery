# Manual de usuario — skill `diseno-web-integral`

Guía para usar la skill que lleva un sitio web desde el diagnóstico hasta la aprobación final, coordinando todas
las skills de diseño instaladas. Funciona en **Claude Code** y en **Codex** (OpenAI).

## Contenido

1. [Qué hace](#1-qué-hace)
2. [Requisitos](#2-requisitos)
3. [Instalación](#3-instalación)
4. [Cómo usarla](#4-cómo-usarla)
5. [Las cuatro fases y las tres puertas](#5-las-cuatro-fases-y-las-tres-puertas)
6. [Cómo responder en cada puerta](#6-cómo-responder-en-cada-puerta)
7. [Qué tipo de trabajo hace según tu pedido](#7-qué-tipo-de-trabajo-hace-según-tu-pedido)
8. [Archivos que genera en tu proyecto](#8-archivos-que-genera-en-tu-proyecto)
9. [Criterios de validación](#9-criterios-de-validación)
10. [Trabajar sin interrupciones](#10-trabajar-sin-interrupciones)
11. [Tiempo y costo](#11-tiempo-y-costo)
12. [Solución de problemas](#12-solución-de-problemas)
13. [Preguntas frecuentes](#13-preguntas-frecuentes)

---

## 1. Qué hace

`diseno-web-integral` no diseña por su cuenta: **dirige** a otras skills especializadas y decide cuál usar en
cada momento. Garantiza tres cosas:

- **Orden:** nada se construye sin diagnóstico y nada se entrega sin validación medida.
- **Una sola fuente de verdad:** todas las skills trabajan sobre los mismos archivos del proyecto
  (`PRODUCT.md` y `DESIGN.md`).
- **Tu aprobación explícita:** el trabajo se detiene en tres puntos de control ("puertas") y no avanza hasta
  que respondes.

Skills que coordina:

| Skill | Para qué la usa |
|---|---|
| `impeccable` | Contexto del producto, crítica de usabilidad (/40), auditoría técnica (/20), pulido final, `DESIGN.md` |
| `design-taste-frontend` | Dirección de arte que no parezca plantilla; lint e inspector en navegador real |
| `ui-ux-pro-max` | Datos UX: paletas, tipografías, 119 reglas de usabilidad, guías por tecnología |
| `design-system`, `ui-styling`, `brand` | Tokens de diseño, temas Tailwind/shadcn, identidad de marca |
| `animate`, `review-animations`, `apple-design` | Movimiento con propósito y bien ejecutado |
| `break-ui`, `mobile-native` | Pruebas con datos extremos y buena experiencia en celular |
| Biblioteca de 84 marcas | Referencias del tipo "que se sienta como Stripe / Apple / Linear" |

---

## 2. Requisitos

| Requisito | Para qué | Cómo comprobarlo |
|---|---|---|
| Claude Code o Codex (terminal, VS Code o app de escritorio) | Ejecutar la skill | — |
| Node.js 22 o superior | Scripts de design-taste-frontend | `node -v` |
| Python 3 | Buscador de ui-ux-pro-max | `python --version` |
| Google Chrome, Edge o Chromium | Inspector que mide la página y toma capturas | Que esté instalado |
| Conexión a internet | Buscar imágenes con licencia libre (opcional) | — |

---

## 3. Instalación

Cada programa lee las skills de su propia carpeta. Una skill instalada ahí está disponible en todos tus
proyectos:

| Programa | Carpeta de skills | Subagentes de impeccable |
|---|---|---|
| Claude Code | `C:\Users\<tu-usuario>\.claude\skills\` (Mac/Linux: `~/.claude/skills/`) | `~/.claude/agents/` |
| Codex | `C:\Users\<tu-usuario>\.agents\skills\` (Mac/Linux: `~/.agents/skills/`) | Vienen dentro de la skill (`impeccable/agents/*.toml`) |

Codex también lee `~/.codex/skills/`. La skill busca sus dependencias en cualquiera de estas carpetas.

### 3.1 Instalación automática (recomendada)

El script `scripts/instalar.py` instala la skill orquestadora y todas las que coordina, a partir de los zips de
la carpeta `02 Skills - Diseno UI-UX`. Desde la carpeta `diseno-web-integral`:

```bash
# Para Claude Code y Codex a la vez
python scripts/instalar.py --zips "D:\0. My APPs\2 Third party\02 Skills - Diseno UI-UX" --destino ambos

# Solo para Claude Code / solo para Codex
python scripts/instalar.py --zips "<carpeta de los zips>" --destino claude
python scripts/instalar.py --zips "<carpeta de los zips>" --destino codex
```

| Opción | Qué hace |
|---|---|
| `--forzar` | Reemplaza las skills ya instaladas (por defecto no toca las existentes) |
| `--omitir impeccable,brand` | No toca esas skills aunque uses `--forzar` |
| `--dir-codex ~/.codex/skills` | Instala para Codex en otra carpeta |

Lo que hace el instalador por ti:
- Instala para cada programa la variante correcta de impeccable (la de Claude o la de Codex).
- En Codex, adapta el encabezado de las skills que traen campos solo de Claude. Las que en Claude son "solo
  bajo pedido" (`prototype`, `pick-ui-library`, `review-animations`) quedan en Codex con la misma regla: solo se
  usan si las nombras con `$nombre`.
- Si una skill está en uso por otro programa, no la toca y te avisa. **Cierra Claude Code y Codex antes de
  usar `--forzar`.**

### 3.2 Instalación manual

Si prefieres copiar a mano: copia la carpeta `diseno-web-integral` a la carpeta de skills del programa (tabla de
arriba) y luego copia las dependencias desde los zips:

| Zip | Carpeta de origen dentro del zip | Destino en `~/.claude/skills/` |
|---|---|---|
| `impeccable-main.zip` | Claude: `impeccable-main/.claude/skills/impeccable` · Codex: `impeccable-main/.agents/skills/impeccable` | `impeccable` |
| `impeccable-main.zip` | Solo Claude: `impeccable-main/.claude/agents/*` | `~/.claude/agents/` (subagentes revisores) |
| `taste-skill-main.zip` | `taste-skill-main/skills/taste-skill` | `design-taste-frontend` ⚠️ cambia el nombre |
| `ui-ux-pro-max-skill-main.zip` | `ui-ux-pro-max-skill-main/.claude/skills/<cada una>` | `ui-ux-pro-max`, `design-system`, `brand`, `ui-styling`, `design`, `banner-design`, `slides` |
| `skills-main.zip` | `skills-main/skills/<cada una>` | `animate`, `break-ui`, `mobile-native`, `review-animations`, `apple-design`, `emil-design-eng`, etc. |

En la instalación manual para Codex, quita de cada `SKILL.md` las líneas `argument-hint:` y
`disable-model-invocation:` del encabezado; Codex no las acepta.

La skill orquestadora ya trae dentro la biblioteca de marcas (`references/marcas/`), así que el zip
`awesome-design-md-main.zip` no hace falta instalarlo.

### 3.3 Verificar

- **Claude Code:** abre una sesión nueva y escribe `/`. Deben aparecer `diseno-web-integral`, `impeccable`,
  `design-taste-frontend` y `ui-ux-pro-max`.
- **Codex:** abre una sesión nueva y escribe `/skills` (o `$`). Debe aparecer **Diseño web integral**.

---

## 4. Cómo usarla

Hay dos formas:

**a) Nombrándola**, desde la carpeta de tu proyecto web:

| Programa | Cómo se escribe |
|---|---|
| Claude Code | `/diseno-web-integral rediseña la página de inicio de mi portafolio` |
| Codex | `$diseno-web-integral rediseña la página de inicio de mi portafolio` |

**b) Con lenguaje natural.** La skill se activa sola cuando pides algo de principio a fin, por ejemplo:

- "Necesito la página web de mi tienda de cerámica, hazla completa y que no se vea como plantilla."
- "Haz un diagnóstico de este sitio, rediséñalo y valídalo para aprobarlo."
- "Mi landing se ve hecha con IA, déjala profesional."
- "Ajusta la webpage de mi CV."

**Consejos para un buen pedido:**

- Abre Claude Code **en la carpeta del proyecto**, o indica la ruta del archivo (por ejemplo `sitio/index.html`).
- Da los datos reales: nombre, qué vendes u ofreces, a quién va dirigido, qué debe hacer el visitante, precios,
  fechas, ubicación.
- Di si ya tienes marca (colores, tipografía, logo) y si tienes fotos propias.
- Di la tecnología si la hay (HTML/CSS, React, Next.js, Tailwind…). Si no, la skill la detecta o te pregunta.

---

## 5. Las cuatro fases y las tres puertas

```
 Fase 1 DIAGNÓSTICO ──► 🚪 Puerta 1 ──► Fase 2a DIRECCIÓN ──► 🚪 Puerta 2 ──► Fase 2b CONSTRUCCIÓN
                                                                                   │
                         ◄── Fase 4 APROBACIÓN ◄── 🚪 Puerta 3 ◄── Fase 3 VALIDACIÓN ◄┘
```

### Fase 1 — Diagnóstico

Entender qué es real antes de proponer nada.

- Lee o crea `PRODUCT.md`: propósito, audiencia, acción principal, tono, restricciones.
- Hace un **inventario del sujeto**: de 8 a 12 cosas que son solo tuyas y de ningún competidor (tu nombre, tu
  lugar, tus números, tus rituales). De ahí sale la idea del diseño.
- Si ya existe un sitio, **lo mide**: usabilidad (/40), calidad técnica (/20) y capturas a 1440, 768 y 390 px.

**Recibes:** lo que entendió, los problemas medidos, oportunidades, el inventario y los supuestos.

### 🚪 Puerta 1 — ¿Está bien entendido el problema?

### Fase 2a — Dirección

- Decide el **modo** de la página: *Persuadir* (landing, ventas), *Operar* (app, dashboard), *Leer* (documentación,
  artículos) o *Experiencia* (portafolio, galería).
- Prepara **2 o 3 direcciones de diseño distintas**, cada una con su idea, composición, tipografía, paleta,
  imágenes y movimiento.

**Recibes:** las direcciones A, B y C y una recomendación.

### 🚪 Puerta 2 — Elige la dirección

### Fase 2b — Construcción

Define los tokens de diseño, construye la página, busca imágenes con licencia libre si no tienes propias y
añade el movimiento. El contenido provisional queda marcado.

### Fase 3 — Validación

Mide la página con herramientas, no con opiniones, y corrige como máximo en dos rondas (ver [sección 9](#9-criterios-de-validación)).

### 🚪 Puerta 3 — Aprobación final

**Recibes:** qué se construyó, dónde están los archivos, la tabla de validación, las decisiones tomadas y lo que
hay que reemplazar antes de publicar.

### Fase 4 — Cierre

Si apruebas, genera `DESIGN.md` con el sistema que realmente se entregó, para que los cambios futuros partan
de ahí.

---

## 6. Cómo responder en cada puerta

| Puerta | Respuestas posibles | Ejemplo |
|---|---|---|
| 1 Diagnóstico | Confirmar o corregir | "Sí, pero el público son empresas, no personas." |
| 2 Dirección | Elegir, combinar o pedir ajustes | "La B, con la paleta de la C." |
| 3 Final | **aprobado** · **aprobado con cambios** · **rechazado** | "Aprobado con cambios: el botón más grande y quita la sección de FAQ." |

Qué pasa después de la puerta 3:

- **Aprobado:** se genera `DESIGN.md` y se cierra.
- **Aprobado con cambios:** aplica los cambios, vuelve a medir solo lo afectado y te presenta otra vez la puerta 3.
- **Rechazado:** identifica dónde estuvo el problema y vuelve a esa fase, no al principio. Si se entendió mal
  el problema, vuelve al diagnóstico; si no te gusta el estilo, a la dirección; si falla la ejecución, a la
  construcción.

> La skill nunca da por aprobado algo que tú no aprobaste.

---

## 7. Qué tipo de trabajo hace según tu pedido

| Si pides… | La skill hace… |
|---|---|
| Un sitio o página nueva | Las 4 fases completas |
| Un rediseño | Las 4 fases, con comparación antes/después |
| Mejorar sin cambiar la identidad | Un diagnóstico corto, refinamiento, validación y aprobación |
| "Revisa / audita mi sitio" | Solo diagnóstico y validación, entrega el informe y te ofrece seguir |
| Una pantalla de app (dashboard, admin) | Las 4 fases por la ruta "Operar" |

---

## 8. Archivos que genera en tu proyecto

| Archivo o carpeta | Qué es | ¿Conservar? |
|---|---|---|
| `PRODUCT.md` | Contexto del producto: propósito, audiencia, tono | Sí |
| `DESIGN.md` | Sistema visual aprobado: colores, tipografía, componentes | Sí |
| `index.html`, `assets/` (o los archivos de tu stack) | La página | Sí |
| `assets/credits.json` | Créditos y licencias de las imágenes encontradas | Sí, si usas esas imágenes |
| `.taste-skill/` | Dirección de arte y capturas del inspector | Opcional (puedes añadirla a `.gitignore`) |
| `.impeccable/` | Historial de críticas y auditorías | Opcional |
| `design-system/` | Sistema de ui-ux-pro-max, si se guardó | Opcional |

---

## 9. Criterios de validación

La página se presenta para aprobación cuando cumple estos umbrales:

| Criterio | Herramienta | Umbral |
|---|---|---|
| Patrones genéricos o "de IA" en el código | `lint.mjs` | 0 FAIL |
| Medidas en navegador real (1440 / 768 / 390 px) | `inspect.mjs` | 0 FAIL |
| Calidad técnica (accesibilidad, rendimiento, responsive) | `impeccable audit` | ≥ 16/20, sin problemas P0/P1 |
| Usabilidad (10 heurísticas de Nielsen) | `impeccable critique` | ≥ 28/40, sin P0 |
| Calidad visual (criterio de jurado) | crítica de design-taste-frontend | ≥ 7.5/10 |
| Accesibilidad | auditoría + reglas UX | Contraste ≥ 4.5:1, foco visible, teclado, textos alternativos |
| Celular | reglas UX + mobile-native | Botones ≥ 44 px, sin scroll horizontal |
| Datos extremos | `break-ui` | Nada se rompe |
| Prueba de 5 segundos | revisión de capturas | Se entiende qué es y qué hacer |
| Contenido | revisión | Sin lorem ipsum ni cifras inventadas |

Cada criterio se reporta como ✅ cumple, ❌ no cumple, ⚪ no medido o ➖ no aplica. Si una herramienta no pudo
ejecutarse, el criterio aparece como **no medido**, nunca como aprobado. Puedes pedir otros umbrales, por
ejemplo: "exige 32/40 en usabilidad".

---

## 10. Trabajar sin interrupciones

Si no puedes atender las puertas, dilo en el pedido:

> "Hoy no voy a poder responderte, avanza tú y me cuentas al final."

La skill tomará cada decisión por su cuenta, la dejará escrita con su razón y entregará todo como
**pendiente de aprobación**. Al volver, respondes la puerta 3 como siempre.

---

## 11. Tiempo y costo

Valores medidos en las pruebas de la skill (octubre de 2026):

| Tipo de pedido | Tiempo aproximado | Tokens aproximados |
|---|---|---|
| Landing page nueva, de principio a fin | ~33 min | ~325 mil |
| Rediseño de un sitio existente | ~29 min | ~277 mil |

La skill tarda entre 1,5 y 4 veces más que pedir el diseño sin ella, a cambio de diagnóstico, varias
direcciones, validación medida y aprobación. En las pruebas cumplió el 100 % de los criterios, frente al 65 %
sin la skill.

Para ahorrar:

- Pide solo lo que necesitas ("solo audita", "solo mejora la tipografía").
- En modo interactivo, responder en las puertas evita construir una dirección que luego descartas.

---

## 12. Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| La skill no aparece al escribir `/` (Claude) o en `/skills` (Codex) | No está en la carpeta de skills de ese programa, o la sesión es anterior a la instalación | Revisa la carpeta (sección 3) y abre una sesión nueva |
| Codex no carga una skill o la marca como inválida | Su encabezado trae campos solo de Claude o un `:` sin comillas en la descripción | Reinstala con `instalar.py --destino codex --forzar`, que la adapta |
| El instalador dice "en uso por otro programa" | Claude Code o Codex tienen abierto un archivo de esa skill | Ciérralos y vuelve a ejecutarlo; la versión anterior queda intacta |
| Faltan dependencias | Solo se instaló la skill orquestadora | La skill te dice cuáles faltan; instálalas con `instalar.py` |
| Las críticas no usan subagentes | Tu entorno no permite lanzarlos | La skill hace las evaluaciones en secuencia y lo indica en el informe |
| "Context loading did not run" | Falló el lanzador de impeccable | La skill sigue leyendo PRODUCT.md/DESIGN.md directamente. En PowerShell se usa `impeccable.cmd` |
| El inspector no genera capturas | Falta Chrome/Edge o Node < 22 | Instala Chrome y actualiza Node |
| `ModuleNotFoundError: No module named 'core'` | Se ejecutó ui-ux-pro-max con `python -I` | Ejecútalo sin `-I`: `python ~/.claude/skills/ui-ux-pro-max/scripts/search.py "…"` |
| ui-ux-pro-max devuelve 0 resultados | La consulta es muy amplia | Usa 2 a 5 palabras y añade `--domain` (ux, color, typography, landing) |
| No encuentra imágenes | Sin internet | La skill usa ilustraciones o elementos tipográficos y lo indica en el informe |
| Algo queda por debajo del umbral | Se agotaron las dos rondas de corrección | Se reporta con honestidad; puedes pedir otra ronda en la puerta 3 |

---

## 13. Preguntas frecuentes

**¿Puedo usar una sola skill sin pasar por todo el flujo?**
Sí. Invócala directamente, por ejemplo `/impeccable audit` o `/design-taste-frontend`. Usa
`diseno-web-integral` cuando el trabajo abarque más de una fase.

**¿Copia el diseño de otras marcas?**
No. Las 84 referencias de marca son interpretaciones que sirven de inspiración ("que se sienta como…"), no
plantillas para copiar.

**¿Respeta mi marca actual?**
Sí. Si das colores, tipografías o logo, se mantienen. Tu brief tiene prioridad sobre el gusto de la skill.

**¿Inventa fotos o cifras?**
No. Usa tus imágenes o imágenes con licencia libre acreditadas. Todo contenido provisional queda listado para
que lo reemplaces antes de publicar.

**¿Funciona con React, Next.js, Vue o Tailwind?**
Sí. Detecta la tecnología del proyecto y aplica las guías correspondientes.

**¿Funciona igual en Claude Code y en Codex?**
Sí: las mismas fases, puertas, criterios y archivos. Solo cambian la carpeta de instalación y la forma de
nombrarla (`/` en Claude, `$` en Codex). Las pruebas de tiempo y costo de la sección 11 se hicieron en Claude Code.

**¿Dónde quedó la copia de respaldo?**
En la carpeta del proyecto `02 Skills - Diseno UI-UX/diseno-web-integral/`. Ni Claude Code ni Codex la leen
desde ahí; es solo para reinstalar (ver [sección 3](#3-instalación)).
