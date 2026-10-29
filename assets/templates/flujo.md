# Flujo — {{ID}} {{TITULO}}

Dos miradas para modelar cada funcionalidad: **BPMN 2.0** (proceso de negocio: actores, decisiones, excepciones, permisos, rutas alternativas) y **Mermaid / diagrama de estados** (comportamiento de interfaz: navegación, estados de pantalla, respuestas del sistema).

## 1. Proceso de negocio (BPMN 2.0 expresado en Mermaid, un carril por actor)

```mermaid
flowchart LR
  subgraph Gestor
    A((Inicio)) --> B[Registra elemento] --> C[Completa ficha y documentos] --> D{¿Datos completos?}
    D -- No --> C
  end
  subgraph Aprobador
    D -- Sí --> E{¿Publicación autorizada?}
    E -- No --> F[Devuelve con observaciones] --> C
  end
  subgraph Sistema
    E -- Sí --> G[Publica]
  end
  subgraph Usuario
    G --> H[Consulta catálogo] --> I[Aplica filtros y abre ficha] --> J{¿Vigente?}
    J -- Sí --> K[Visualiza opción de acción] --> Z((Fin))
    J -- No --> L[Consulta cerrada] --> Z
  end
```
_(Si el equipo usa una herramienta BPMN — Camunda Modeler, bpmn.io — adjunte el .bpmn en `scrum-ai/design/`.)_

## 2. Comportamiento de interfaz (estados)

```mermaid
stateDiagram-v2
  [*] --> Cargando
  Cargando --> Listado: datos OK
  Cargando --> Error: falla servidor
  Error --> Cargando: reintentar
  Listado --> Vacio: sin resultados
  Listado --> Ficha: seleccionar
  Ficha --> SoloConsulta: sin permiso
  Ficha --> Detalle: con permiso
  Detalle --> Cerrada: no vigente
  Detalle --> Accion: vigente (CTA)
```

## 3. Actores y permisos
| Actor | Puede | No puede |
|---|---|---|

## 4. Escenarios
| # | Escenario | Tipo (principal/alterno/excepción) | Criterio AC relacionado |
|---|---|---|---|

## Checklist G2 (Flujo)
- [ ] Flujo de proceso completo
- [ ] Actores y permisos
- [ ] Escenarios principales y excepciones
- [ ] Coherencia con requisitos (cada AC aparece en algún camino)
