# Plantillas de entrega

Formatos para lo que se muestra en el chat al cerrar cada fase. Mantén cada entrega escaneable: el usuario
decide en la puerta con esto, así que lo importante va primero y lo técnico al final.

## §1 Diagnóstico (Puerta 1)

```markdown
## Diagnóstico — <proyecto>

**Lo que entendí:** <una o dos frases: qué es, para quién, qué debe lograr la página>
**Modo:** <Persuadir | Operar | Leer | Experiencia> · **Stack:** <detectado o "por definir">

### Estado actual  (solo si hay sitio existente)
| Medida | Resultado |
|---|---|
| Usabilidad (Nielsen) | 22/40 |
| Calidad técnica | 11/20 · 2 P0, 4 P1 |
| Inspector (1440/768/390) | 6 FAIL, 4 WARN |

### Los problemas que más importan
1. <problema> — <evidencia: captura, medida o línea de código> — <por qué le importa al visitante>
2. …

### Oportunidades
- <qué podría hacer este sitio que hoy no hace>

### Inventario del sujeto
<8–12 elementos propios del cliente>

### Supuestos
- <lo que asumí y no está confirmado>

**¿Está bien entendido el problema? Confírmame o corrígeme antes de pasar a las propuestas de dirección.**
```

## §2 Direcciones (Puerta 2)

```markdown
## Propuestas de dirección

### A · <nombre>
- **Idea:** <una frase atada a un elemento del inventario>
- **Composición:** <cómo se organiza la página>
- **Tipografía:** <familias y escala>
- **Paleta:** `#…` fondo · `#…` texto · `#…` acento
- **Imágenes:** <de dónde salen>
- **Movimiento característico:** <uno>
- **Por qué encaja:** <qué del diagnóstico resuelve>

### B · …
### C · …

**Mi recomendación:** <letra> porque <razón en una frase>.
**¿Cuál eliges? Puedes combinar ("A con la paleta de C") o pedir ajustes.**
```

## §3 Validación

```markdown
## Validación

| # | Criterio | Antes | Ahora | Umbral | Estado |
|---|---|---|---|---|---|
| 5 | Calidad técnica | 11/20 | 18/20 | ≥16, 0 P0/P1 | ✅ |
| 6 | Usabilidad | 22/40 | 31/40 | ≥28 | ✅ |
| 7 | Calidad visual | — | 7.8/10 | ≥7.5 | ✅ |
| … |

**Rondas de corrección:** <n> · **Capturas:** `.taste-skill/inspect/…`
**Pendiente / por debajo del umbral:** <lista honesta, o "nada">
```

## §4 Aprobación final (Puerta 3)

```markdown
## Listo para tu aprobación — <proyecto>

**Qué se entrega:** <archivos y rutas> · **Cómo verlo:** <abrir index.html | comando>
**Dirección aplicada:** <nombre> — <idea>

<tabla resumida de validación (§3)>

**Decisiones que tomé:** <lista corta>
**Reemplazar antes de publicar:** <textos, imágenes o datos de muestra; créditos de imágenes encontradas>

Responde **aprobado**, **aprobado con cambios** (y cuáles) o **rechazado** (y por qué).
```

## Modo sin interrupciones

Si trabajas sin poder esperar respuesta, usa las mismas plantillas, cambia la pregunta final de cada puerta por
"**Decisión tomada:** … porque …" y titula la entrega final **Pendiente de aprobación**.
