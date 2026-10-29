# Criterios de validación

Estos umbrales deciden si el diseño puede presentarse para aprobación final. Vienen de las propias skills
(impeccable, design-taste-frontend, ui-ux-pro-max) para que la medida sea la misma que esas skills usan.
Un criterio sin medir se reporta como **no medido**, nunca como aprobado.

## Tabla de criterios

| # | Criterio | Herramienta | Umbral para aprobar | Bloqueante |
|---|---|---|---|---|
| 1 | Patrones prohibidos en código | `lint.mjs` | 0 FAIL | Sí |
| 2 | Medidas en navegador real a 1440 / 768 / 390 | `inspect.mjs` (`--app` en pantallas de app) | 0 FAIL; cada WARN defendible en una frase | Sí |
| 3 | Escenas de scroll (si existen) | `scenes.mjs` | sin problemas en escritorio, móvil y reduced-motion | Sí |
| 4 | Anti-patrones de diseño | `impeccable detect --json` | 0 hallazgos de severidad alta; el resto justificado | No |
| 5 | Calidad técnica (a11y, rendimiento, theming, responsive) | `impeccable audit` | ≥ 16/20 y 0 problemas P0 o P1 | Sí |
| 6 | Usabilidad (10 heurísticas de Nielsen) | `impeccable critique` | ≥ 28/40 (o ≥ 70 % del máximo aplicable si hay n/a) y 0 P0 | Sí |
| 7 | Calidad visual a ojos de un jurado | crítica de design-taste-frontend (`references/critique.md`) sobre las capturas | ≥ 7.5/10 | Sí para páginas Persuadir/Experiencia |
| 8 | Accesibilidad básica | audit + ui-ux-pro-max (prioridad 1) | contraste ≥ 4.5:1 en texto, foco visible, navegación por teclado, alt en imágenes, `prefers-reduced-motion` | Sí |
| 9 | Táctil y móvil | ui-ux-pro-max (prioridad 2) + `mobile-native` | objetivos ≥ 44×44 px, sin scroll horizontal a 390 px, inputs sin zoom | Sí |
| 10 | Datos del peor caso | `break-ui` en componentes con datos variables | nada se rompe o cada rotura tiene arreglo aplicado | No (sí si hay formularios/listas) |
| 11 | Movimiento | `review-animations`; inspector cuenta elementos en movimiento | solo transform/opacity, reduced-motion respetado; ≥ 8 elementos animados en páginas | No |
| 12 | Prueba de los 5 segundos | tu lectura de la captura del primer pantallazo | un desconocido sabe qué es y qué hacer | Sí |
| 13 | Contenido | revisión manual | sin lorem ipsum ni números inventados; provisionales listados | Sí |

Los umbrales de 5 y 6 son el piso de esta skill: impeccable dice que la mayoría de interfaces reales puntúan
20–32/40, así que 28 exige estar en la parte alta sin pedir perfección. Si el usuario fija otros umbrales,
usa los suyos.

## Orden de ejecución

El orden va de lo barato y objetivo a lo caro y de juicio, para no gastar una crítica en algo que el linter
habría marcado:

1. `lint.mjs` → corrige FAIL.
2. `inspect.mjs` (+ `scenes.mjs`) y `impeccable detect` → corrige FAIL.
3. Abre **todas** las capturas que liste el inspector (no solo la primera pantalla).
4. `impeccable audit` y `impeccable critique`; crítica /10 de taste sobre las capturas.
5. `break-ui` y revisión de movimiento donde aplique.
6. Junta todo en una lista, corrige en **un lote**, vuelve a correr 2 → 4 una vez.
7. Si aún falla algo tras la segunda ronda, detente y repórtalo; no hagas una tercera ronda sin preguntar.

## Cómo reportar

Para cada criterio: valor medido, umbral, estado (✅ / ❌ / ⚪ no medido / ➖ no aplica) y, si falló, la causa
y lo que haría falta. Si hubo diagnóstico de un sitio existente, añade la columna **Antes** para mostrar la
mejora con los mismos instrumentos.
