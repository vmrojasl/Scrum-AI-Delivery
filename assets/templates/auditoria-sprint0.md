# Sprint 0 — Auditoría del código existente · {{PROYECTO}}

> Conocer antes de construir. Objetivo: diagnóstico claro y accionable que alimente el backlog real. Fecha: {{FECHA}}

## 1. Inventario del código existente
_Árbol del repositorio con semáforo por carpeta (🟢 bien · 🟡 mejorable · 🔴 crítico)._

```
proyecto/
```

## 2. Evaluación por componente
Escala 1–5 en cada criterio. Semáforo por celda.

| Componente | Estado (1–5) | Calidad | Mantenibilidad | Seguridad | Cobertura pruebas | Dependencias | Riesgo | Acción |
|---|---|---|---|---|---|---|---|---|
| Arquitectura | | | | | | | | |
| Frontend | | | | | | | | |
| Backend | | | | | | | | |
| Datos | | | | | | | | |
| Componentes | | | | | | | | |
| Dependencias | | | | | | | | |
| Seguridad | | | | | | | | |
| Pruebas | | | | | | | | |
| CI/CD | | | | | | | | |
| Documentación | | | | | | | | |
| Deuda técnica | | | | | | | | |

Registrar cada fila también con `python sai.py audit <componente> --state N --value N [--action ...]`.

## 3. Criterios de decisión (valor de negocio × estado técnico)
| | Estado técnico bueno | Estado técnico malo |
|---|---|---|
| **Valor alto** | Conservar (usar como base) | Refactorizar (mejorar y modernizar) |
| **Valor bajo** | Retirar (eliminar) | Reconstruir (desarrollar de nuevo) |

## 4. Resultado de la auditoría
Distribución: Conservar __% · Refactorizar __% · Reconstruir __% · Retirar __%

## 5. Hallazgos (riesgos, oportunidades, recomendaciones)
| # | Hallazgo | Tipo | Severidad | Recomendación | Historia/épica generada |
|---|---|---|---|---|---|

## Salida principal: backlog real del proyecto
- Componentes a conservar:
- Componentes a refactorizar:
- Componentes a reconstruir:
- Elementos a retirar:
- Nuevas historias técnicas y funcionales:
