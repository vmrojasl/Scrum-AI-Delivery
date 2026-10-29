# Manual de usuario — Scrum-AI Delivery

**Del requisito al release, con evidencia en cada paso.**

Este manual explica cómo usar el skill **Scrum-AI Delivery** con Claude (Claude Code) o con Codex para llevar un proyecto de software con la metodología Scrum-AI Delivery: desde la visión y el Sprint 0 hasta el release, con *quality gates*, aprobación humana y trazabilidad.

| | |
|---|---|
| **Para quién es** | Product Owners, Scrum Masters, responsables técnicos, desarrolladores, QA y seguridad, UX/UI, dueños de proceso y usuarios clave que participen en un proyecto con la metodología |
| **Qué necesita saber** | Nada de programación para las secciones 1, 2, 5, 7 y 8. Las secciones de instalación, comandos y GitHub asumen que sabe abrir una terminal |
| **Repositorio** | <https://github.com/vmrojasl/Scrum-AI-Delivery> |
| **Sitio** | <https://vmrojasl.github.io/Scrum-AI-Delivery/> |

## Cómo leer este manual

- **Si es su primer día**, lea la sección 1 y la 4 (inicio rápido). Con eso puede empezar.
- **Si va a aprobar entregables** (PO, dueño de proceso, UX/UI, QA, operaciones), lea la sección 5 (cómo trabajar con Claude) y la 8 (gates y calidad).
- **Si va a instalar o administrar el skill**, lea la 3, la 10 y la 14.
- **Si algo falla**, vaya directo a la sección 15.

---

## Contenido

1. [Qué es Scrum-AI Delivery](#1-qué-es-scrum-ai-delivery)
2. [Conceptos clave](#2-conceptos-clave)
3. [Requisitos e instalación](#3-requisitos-e-instalación)
4. [Inicio rápido](#4-inicio-rápido)
5. [Cómo trabajar con Claude](#5-cómo-trabajar-con-claude)
6. [Sprint 0: conocer antes de construir](#6-sprint-0-conocer-antes-de-construir)
7. [El ciclo de una historia de usuario](#7-el-ciclo-de-una-historia-de-usuario)
8. [Quality gates, DoR, DoD y scorecard](#8-quality-gates-dor-dod-y-scorecard)
9. [Sprints, retrospectivas e indicadores](#9-sprints-retrospectivas-e-indicadores)
10. [Paquetes de skills integrados](#10-paquetes-de-skills-integrados)
11. [Otras capacidades: skills de terceros, MCP y RAG](#11-otras-capacidades-skills-de-terceros-mcp-y-rag)
12. [Trabajo con GitHub](#12-trabajo-con-github)
13. [Archivos que crea el skill](#13-archivos-que-crea-el-skill)
14. [Referencia de comandos](#14-referencia-de-comandos)
15. [Solución de problemas y preguntas frecuentes](#15-solución-de-problemas-y-preguntas-frecuentes)
16. [Glosario](#16-glosario)
17. [Mantener y actualizar el skill](#17-mantener-y-actualizar-el-skill)

---

## 1. Qué es Scrum-AI Delivery

Scrum-AI Delivery es una metodología que combina tres cosas:

1. **Scrum**, que organiza el trabajo en sprints de dos semanas con un backlog priorizado.
2. **Diseño orientado a especificaciones** (*Spec-Driven Development*), que define qué construir antes de programar: historia, flujo, mockup y criterios de aceptación.
3. **Agent Skills y vibecoding controlado**, que aceleran la ejecución con IA bajo reglas, pruebas y revisión.

Ninguna de las tres funciona sola. Juntas producen incrementos funcionales verificables.

### Qué hace el skill

El skill convierte a Claude en el **facilitador-ejecutor** de la metodología. En la práctica, Claude:

- Le dice en qué punto está el proyecto y cuál es el siguiente paso.
- Redacta los artefactos: visión, historias, criterios de aceptación, flujos BPMN/Mermaid, mockups, planes técnicos, ADR, código, pruebas, documentación y reportes.
- Usa, en cada fase, los skills especializados que el equipo aprobó (agent-skills, ECC, diseno-web-integral y otros), los servidores MCP conectados y las fuentes documentales (RAG).
- **Se detiene en cada gate** y le pide a una persona que apruebe o rechace, con la evidencia a la vista.
- Registra cada decisión con nombre, rol, fecha y evidencia, para que quede auditada.

### Qué no hace el skill (a propósito)

- **No aprueba nada.** Los agentes de IA ejecutan; las personas aprueban. El script rechaza a "Claude", "IA", "bot", "agente" y nombres similares como aprobadores.
- **No cambia el alcance** de una historia aprobada. Si descubre que algo es inviable, se detiene y lo propone al Product Owner.
- **No se salta pruebas.** Sin pruebas ejecutadas no hay G4.
- **No despliega a producción por iniciativa propia.** El release es el gate G6, y es humano.

### Por qué existe

| Antes | Con Scrum-AI Delivery |
|---|---|
| Requisitos ambiguos, criterios incompletos | Historias con reglas y criterios verificables antes de diseñar |
| Diseños que cambian durante el desarrollo | Diseño antes del código: flujo y mockup aprobados |
| Código generado con IA sin trazabilidad ni validación | IA bajo reglas: microciclo controlado, pruebas y revisión |
| Retrabajo y demoras | Iteraciones guiadas por especificaciones y retroalimentación temprana |
| Aprobaciones inciertas | Seis gates con evidencia, UAT y scorecard |

---

## 2. Conceptos clave

### 2.1 Los cuatro principios

1. **Los agentes de IA ejecutan, no aprueban.** Las decisiones críticas (priorización, diseño, aprobación, release) son humanas.
2. **Nada avanza sin evidencia.** Cada gate exige artefactos verificables; "se ve bien" no aprueba.
3. **Diseño antes del código.** Historia → flujo → mockup → plan técnico → código. Si falta un eslabón, la historia no entra a desarrollo.
4. **Las tres dimensiones van juntas.** Scrum organiza, la especificación define y la IA acelera, siempre bajo control.

### 2.2 Roadmap del proyecto (S0–S6)

El proyecto avanza por siete fases secuenciales. El skill no deja saltar fases sin una justificación explícita.

| Fase | Objetivo | Entregable principal |
|---|---|---|
| **S0** Descubrimiento y estrategia | Entender el problema y definir la visión | Visión, alcance inicial, caso de negocio, entregables del Sprint 0 |
| **S1** Planificación | Requerimientos, priorización y estimación | Backlog priorizado, roadmap detallado, criterios de éxito |
| **S2** Diseño | Solución técnica y experiencia de usuario | Arquitectura, flujos, prototipos, diseño de datos y APIs |
| **S3** Desarrollo | Construir de forma incremental y controlada | Código funcional, integraciones, build desplegable |
| **S4** Pruebas y validación | Calidad, seguridad y cumplimiento | Resultados de QA, validación de seguridad |
| **S5** Despliegue | Liberar en producción de forma segura | Despliegue, plan de monitoreo, comunicación a usuarios |
| **S6** Operación y mejora continua | Medir y evolucionar | Indicadores de uso, plan de mejoras, nuevas versiones |

El roadmap es la vista macro. Dentro de S1–S5, el trabajo ocurre en **sprints de dos semanas**, y cada historia recorre su propio ciclo de 11 pasos (sección 7).

### 2.3 Roles

| Rol | Qué hace en la metodología |
|---|---|
| **Product Owner (PO)** | Define prioridades, aprueba entregables y acepta el incremento. Aprueba G1, G3, G5 y G6 y los cambios de fase |
| **Scrum Master** | Facilita el proceso, gestiona el sprint y elimina bloqueos |
| **Responsable / Líder técnico** | Define la arquitectura, revisa código y seguridad, valida estándares. Aprueba G4 |
| **Dueño de proceso** | Aporta el conocimiento de negocio y valida reglas y excepciones. Aprueba G1, G2 y G3 |
| **Arquitecto de procesos** | Valida el flujo de negocio. Aprueba G2 |
| **UX/UI** | Diseña la experiencia, crea mockups y prototipos. Aprueba G3 |
| **QA / Seguridad** | Diseña y ejecuta pruebas, valida seguridad y calidad. Aprueba G4 y confirma el scorecard |
| **Usuarios clave** | Validan en UAT y confirman el valor. Aprueban G5 |
| **Operaciones / TI** | Despliegue, monitoreo y rollback. Aprueba G6 |
| **Agentes de IA (Claude)** | Generan código, pruebas y documentación. **No aprueban entregables** |

La matriz RACI del proyecto vive en `scrum-ai/vision/roles-raci.md` y se completa con nombres reales en el Sprint 0.

### 2.4 Las seis puertas (gates)

| Gate | Qué se aprueba | Quién aprueba |
|---|---|---|
| **G1 Requisitos** | Historia, reglas de negocio y criterios de aceptación | PO + Dueño de proceso |
| **G2 Flujo** | Diagrama BPMN/Mermaid con actores, permisos y excepciones | Dueño de proceso + Arquitecto de procesos |
| **G3 Diseño** | Mockup, estados de pantalla, responsive y accesibilidad | UX/UI + PO + Dueño de proceso |
| **G4 Desarrollo** | Código, pruebas, revisión de PR y seguridad | Líder técnico + QA/Seguridad |
| **G5 Funcional** | UAT con usuarios clave y evidencia | Usuarios clave + PO |
| **G6 Entrega** | Release, monitoreo, observabilidad y rollback | PO + Operaciones/TI |

El detalle de cada gate está en la sección 8.

---

## 3. Requisitos e instalación

### 3.1 Requisitos

| Componente | Para qué | Obligatorio |
|---|---|---|
| **Claude Code** (terminal, VS Code, JetBrains o escritorio), **Codex** (CLI o extensión) o **claude.ai / Cowork** | Ejecutar el skill | Sí, uno de ellos |
| **Python 3.8 o superior** | Scripts `sai.py` y `rag.py` (solo usan la biblioteca estándar) | Sí |
| **Git** | Control de versiones del proyecto y descarga de skills desde GitHub (`cap fetch`) | Recomendado |
| **GitHub CLI (`gh`)** o el MCP de GitHub | Issues, etiquetas, PR y releases | Opcional |
| **Node.js y npm** | Hooks del paquete ECC; plugin y CLI de Codex | Si usa ECC o la revisión cruzada |
| **Codex CLI** (`npm install -g @openai/codex`) con sesión (`codex login`) y una cuenta de OpenAI/ChatGPT | Revisión cruzada en Claude Code, o ejecutar el skill en Codex | Opcional |
| **`pdftotext`** (Poppler) | Indexar PDF en fuentes RAG locales | Opcional |

Para comprobar Python:

```bash
python --version
```

### 3.2 Instalar el skill en Claude Code

Clone el repositorio en la carpeta de skills de su usuario:

```bash
# macOS / Linux / Git Bash en Windows
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git ~/.claude/skills/scrum-ai-delivery
```

```powershell
# PowerShell en Windows
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git "$env:USERPROFILE\.claude\skills\scrum-ai-delivery"
```

Si prefiere que el skill viaje con un solo proyecto (para que todo el equipo use la misma versión), clónelo en `.claude/skills/scrum-ai-delivery` dentro del repositorio del proyecto y haga commit.

Abra una sesión nueva de Claude Code (o escriba `/reload-plugins`) para que lo detecte.

### 3.3 Instalar el skill en claude.ai o Cowork

1. Descargue el repositorio como `.zip` desde GitHub (*Code → Download ZIP*).
2. En claude.ai, vaya a **Configuración → Capacidades → Skills** y suba el `.zip`.
3. Active el skill.

En claude.ai los servidores MCP se conectan como **conectores** desde la configuración de la cuenta u organización, no desde `.mcp.json`.

### 3.3b Instalar el skill en Codex

Codex carga skills desde `~/.agents/skills/` (o `$CODEX_HOME/skills/`, por defecto `~/.codex/skills/`) y desde `.agents/skills/` del proyecto:

```bash
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git ~/.agents/skills/scrum-ai-delivery
```

```powershell
git clone https://github.com/vmrojasl/Scrum-AI-Delivery.git "$env:USERPROFILE\.agents\skills\scrum-ai-delivery"
```

Abra una sesión nueva de Codex y pida, por ejemplo, *"Usa $scrum-ai-delivery para iniciar el proyecto X"*. El skill trae `agents/openai.yaml` con su nombre visible y su descripción para Codex. En Codex, los comandos del script llevan `--harness codex` (sección 10.8).

### 3.4 Instalar los paquetes de skills integrados

El skill trabaja mejor con tres paquetes de skills que ejecuta en cada fase y, en Claude Code, con el plugin de Codex para la revisión cruzada (sección 10). Todos son opcionales: sin ellos la metodología funciona con las referencias del propio skill.

**Forma recomendada: que el skill los instale.** Al iniciar, Claude revisa qué paquetes faltan. Si falta alguno, le muestra el plan y le pide autorización. También puede hacerlo usted, desde la raíz de un proyecto ya inicializado:

```bash
sai.py cap install          # muestra qué falta, de qué repositorio original sale, licencia y avisos
sai.py cap install --yes    # lo instala (o --pack <paquete> --yes para uno solo)
```

| Paquete | De dónde lo instala `cap install` |
|---|---|
| agent-skills | Plugin desde su repositorio original, `github.com/addyosmani/agent-skills` |
| ecc | Plugin desde su repositorio original, `github.com/affaan-m/ECC` |
| diseno-web-integral | Copia incluida en este skill (`vendor/diseno-web-integral`, es propietario). Sus dependencias de diseño se descargan de sus repositorios originales: `pbakaus/impeccable` (Apache-2.0), `Leonxlnx/taste-skill`, `nextlevelbuilder/ui-ux-pro-max-skill` y `emilkowalski/skills` (MIT) |
| codex (solo Claude Code) | Plugin `codex@openai-codex` desde `github.com/openai/codex-plugin-cc`. Si falta el CLI de Codex, `npm install -g @openai/codex`. Después **usted** inicia sesión con `codex login` (es interactivo) |

En Codex, `cap install --harness codex` copia los skills de agent-skills y ECC a `~/.agents/skills/`, adaptados a Codex, e instala `diseno-web-integral` con sus dependencias en esa misma carpeta. El plugin de Codex no aplica ahí.

Detalles del comportamiento:

- Busca el CLI de Claude Code en la sesión actual, en el PATH y en las extensiones de VS Code, Cursor y Windsurf.
- Si no encuentra el CLI, o la instalación del plugin falla, clona el repositorio original y copia a `~/.claude/skills/` solo los skills que usa la metodología.
- Nunca sobrescribe una skill que ya exista con el mismo nombre.
- Al terminar, recargue Claude Code con `/reload-plugins` o abra una sesión nueva.
- **Instalar no es aprobar:** los skills quedan en `pendiente_revision` hasta que una persona los apruebe (sección 10.3).

Si prefiere instalarlos a mano, estos son los comandos equivalentes.

**agent-skills** (Addy Osmani, licencia MIT):

```bash
claude plugin marketplace add addyosmani/agent-skills
claude plugin install agent-skills@addy-agent-skills --scope user
```

**ECC — Everything Claude Code** (Affaan Mustafa, licencia MIT):

```bash
claude plugin marketplace add affaan-m/ECC
claude plugin install ecc@ecc --scope user
```

ECC instala *hooks* que corren en cada uso de herramienta y en cada sesión. Puede ajustarlos con `/plugin configure ecc@ecc` (perfiles `minimal`, `standard` o `strict`, o desactivarlos con `hooks_enabled=false`).

**Codex para Claude Code** (OpenAI, licencia Apache-2.0):

```bash
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex --scope user
npm install -g @openai/codex
codex login
```

**diseno-web-integral**: copie la carpeta `vendor/diseno-web-integral` de este skill en `~/.claude/skills/`. Para sus dependencias, descargue los `.zip` de los cuatro repositorios de diseño en una carpeta y ejecute `python ~/.claude/skills/diseno-web-integral/scripts/instalar.py --zips <carpeta> --destino claude`.

> **Dónde está el comando `claude` en VS Code.** Si `claude` no está en el PATH, el ejecutable viene con la extensión, en `~/.vscode/extensions/anthropic.claude-code-<versión>/resources/native-binary/claude.exe`. También puede escribir `/plugin` dentro de Claude Code para instalar desde la interfaz.

### 3.5 Verificar la instalación

Dentro del proyecto donde va a trabajar:

```bash
python ~/.claude/skills/scrum-ai-delivery/scripts/sai.py -h
```

Después de inicializar el proyecto (sección 4), compruebe los paquetes:

```bash
python ~/.claude/skills/scrum-ai-delivery/scripts/sai.py cap detect
```

La salida esperada en Claude Code, con todo instalado, es:

```text
  (entorno: Claude Code)
  agent-skills           instalados 20  ·  faltan 0
  diseno-web-integral    instalados 1  ·  faltan 0
  ecc                    instalados 12  ·  faltan 0
  codex                  instalados 1  ·  faltan 0
```

Si falta el CLI de Codex, aparece una línea adicional con el comando para instalarlo. En Codex, la línea de `codex` no aparece.

> **Nota sobre las rutas.** En este manual `sai.py` es una abreviatura de `python <carpeta del skill>/scripts/sai.py`. Ejecute siempre los comandos **desde la raíz del proyecto** (la carpeta que contiene `scrum-ai/`), no desde la carpeta del skill.

---

## 4. Inicio rápido

Este recorrido toma unos minutos y deja el proyecto listo para el Sprint 0. Son cinco pasos.

**1. Abra Claude Code en la carpeta de su proyecto** y escriba algo como:

> Iniciemos el proyecto "Portal de convocatorias" con la metodología Scrum-AI. Ya existe código.

Claude le preguntará:

- El nombre del proyecto y si ya hay código (modo `existente`) o no (modo `nuevo`).
- Si usarán GitHub.
- **Dónde se harán las pruebas**: en un `sandbox` (una carpeta o un proyecto de pruebas aparte), en una `rama` de git o en el propio `proyecto`.
- La **complejidad del proyecto**, para elegir un perfil: `esencial` (prototipo o herramienta pequeña), `estandar` (por defecto) o `completo` (institucional o crítico).

Luego ejecutará:

```bash
sai.py init --name "Portal de convocatorias" --mode existente --github --tests-in sandbox --tests-path ../portal-pruebas --profile estandar
```

**Perfil y flags de ahorro.** El perfil decide cuánto de la metodología y de los skills externos se ejecuta, para no gastar tokens en lo que el proyecto no necesita:

| Perfil | Skills externos | Etapas omitidas | Diseño | Detalle | Verificación |
|---|---|---|---|---|---|
| `esencial` | ninguno | flujo y UAT | básico | breve | ligero |
| `estandar` | solo principales | ninguna | básico | breve | ligero |
| `completo` | todos | ninguna | integral (`diseno-web-integral`) | completo | completo |

Puede ajustar cualquier valor con flags, en `init` o después con `config`:

```bash
sai.py config --skills todos --design integral    # más capacidad para este proyecto
sai.py config --skip-stages mockup                # sin mockup por defecto (p. ej. un API)
sai.py story add US-API-01 "Exponer convocatorias" --skip mockup   # solo para esta historia
```

G1, G4, G6, DoR, DoD, el scorecard y la aprobación humana nunca se omiten. Para un solo paso también puede escribir flags en su mensaje, como `--completo`, `--sin-skills`, `--con <skill>`, `--breve`, `--verificar` o `--xreview`, sin cambiar la configuración del proyecto.

Esto crea la carpeta `scrum-ai/`, los archivos `AGENTS.md` y `CONSTRAINTS.md`, las plantillas de visión, roles y DoR/DoD y, con `--github`, las plantillas de issue, PR y el workflow de quality gates. También detecta los paquetes de skills instalados.

**Nivel de verificación.** Con `ligero`, Claude escribe las pruebas y le da los comandos; usted los ejecuta y le pega el resultado. La revisión cruzada de Codex y los skills extra de verificación (E2E, navegador, regresión) se corren solo si usted los pide. Así se ahorran tokens y las respuestas son más cortas. Con `completo`, el agente ejecuta todo por su cuenta. Puede cambiarlo cuando quiera: `sai.py config --verify completo`.

**Lugar de las pruebas.** Claude solo crea prototipos y proyectos de prueba en el lugar registrado, y no rehace ni reestructura el proyecto para probar: si una prueba parece exigirlo, se detiene y le pregunta. En proyectos creados antes de esta opción, `status` muestra «Pruebas: sin definir», y Claude se lo preguntará antes de escribir la primera prueba (`sai.py config --tests-in …`).

**2. Instale lo que falte.** Si `init` reporta paquetes faltantes, Claude le mostrará el plan de `cap install`, con los repositorios de origen, las licencias y los avisos. Si lo autoriza, los instala y le pide recargar Claude Code.

**3. Apruebe los paquetes de skills.** Claude le resumirá qué hace cada paquete y qué ejecuta. Si está de acuerdo, responda con su nombre y rol, por ejemplo: *"Aprobado. Juan Ruiz, Líder técnico"*. Claude registra:

```bash
sai.py cap approve --pack agent-skills --by "Juan Ruiz (Líder técnico)"
```

**4. Trabaje el Sprint 0.** Pida, por ejemplo: *"Hagamos la visión del MVP"*. Claude le hará preguntas de una en una y completará `scrum-ai/vision/vision.md` (sección 6).

**5. Pregunte en cualquier momento** *"¿dónde estamos?"*. Claude ejecuta `sai.py status` y le resume la fase, el sprint, las historias y el siguiente paso de cada una.

---

## 5. Cómo trabajar con Claude

La mayor parte del tiempo **usted conversa y el agente ejecuta los comandos**. No necesita memorizar `sai.py`. Esta sección habla de Claude, pero en Codex funciona igual (diferencias en la sección 10.8).

### 5.1 Qué esperar en cada respuesta

En cada interacción Claude entrega:

- Una línea de contexto: fase, sprint, historia y estado.
- El artefacto que produjo (un archivo en `scrum-ai/…` o en el código) y un resumen breve.
- Una **solicitud de aprobación** cuando toca un gate, o la siguiente acción que propone.
- Las fuentes citadas si consultó documentos (RAG), y el nombre del skill o MCP que usó.

### 5.2 Ejemplos de pedidos

| Quiere… | Puede decir |
|---|---|
| Saber el estado | "¿Dónde estamos?", "¿Qué sigue?" |
| Arrancar el proyecto | "Iniciemos el proyecto X con Scrum-AI" |
| Trabajar el Sprint 0 | "Hagamos la visión", "Audita el código existente", "Completa AGENTS.md" |
| Crear historias | "Crea la historia US-CONV-001: consultar convocatorias, épica Convocatorias" |
| Especificar | "Especifica US-CONV-001 con sus reglas y criterios de aceptación" |
| Diseñar | "Haz el flujo BPMN de US-CONV-001", "Diseña el mockup de la ficha" |
| Construir | "Implementa US-CONV-001 siguiendo el plan técnico" |
| Verificar | "Corre la verificación y prepara la evidencia de G4" |
| Iniciar o cerrar sprint | "Iniciemos el sprint 1 con objetivo…", "Cierra el sprint y haz el reporte" |
| Registrar una decisión técnica | "Registra un ADR: usar PostgreSQL" |
| Conectar documentos | "Indexa la carpeta docs/normativa como fuente RAG para Define y Review" |

### 5.3 Cómo aprobar o rechazar un gate

Cuando un entregable está listo, Claude presenta una solicitud con esta forma:

```
## Solicitud de aprobación — G3 Diseño · US-CONV-001
Qué se verifica: mockup de alta fidelidad; estados (carga, vacío, error); responsive; accesibilidad
Evidencia: scrum-ai/design/US-CONV-001/diseno-ui.md, prototipo en …
Autoverificación: ✔ estados de carga y error · ✖ falta estado vacío útil
Revisión cruzada (Codex): no aplica en G3
Riesgos o pendientes: …
Quién aprueba: UX/UI + Product Owner + Dueño de proceso
→ Responda "aprobado" o "rechazado + observaciones", indicando nombre y rol de quien aprueba.
```

Para responder:

- **Aprobar:** *"Aprobado. Sofía León (UX/UI), Ana Pérez (PO) y Luis Gómez (Dueño de proceso)."*
- **Rechazar:** *"Rechazado. Sofía León (UX/UI). Falta el estado vacío y el contraste del botón no cumple."*

Reglas importantes:

- **Siempre dé nombre y rol** de cada persona que aprueba. Si no los da, Claude se los pedirá: el acta queda en `scrum-ai/evidence/<ID>/<G#>.md` y sirve de auditoría.
- **Aprueba quien tiene el rol.** Si usted es el PO y el gate pide también al Dueño de proceso, consiga su aprobación antes de responder, o registre solo la suya y deje la observación.
- **La autoverificación es honesta a propósito.** Claude marca con ✖ lo que no se cumple. Es mejor presentar un pendiente que ocultarlo: el gate existe para que usted decida con información completa.

**Aprobar más rápido.** Para no esperar seis aprobaciones por historia:

- **Regístrese una vez como aprobador:** `sai.py config --approver "Ana Pérez (PO)"` (o al iniciar con `init --approver`). Desde entonces basta con responder *"aprobado"*. Si aprueba otra persona, Claude pedirá su nombre y rol.
- **Cuatro puntos de decisión por historia, no seis.** Claude prepara un tramo completo y le pide una sola respuesta:
  1. Planeación: G1 de todas las historias del sprint.
  2. Diseño: G2 y G3 juntos, con el plan técnico.
  3. Entrega técnica: G4.
  4. Cierre: G5, DoD, scorecard y G6.
- **La historia avanza sola** al aprobarse un gate, al completarse el DoR o al aprobarse DoD y scorecard.
- **Una plantilla sin completar nunca cuenta como evidencia:** el script la rechaza aunque usted responda *"aprobado"*.

Ejemplo de lo que Claude registra tras su *"aprobado"*: `sai.py gate US-1,US-2,US-3 G1 --decision aprobado`.

### 5.4 Si tiene prisa y quiere saltarse un control

Claude no se salta controles por prisa. Si alguien quiere omitir un gate, Claude explicará el riesgo. Si la persona con autoridad lo decide de todos modos, la excepción se registra con su nombre y la justificación en `--notes`, de modo que quede auditada.

### 5.5 Idioma

Claude responde en el idioma de la conversación (por defecto español). Los skills de terceros están en inglés; Claude le traduce sus resultados.

---

## 6. Sprint 0: conocer antes de construir

**Objetivo:** alinear visión, personas, tecnología y proceso antes de construir. Si hay código existente, obtener un diagnóstico accionable que alimente el backlog real.

### 6.1 Entregables

El Sprint 0 tiene 11 entregables. `sai.py sprint0` muestra el checklist y `sai.py sprint0 <clave> --evidence <ruta>` marca cada uno cuando la persona responsable lo valida.

| Clave | Entregable | Cómo lo produce Claude |
|---|---|---|
| `vision_mvp` | Visión y MVP: alcance, valor, primera versión | Entrevista guiada, una pregunta a la vez → `scrum-ai/vision/vision.md` |
| `inventario_funcional` | Funcionalidades y componentes existentes | Recorrido del repositorio o del sistema actual |
| `matriz_roles` | Equipos, responsabilidades, RACI | Completa `scrum-ai/vision/roles-raci.md` con nombres reales |
| `diagnostico_tecnico` | Estado del código, arquitectura, dependencias y riesgos | Auditoría (6.2). **Solo en modo `existente`**; en modo `nuevo` aparece como `[-]` (no aplica) |
| `adr` | Decisiones técnicas clave | `sai.py adr "<título>"` por cada decisión |
| `dor_dod` | Criterios de entrada y salida de historias | Revisión de `scrum-ai/dor-dod.md` con el equipo |
| `estructura_repositorio` | Carpetas, ramas y convenciones | Propuesta de estructura (sección 12) |
| `agents_md` | Guía para agentes de IA | Completa `AGENTS.md`: stack, comandos, convenciones |
| `constraints_md` | Restricciones y límites operativos | Completa `CONSTRAINTS.md`: técnicas, seguridad, calidad, límites de la IA, operación |
| `pipeline_ci_cd` | Automatización y quality gates | Adapta `.github/workflows/quality-gates.yml` al stack |
| `sprint1_refinado` | Backlog listo para iniciar | Historias del Sprint 1 con ficha y DoR en curso |

**La visión** (`vision.md`) cubre: propósito, problema y oportunidad, usuarios, objetivos medibles (indicador, línea base, meta y plazo), alcance dentro y fuera del MVP, caso de negocio, módulos involucrados, stakeholders y aprobación.

**`AGENTS.md` y `CONSTRAINTS.md`** son las reglas que Claude y cualquier otro agente deben seguir en el repositorio. `CONSTRAINTS.md` ya trae, entre otras, estas restricciones por defecto:

- Sin secretos en el código ni en los prompts.
- Cumplimiento de la Ley 1581 de 2012 (Habeas Data) y datos anonimizados en pruebas.
- Una vulnerabilidad crítica (CVSS 9.0–10) bloquea la entrega.
- SAST/DAST obligatorio antes de G4.
- Estados de UI obligatorios: carga, vacío, error, permisos, confirmación y responsive.
- Los agentes no modifican alcance, no omiten pruebas, no despliegan y no aprueban gates.

### 6.2 Auditoría del código existente (modo `existente`)

Proceso: **analizar el repositorio → evaluar el estado → definir la acción → documentar hallazgos → generar el backlog real.**

1. **Inventario.** Árbol del repositorio con semáforo por carpeta (frontend, backend, base de datos, docs, tests, workflows, dependencias). Lo que Claude no puede ver se marca como "no evaluado"; no se inventa.
2. **Evaluación por componente**: arquitectura, frontend, backend, datos, dependencias, seguridad, pruebas, CI/CD, documentación y deuda técnica. Cada uno recibe un estado técnico de 1 a 5, apoyado en evidencia objetiva cuando es posible (pruebas, `npm audit`/`pip-audit`, linters, cobertura).
3. **Decisión por componente** según el valor de negocio (lo confirma el PO) y el estado técnico:

   | | Estado técnico bueno (≥3) | Estado técnico malo (<3) |
   |---|---|---|
   | **Valor alto (≥3)** | **Conservar**: usar como base | **Refactorizar**: mejorar y modernizar |
   | **Valor bajo (<3)** | **Retirar**: eliminar | **Reconstruir**: desarrollar de nuevo |

   ```bash
   sai.py audit Backend --state 2 --value 5
   # ✔ Backend: estado 2/5, valor 5/5 → sugerida Refactorizar, decidida Refactorizar
   ```

   La acción sugerida orienta; la decide el equipo con `--action Conservar|Refactorizar|Reconstruir|Retirar`.
4. **Resultado.** `sai.py audit` (sin argumentos) muestra la tabla y la distribución porcentual por acción. Los hallazgos se documentan en `scrum-ai/audit/auditoria.md`.
5. **Backlog real.** De la auditoría salen épicas, historias y tareas técnicas (`sai.py story add …`).

Si ECC está aprobado, Claude puede usar `ecc:brownfield-retrospective` para el registro de brechas.

### 6.3 Pasar a S1

Antes del Sprint 1 hay decisiones que **toman personas**: validar visión y alcance, asignar roles, aprobar la arquitectura objetivo (ADR), definir entornos y accesos, aprobar DoR/DoD, activar el pipeline, priorizar el backlog y aprobar `AGENTS.md` y `CONSTRAINTS.md`. Claude se las presenta como lista de pendientes con responsable.

Cuando estén resueltas:

```bash
sai.py phase --set S1 --approver "Ana Pérez (PO)"
sai.py sprint start --goal "Consulta de convocatorias"
```

Si el Sprint 0 tiene entregables pendientes, el cambio de fase se bloquea:

```
✖ Sprint 0 incompleto (inventario_funcional, matriz_roles, …). Complete o use --force con justificación.
```

`--force` existe para casos justificados; úselo solo con la decisión explícita del PO.

---

## 7. El ciclo de una historia de usuario

### 7.1 Los estados

Cada historia recorre 12 estados. El script **bloquea** el avance si falta el requisito de salida, y solo deja avanzar **un estado a la vez**.

```
backlog → especificacion ─G1→ flujo ─G2→ mockup ─G3→ plan_tecnico ─DoR→ ready → desarrollo
        → pruebas ─G4→ uat ─G5→ aceptacion ─DoD + scorecard→ release ─G6→ done
```

| # | Paso del sprint | Estado | Fase de skills | Requisito para salir | Archivo principal |
|---|---|---|---|---|---|
| 01 | Selección del backlog | `backlog` | Plan | — | `scrum-ai/backlog/<ID>.md` |
| 02 | Especificación | `especificacion` | Define | **G1** | `scrum-ai/backlog/<ID>.md` |
| 03 | Flujo | `flujo` | Design | **G2** | `scrum-ai/design/<ID>/flujo.md` |
| 04 | Mockup | `mockup` | Design | **G3** | `scrum-ai/design/<ID>/diseno-ui.md` |
| 05 | Plan técnico | `plan_tecnico` | Design | **DoR** completo | ADR en `scrum-ai/adr/` |
| — | Lista para desarrollo | `ready` | Plan | — | — |
| 06 | Desarrollo con IA | `desarrollo` | Build | — | Rama `feature/<ID>` |
| 07 | Pruebas | `pruebas` | Verify | **G4** | PR, resultados de pruebas |
| 08 | UAT | `uat` | Verify | **G5** | Plan y resultados de UAT |
| 09 | Aceptación del PO | `aceptacion` | Review | **DoD** + **scorecard ≥85** | `scrum-ai/evidence/<ID>/scorecard.json` |
| 10 | Release | `release` | Ship | **G6** | Release publicado |
| 11 | Cerrada | `done` | Ship | — | Retrospectiva a nivel sprint |

**Retroceder** a un estado anterior está permitido, pero exige un motivo:

```bash
sai.py story move US-CONV-001 flujo --reason "Mockup no aprobado: el flujo no contempla permisos"
```

### 7.2 Qué pasa en cada paso

**01 Selección del backlog.** Claude revisa el backlog con el PO, propone el Sprint Goal y las historias que caben. Al mover una historia de `backlog` a `especificacion`, queda asignada al sprint actual.

**02 Especificación → G1.** Claude completa la ficha `scrum-ai/backlog/<ID>.md`:

- *Como / Quiero / Para*, valor esperado, reglas de negocio y dependencias.
- **Criterios de aceptación verificables** en tabla (ID, condición, resultado esperado). Deben cubrir: caso feliz, filtros o variantes, sin resultados (estado vacío útil), caso de borde de negocio, error del servidor (mensaje comprensible y reintento) y uso móvil.
- Evidencia requerida.

Claude pregunta lo que falte en vez de inventar reglas, y si la regla depende de normativa institucional consulta las fuentes RAG y las cita. En Claude Code con el paquete `codex` aprobado, antes de pedir G1 pasa la ficha por la **revisión cruzada de Codex** (sección 10.7). **Sin esta ficha la historia no entra a desarrollo.**

**03 Flujo → G2.** Dos miradas en `flujo.md`:

- **BPMN 2.0 (negocio):** carriles por actor, decisiones, excepciones, permisos y rutas alternativas.
- **Mermaid de estados (interacción):** navegación y estados de pantalla (carga, vacío, error, permisos).

Cada criterio de aceptación debe aparecer en algún camino del flujo.

**04 Mockup → G3.** Tres niveles en `diseno-ui.md`: **wireframe** (estructura), **mockup visual** (el contrato visual del desarrollo, con el sistema de diseño institucional) y **prototipo navegable**. Si `diseno-web-integral` está aprobado, Claude conduce este paso con él (diagnóstico, diseño, validación medida y aprobación). Su aprobación final **es evidencia para G3, no reemplaza a G3**.

**05 Plan técnico → DoR.** Arquitectura afectada, tareas y estimación, contratos de API (OpenAPI cuando aplique), datos y riesgos. Las decisiones relevantes se registran como ADR. Se completan los ítems de DoR que los gates no marcaron (`dependencias_identificadas` y `tamano_estimado`). Antes de cerrar el DoR, revisión cruzada del plan técnico (sección 10.7).

**06 Desarrollo con IA.** Claude sigue el **microciclo de vibecoding controlado**:

1. **Preparar contexto**: ficha, flujo, mockup, plan técnico, `AGENTS.md`, `CONSTRAINTS.md`, ADR y código relevante.
2. **Generar plan**: archivos a crear o modificar, pruebas a escribir (una o más por criterio) y riesgos.
3. **Desarrollar** en `feature/<ID>`, con cambios pequeños e incrementales y TDD.
4. **Probar**: ejecutar realmente las pruebas y conservar la salida. Nunca se declara "pasa" sin ejecutar.
5. **Revisar** contra estándares y `CONSTRAINTS.md`, con linters, análisis de dependencias y SAST.
6. **Corregir** hasta cumplir los criterios, o reportar el bloqueo con claridad.
7. **Presentar evidencia**: PR con tabla criterio → prueba → resultado, salida de pruebas, informe de seguridad, capturas responsive y nota de qué se generó con IA.

**07 Pruebas → G4.** Pruebas automatizadas por criterio (AC01…ACnn), revisión de seguridad, revisión del PR y cumplimiento de estándares. Claude calcula un **scorecard preliminar**. Si ECC está aprobado, adjunta el informe PASS/FAIL de `ecc:verification-loop`. Con el paquete `codex`, Codex revisa el código antes de pedir G4 (sección 10.7).

**08 UAT → G5.** Plan de UAT con usuarios clave, escenarios y datos reales o anonimizados, registro de hallazgos y correcciones, y evidencia de aceptación.

**09 Aceptación → DoD + scorecard.** El PO revisa contra los criterios. Se completan los ítems de DoD pendientes y el **scorecard final** debe quedar aprobado.

**10 Release → G6.** El despliegue lo ejecuta **una persona o un pipeline con revisores requeridos**, nunca Claude por iniciativa propia. Se verifica monitoreo y alertas, plan de rollback probado y documentación de despliegue. Con el paquete `codex`, Codex revisa la preparación del release antes de pedir G6.

**11 Retrospectiva.** A nivel de sprint (sección 9).

### 7.3 Recorrido completo de ejemplo: US-CONV-001

La historia de referencia de la metodología es **US-CONV-001 Consultar convocatorias**:

- **Como** investigador **quiero** consultar las convocatorias disponibles y filtrar las oportunidades **para** identificar aquellas a las que puedo postularme.
- **Reglas:** solo se publican convocatorias autorizadas; los estados dependen de fechas y decisiones administrativas; una convocatoria cerrada sigue siendo consultable cuando corresponda; los documentos tienen control de versiones.
- **Criterios:** AC01 listado con título, plazo y estado · AC02 filtro → solo coincidencias · AC03 sin resultados → estado vacío útil · AC04 vencida → no aparece como abierta · AC05 error del servidor → mensaje y reintento · AC06 móvil → sin desbordamiento.

A continuación, los comandos que Claude ejecuta a lo largo del ciclo, con lo que responde el script (salidas reales, abreviadas). Los nombres de personas son ilustrativos.

```bash
# Sprint y historia
sai.py sprint start --goal "Consulta de convocatorias"
# ✔ Sprint 1 iniciado (2026-10-20 → 2026-11-03). Plan: scrum-ai/sprints/sprint-1/plan.md
sai.py story add US-CONV-001 "Consultar convocatorias" --epic Convocatorias
# ✔ US-CONV-001 creada en backlog → scrum-ai/backlog/US-CONV-001.md
sai.py story move US-CONV-001 especificacion
# Siguiente: Producir evidencia de G1 (Requisitos) y pedir aprobación a: Product Owner, Dueño de proceso.

# Intentar avanzar sin G1
sai.py story move US-CONV-001 flujo
# ✖ Bloqueado: salir de 'especificacion' requiere G1 (Requisitos) aprobado por humanos.

# G1, después de que las personas aprueban en la conversación
sai.py gate US-CONV-001 G1 --decision aprobado \
  --approver "Ana Pérez (PO)" --approver "Luis Gómez (Dueño de proceso)" \
  --evidence scrum-ai/backlog/US-CONV-001.md
# ✔ G1 aprobado para US-CONV-001. Acta: scrum-ai/evidence/US-CONV-001/G1.md

sai.py story move US-CONV-001 flujo
#    + scrum-ai/design/US-CONV-001/flujo.md
sai.py gate US-CONV-001 G2 --decision aprobado \
  --approver "Luis Gómez (Dueño de proceso)" --approver "Marta Ríos (Arquitecta de procesos)" \
  --evidence scrum-ai/design/US-CONV-001/flujo.md

sai.py story move US-CONV-001 mockup
#    + scrum-ai/design/US-CONV-001/diseno-ui.md

# Un rechazo también queda registrado
sai.py gate US-CONV-001 G3 --decision rechazado --approver "Sofía León (UX/UI)" --notes "Falta estado vacío"
# Siguiente: G3 rechazado → ajustar y volver a presentar evidencia.
sai.py gate US-CONV-001 G3 --decision aprobado \
  --approver "Sofía León (UX/UI)" --approver "Ana Pérez (PO)" --approver "Luis Gómez (Dueño de proceso)" \
  --evidence scrum-ai/design/US-CONV-001/diseno-ui.md

# Plan técnico y DoR
sai.py story move US-CONV-001 plan_tecnico
sai.py story move US-CONV-001 ready
# ✖ Bloqueado por Definition of Ready. Falta: dependencias_identificadas, tamano_estimado
sai.py dor US-CONV-001 dependencias_identificadas tamano_estimado
sai.py story move US-CONV-001 ready
sai.py story move US-CONV-001 desarrollo
sai.py story move US-CONV-001 pruebas

# Scorecard preliminar y G4
sai.py score US-CONV-001 --func 4 --tec 4 --ux 4 --pruebas 5 --seg 4 --doc 4 --evaluator "Pedro Díaz (QA)"
# TOTAL 83.0/100 · ⚠ No alcanza el umbral mínimo de 85/100. · ESTADO: NO APROBADA
sai.py gate US-CONV-001 G4 --decision aprobado \
  --approver "Juan Ruiz (Líder técnico)" --approver "Pedro Díaz (QA)" \
  --evidence https://github.com/org/repo/pull/12

# UAT y G5
sai.py story move US-CONV-001 uat
sai.py gate US-CONV-001 G5 --decision aprobado \
  --approver "Investigadores piloto (Usuarios clave)" --approver "Ana Pérez (PO)" \
  --evidence scrum-ai/evidence/US-CONV-001/uat.md

# Aceptación: DoD y scorecard final
sai.py story move US-CONV-001 aceptacion
sai.py story move US-CONV-001 release
# ✖ Bloqueado por Definition of Done. Falta: aceptacion_completa, responsive_verificado, documentacion_al_dia
sai.py dod US-CONV-001 aceptacion_completa responsive_verificado documentacion_al_dia
sai.py story move US-CONV-001 release
# ✖ Bloqueado: el scorecard debe estar aprobado (≥85/100, ninguna dimensión <3, sin controles críticos).
sai.py score US-CONV-001 --func 5 --tec 4 --ux 4 --pruebas 5 --seg 4 --doc 4 --evaluator "Pedro Díaz (QA)"
# TOTAL 89.0/100 · ESTADO: APROBADA
sai.py story move US-CONV-001 release

# Release y cierre
sai.py gate US-CONV-001 G6 --decision aprobado \
  --approver "Ana Pérez (PO)" --approver "Carlos Vega (Operaciones/TI)" \
  --evidence https://github.com/org/repo/releases/tag/v1.0.0
sai.py story move US-CONV-001 done
# Siguiente: Cerrada con evidencia.
```

Al final, `scrum-ai/evidence/US-CONV-001/` contiene las actas `G1.md` a `G6.md` y `scorecard.json`.

---

## 8. Quality gates, DoR, DoD y scorecard

### 8.1 Detalle de los gates

| Gate | Qué se verifica | Evidencia esperada |
|---|---|---|
| **G1 Requisitos** | Historia completa · reglas de negocio · criterios de aceptación · dependencias y alcance | Historia en el backlog · criterios · trazabilidad de requisitos |
| **G2 Flujo** | Flujo de proceso · actores y permisos · escenarios principales y excepciones · coherencia con requisitos | Diagrama BPMN/Mermaid · descripción de escenarios · validación del proceso |
| **G3 Diseño** | Mockup de alta fidelidad · estados (carga, vacío, error) · responsive · accesibilidad y consistencia | Mockups aprobados · prototipo navegable · guía de estilos (si aplica) |
| **G4 Desarrollo** | Implementación completa · pruebas automatizadas · revisión de código (PR) · estándares · seguridad (SAST/DAST) | PR y revisión · resultados de pruebas · informe de seguridad · buenas prácticas |
| **G5 Funcional** | Funcionalidad según criterios · pruebas con usuarios clave · datos y escenarios reales · corrección de hallazgos | Plan y resultados de UAT · registro de hallazgos · evidencia de aceptación |
| **G6 Entrega** | Despliegue en producción · monitoreo · observabilidad y alertas · rollback · documentación operativa | Release en producción · alertas activas · rollback probado · documentación de despliegue |

Para ver la definición desde la terminal: `sai.py gate G3`.

### 8.2 Reglas que el script hace cumplir

Al registrar un gate (`sai.py gate <ID> <G#> …`), el script verifica:

- **Momento correcto.** Cada gate se decide en su estado: G1 en `especificacion`, G2 en `flujo`, G3 en `mockup`, G4 en `pruebas`, G5 en `uat` y G6 en `release`. Fuera de ese estado se rechaza (salvo `--force`).
- **Aprobadores humanos.** Cada `--approver` debe ser "Nombre (rol)" de una persona. Se rechazan nombres que contengan palabras como *claude, agente, agent, IA, AI, bot, GPT, copilot, LLM* o *asistente*.
- **Evidencia obligatoria para aprobar.** Al menos un `--evidence`, que debe ser una ruta existente dentro del repositorio o una URL `http(s)://`. Un rechazo puede registrarse sin evidencia, con `--notes`.
- **Controles críticos en G4.** Si el scorecard registrado tiene un control crítico fallido, G4 no se puede aprobar.
- **Acta.** Cada decisión genera `scrum-ai/evidence/<ID>/<G#>.md` con decisión, fecha, aprobadores, lo verificado, evidencia y observaciones. Si el gate se vuelve a decidir, el acta se reemplaza con la decisión más reciente (el historial completo queda en el log de `state.json`). En G1, G4 y G6 el acta enlaza la revisión cruzada de Codex, o dice "No se ejecutó" si la revisión cruzada estaba activa y no se corrió.
- **Agentes como aprobadores.** También se rechazan *codex* y *openai*.

### 8.3 Definition of Ready (DoR)

Condición para pasar de `plan_tecnico` a `ready`. Los siete ítems:

| Ítem | Se marca automáticamente con |
|---|---|
| `historia_definida` | G1 aprobado |
| `reglas_de_negocio` | G1 aprobado |
| `criterios_de_aceptacion` | G1 aprobado |
| `flujo_aprobado` | G2 aprobado |
| `mockup_validado` | G3 aprobado |
| `dependencias_identificadas` | `sai.py dor <ID> dependencias_identificadas` |
| `tamano_estimado` | `sai.py dor <ID> tamano_estimado` |

### 8.4 Definition of Done (DoD)

Condición (junto con el scorecard) para pasar de `aceptacion` a `release`:

| Ítem | Se marca automáticamente con |
|---|---|
| `pr_revisado` | G4 aprobado |
| `pruebas_ok` | G4 aprobado |
| `seguridad_validada` | G4 aprobado |
| `uat_completado` | G5 aprobado |
| `aceptacion_completa` | `sai.py dod <ID> aceptacion_completa` |
| `responsive_verificado` | `sai.py dod <ID> responsive_verificado` |
| `documentacion_al_dia` | `sai.py dod <ID> documentacion_al_dia` |

Para desmarcar un ítem: `sai.py dor|dod <ID> <ítem> --undo`.

### 8.5 Scorecard de calidad

| Criterio | Qué evalúa | Peso | Opción |
|---|---|---|---|
| Funcionalidad | Cumple los requisitos y el valor esperado | 30% | `--func` |
| Calidad técnica | Arquitectura, código, estándares | 20% | `--tec` |
| Diseño / UX | Usabilidad, accesibilidad, consistencia | 15% | `--ux` |
| Pruebas | Cobertura, casos, resultados | 15% | `--pruebas` |
| Seguridad | Vulnerabilidades, cumplimiento | 15% | `--seg` |
| Documentación | Técnica, funcional y de usuario | 5% | `--doc` |

Cada criterio se califica de 1 a 5. **Puntaje = Σ peso × calificación / 5.**

**Para aprobar se necesitan las tres condiciones:**

1. Puntaje **≥ 85/100**.
2. **Ninguna** dimensión por debajo de **3/5**.
3. **Ningún control crítico** fallido.

**Controles críticos** (binarios: si uno falla, la entrega se bloquea sin importar el puntaje):

| Control | Opción |
|---|---|
| Vulnerabilidad crítica (CVSS 9.0–10) | `--critical-vuln` |
| Prueba obligatoria fallida (unitarias, integración, seguridad) | `--failed-test` |
| Criterio obligatorio de la metodología incumplido | `--mandatory-missing` |

**Ejemplos de cálculo:**

| Calificaciones (func, tec, ux, pruebas, seg, doc) | Cálculo | Total | Resultado |
|---|---|---|---|
| 4, 4, 4, 5, 4, 4 | 24 + 16 + 12 + 15 + 12 + 4 | 83 | **No aprobada**: no alcanza 85 |
| 5, 4, 4, 5, 4, 4 | 30 + 16 + 12 + 15 + 12 + 4 | 89 | **Aprobada** |
| 5, 5, 5, 5, 2, 5 | 30 + 20 + 15 + 15 + 6 + 5 | 91 | **No aprobada**: Seguridad < 3 |
| 5, 5, 5, 5, 5, 5 + `--critical-vuln` | 100 | 100 | **No aprobada**: control crítico |

**Dónde se aplica cada cosa:**

- En **G4** solo bloquean los **controles críticos**. Un puntaje preliminar bajo (por ejemplo 83) no impide aprobar G4, pero sí debe corregirse antes del release.
- Al salir de **`aceptacion`** hacia `release` se exige el **scorecard aprobado completo** (≥85, ninguna dimensión <3, sin controles críticos).

**Cómo calificar con justicia.** Cada calificación se justifica con evidencia concreta (resultados de pruebas, informe de seguridad, revisión de UX). Claude puede **proponer** las calificaciones; el evaluador humano las confirma con `--evaluator "Nombre (rol)"`. El resultado se guarda en `scrum-ai/evidence/<ID>/scorecard.json`.

Puede calcular un puntaje sin guardarlo, omitiendo el ID:

```bash
sai.py score --func 4 --tec 4 --ux 4 --pruebas 5 --seg 4 --doc 4
```

---

## 9. Sprints, retrospectivas e indicadores

### 9.1 Ciclo del sprint

- **Duración:** dos semanas.
- **Iniciar:** `sai.py sprint start --goal "<objetivo>"`. Crea `scrum-ai/sprints/sprint-N/plan.md` (historias comprometidas, desglose de tareas, criterios de salida, capacidades a usar, riesgos) y `retro.md`.
- **Durante el sprint:** daily de 15 minutos, actualización del tablero, revisión con agentes de IA, control de calidad y seguridad, gestión en GitHub y documentación de la evidencia.
- **Cerrar:** `sai.py sprint close`. Calcula la predictibilidad (historias en `done` frente a las comprometidas en el sprint).
- **Reportar:** `sai.py report`. Genera `scrum-ai/sprints/reporte-sprint-N.md` con indicadores y el estado de cada historia (gates aprobados y score).

### 9.2 Retrospectiva

Claude completa `scrum-ai/sprints/sprint-N/retro.md` con el equipo: indicadores, qué funcionó, qué mejorar, **aprendizajes sobre el uso de IA** (prompts, skills, MCP, RAG) y acciones para el siguiente sprint. Es el momento de decidir qué capacidades aportaron y cuáles deshabilitar.

### 9.3 Indicadores

| Indicador | Descripción | Meta sugerida |
|---|---|---|
| Cumplimiento del Sprint Goal | Entrega de los objetivos del sprint | ≥ 90% |
| **Predictibilidad** | Historias completadas frente a planificadas (lo calcula `sprint close`) | ≥ 85% |
| Lead time | Desde la solicitud hasta producción | ≤ 10 días |
| Cycle time | Tiempo de desarrollo por historia | ≤ 5 días |
| **First-pass acceptance** | Historias aceptadas sin ningún gate rechazado (lo calcula `report`) | ≥ 80% |
| Retrabajo IA | Historias con retrabajo por hallazgos en código generado con IA | ≤ 15% |
| Defectos escapados | Defectos en producción no detectados en QA | ≤ 5% |
| Frecuencia de despliegue | Despliegues en el periodo | ≥ 1 por semana |
| Satisfacción del equipo | Valoración de 1 a 5 | ≥ 4.0 |

---

## 10. Paquetes de skills integrados

El skill es un **orquestador**: la metodología define *qué* se hace y *quién aprueba*; los skills especializados aportan *cómo* hacerlo mejor en cada fase. Trae precargados 33 skills de tres paquetes y, en Claude Code, la revisión cruzada con Codex.

### 10.1 Los paquetes

| Paquete | Qué aporta | Skills |
|---|---|---|
| **agent-skills** (Addy Osmani) | El proceso de ingeniería de la especificación al release. Es el paquete principal en casi todas las fases | 20 |
| **ecc** (Everything Claude Code) | Verificación con informe PASS/FAIL, pruebas E2E, seguridad, ADR, despliegue y patrones por stack | 12 |
| **diseno-web-integral** | Diseño de UI de punta a punta: diagnóstico, diseño, validación medida y aprobación | 1 |
| **codex** (OpenAI, solo Claude Code) | Revisión cruzada: Codex revisa los resultados de Claude en G1, DoR, G4 y G6 | Revisor |

### 10.2 Qué se ejecuta en cada fase

Claude empieza por los **principales** y suma los **complementarios** solo cuando el caso lo pide (el stack coincide, hay UI, el cambio es sensible en seguridad, etc.).

| Fase | Principal | Complementario |
|---|---|---|
| **Define** | `agent-skills:interview-me`, `agent-skills:spec-driven-development` | `agent-skills:idea-refine`; `ecc:brownfield-retrospective` en Sprint 0 con código existente |
| **Plan** | `agent-skills:planning-and-task-breakdown`, `agent-skills:constraint-driven-development` | `agent-skills:git-workflow-and-versioning` |
| **Design** | `diseno-web-integral` (mockup, G3), `agent-skills:api-and-interface-design`, `agent-skills:documentation-and-adrs` | `agent-skills:frontend-ui-engineering`, `ecc:api-design`, `ecc:architecture-decision-records`, `ecc:accessibility` |
| **Build** | `agent-skills:incremental-implementation`, `agent-skills:test-driven-development` | `ecc:tdd-workflow`, `ecc:backend-patterns`, `ecc:frontend-patterns`, `agent-skills:frontend-ui-engineering` |
| **Verify** | `ecc:verification-loop`, `agent-skills:debugging-and-error-recovery`, `diseno-web-integral` (validación medida de la UI) | `agent-skills:browser-testing-with-devtools`, `ecc:e2e-testing`, `ecc:ai-regression-testing`, `ecc:accessibility`, `agent-skills:performance-optimization` |
| **Review** | `agent-skills:code-review-and-quality`, `agent-skills:security-and-hardening` | `agent-skills:code-simplification`, `ecc:security-review` |
| **Ship** | `agent-skills:ci-cd-and-automation`, `agent-skills:shipping-and-launch` | `ecc:deployment-patterns`, `agent-skills:observability-and-instrumentation`, `agent-skills:documentation-and-adrs` |

Para ver qué hay disponible en una fase y cómo invocarlo:

```bash
sai.py cap for-phase Design
```

```
Capacidades disponibles para la fase Design:
  [skills] dwi-diseno-web-integral     ✔ usar   (principal)      Mockup y diseño UI de punta a punta…
           → invoque el skill «diseno-web-integral» (herramienta Skill) o lea …/SKILL.md
  [skills] as-api-and-interface-design ✔ usar   (principal)      Diseño de APIs y contratos…
  [skills] ecc-api-design              · pendiente_revision (complementario) Patrones REST…
```

### 10.3 Ciclo de vida y aprobación

Cada skill pasa por estos estados:

```
por_configurar → pendiente_revision → aprobado
  (no instalado)   (detectado, sin revisar)  (revisado por una persona)
                                         ↘ deshabilitado
```

**Solo se usan los `aprobado`.** Un skill es código e instrucciones que Claude ejecutará, así que aprobarlo es una decisión humana más, **una vez por proyecto y paquete**.

Antes de pedir la aprobación, Claude lee el `SKILL.md` de los skills del paquete y le resume:

- Qué hace cada uno y en qué fases aporta; si se solapa o contradice la metodología.
- Qué ejecuta: comandos, red, escritura de archivos, variables de entorno, hooks.
- Patrones sensibles detectados.
- Su recomendación: aprobar, aprobar con restricciones o no aprobar.

Comandos:

```bash
sai.py cap approve --pack agent-skills --by "Juan Ruiz (Líder técnico)"   # paquete completo
sai.py cap approve ecc-security-review --by "Pedro Díaz (QA)"              # un skill
sai.py cap disable ecc-backend-patterns                                    # retirar uno
sai.py cap disable --pack ecc                                              # retirar un paquete
sai.py cap list --pack ecc                                                 # ver estados
```

### 10.4 Reglas de convivencia

- **Los gates mandan.** Estos skills traen sus propios flujos y puntos de aprobación; ninguno sustituye un gate. Por ejemplo, la aprobación final de `diseno-web-integral` es evidencia para G3, y G3 se registra igual con nombre y rol de UX/UI, PO y Dueño de proceso.
- **Si un skill choca con la metodología, prevalecen la metodología y `CONSTRAINTS.md`.**
- **Un solo flujo para la misma tarea.** No se corren dos TDD ni dos revisiones en paralelo. Por defecto se usa `agent-skills:test-driven-development`; `ecc:tdd-workflow` cuando el plan técnico exige cobertura ≥80% en unitarias, integración y E2E.
- **Patrones por stack bajo demanda.** ECC trae más de 300 skills, entre ellos skills por tecnología (`django-tdd`, `springboot-security`, `react-testing`, `python-testing`…). Se agregan con `cap add-skill` cuando el stack los justifica (sección 11).
- **Hooks de ECC.** Corren automáticamente en cada herramienta y sesión. No cuentan como evidencia de un gate. Si un hook bloquea algo que la metodología exige, Claude lo reporta en vez de esquivarlo.
- **Evidencia.** Claude menciona en la evidencia qué skill usó en cada artefacto.

### 10.5 Si falta un paquete

Al iniciar, Claude revisa los paquetes y las dependencias de `diseno-web-integral`. Si falta algo, ejecuta `sai.py cap install`, que **solo muestra el plan**:

```text
Plan de instalación (fuentes originales):
  [ecc]
     - claude plugin marketplace add affaan-m/ECC
     - claude plugin install ecc@ecc --scope user (si falla, se copian los skills desde el repositorio)
     - ⚠ Instala hooks que corren en cada herramienta y sesión (perfil 'standard'); …
  [diseno-web-integral]
     - descargar de GitHub e instalar con su scripts/instalar.py: pbakaus/impeccable (Apache-2.0), …

Instalar código de terceros es una decisión humana. Cuando una persona lo autorice:
  python sai.py cap install --yes
```

Si usted lo autoriza, Claude ejecuta `cap install --yes` (o `--pack <paquete> --yes`) y le pide recargar Claude Code. Si el plan incluye `codex login`, ese paso lo hace usted, porque abre el navegador para iniciar sesión. Si no lo autoriza, Claude ejecuta la fase con las referencias del skill: **la metodología no depende de ningún skill externo para funcionar.**

### 10.6 Proyectos creados con una versión anterior

Si `sai.py status` muestra *"El registro de capacidades es de una versión anterior"*, ejecute:

```bash
sai.py cap sync
```

Agrega los paquetes nuevos, retira los marcadores antiguos `ecc-*` que nunca se configuraron y detecta lo instalado. **No toca las decisiones ya registradas.**

Ejecute `sai.py cap detect` cada vez que instale o actualice un plugin: la ruta de instalación cambia con la versión.

### 10.7 Revisión cruzada con Codex (solo en Claude Code)

Cuando el skill corre en **Claude Code**, un segundo modelo, **Codex** (OpenAI), puede revisar lo que produjo Claude en cuatro puntos estratégicos, antes de que una persona decida. Con verificación `completo` lo hace en cada punto; con `ligero` (por defecto), solo cuando usted lo pide, porque cada revisión consume tokens de Codex y alarga el ciclo.

| Punto | Momento | Qué revisa Codex | Comando |
|---|---|---|---|
| **G1** | Historia en `especificacion` | La ficha: ambigüedades, reglas faltantes o contradictorias, criterios no verificables, casos de borde, dependencias | `sai.py xreview <ID> --point G1` |
| **DoR** | Historia en `plan_tecnico` | El plan técnico y los ADR frente a los criterios y el mockup: supuestos riesgosos, contratos de API, datos, seguridad, estimación | `sai.py xreview <ID> --point DoR` |
| **G4** | Historia en `pruebas` | El código del cambio (revisión nativa de Codex sobre el diff) | `sai.py xreview <ID> --point G4 [--base main]` |
| **G6** | Historia en `release` | La preparación del release: rollback, monitoreo, migraciones, configuración, documentación | `sai.py xreview <ID> --point G6` |

Cómo funciona:

- **Requisitos:** el paquete `codex` instalado y aprobado, el CLI de Codex instalado y la sesión iniciada (`codex login`). `cap install --pack codex` deja todo listo salvo el inicio de sesión, que hace usted.
- **Qué hace Codex.** En G1, DoR y G6 hace una revisión de solo lectura (no modifica archivos). En G4 usa su revisión de código. Puede agregar foco: `--focus "permisos por rol"`. Una revisión puede tardar varios minutos.
- **Dónde queda.** La salida se guarda **sin editar** en `scrum-ai/evidence/<ID>/codex-<punto>.md`, y el acta del gate la enlaza.
- **Qué hace Claude con ella.** En la solicitud de aprobación agrega la línea *Revisión cruzada (Codex)*, con cada hallazgo y lo que hizo: corregido (con evidencia), descartado (con razón) o pendiente.
- **Codex revisa, no aprueba.** El gate lo siguen decidiendo las personas del gate, y el script rechaza a "Codex" como aprobador.
- **No bloquea.** Si Codex no está disponible (sin CLI, sin sesión o sin red), Claude lo dice en la solicitud y sigue. El acta registra "No se ejecutó".
- **Recordatorio.** Con verificación `completo`, mientras falte la revisión, `status` y `story move` muestran *"Revisión cruzada pendiente: …"* en el siguiente paso de la historia.
- **Privacidad.** El código y los artefactos revisados se envían a OpenAI con la cuenta de quien inició sesión. Tenga en cuenta `CONSTRAINTS.md` y los datos sensibles antes de aprobar el paquete.
- **En Codex no aplica.** Si el skill corre en Codex, `xreview` informa que no aplica y no hace nada.

### 10.8 Usar el skill desde Codex

El skill funciona igual en Codex. Las diferencias:

| | Claude Code | Codex |
|---|---|---|
| Entorno en los scripts | Se detecta solo | Agregue `--harness codex` antes del comando, o defina `SAI_HARNESS=codex` |
| Paquetes | Plugins y `~/.claude/skills/` | Skills copiados a `~/.agents/skills/`, adaptados a Codex |
| Invocar un skill de la fase | Herramienta Skill (`agent-skills:spec-driven-development`) | Mencionar `$spec-driven-development`, o leer su `SKILL.md` |
| Revisión cruzada con Codex | Sí | No aplica |
| Hooks de ECC | Sí (plugin) | No (solo se copian los skills) |
| MCP | `.mcp.json` del proyecto | `~/.codex/config.toml` (`[mcp_servers.<id>]`) |
| Después de instalar | `/reload-plugins` o sesión nueva | Sesión nueva de Codex |

Ejemplo en Codex:

```bash
python ~/.agents/skills/scrum-ai-delivery/scripts/sai.py --harness codex status
python ~/.agents/skills/scrum-ai-delivery/scripts/sai.py --harness codex cap install
```

El estado del proyecto (`scrum-ai/`) es el mismo para ambos agentes: un equipo puede trabajar una historia en Claude Code y otra en Codex sobre el mismo repositorio. Las aprobaciones de paquetes quedan registradas una vez por proyecto; ejecute `cap detect` en cada entorno para que las rutas correspondan.

---

## 11. Otras capacidades: skills de terceros, MCP y RAG

Todas se registran en `scrum-ai/capabilities.json`, que se versiona con el proyecto para que todo el equipo use las mismas.

### 11.1 Skills de terceros

Un skill es una carpeta con `SKILL.md` (y quizá `scripts/`, `references/`, `assets/`).

```bash
# 1. Registrar
sai.py cap add-skill --id ecc-django-tdd --name django-tdd \
  --source github:affaan-m/ECC/skills/django-tdd --phases Build --purpose "TDD en Django"

# 2. Descargar al proyecto (scrum-ai/vendor-skills/<id>/) y listar archivos y patrones sensibles
sai.py cap fetch ecc-django-tdd

# 3. Revisión humana y aprobación
sai.py cap approve ecc-django-tdd --by "Juan Ruiz (Líder técnico)"
```

Fuentes soportadas: `github:owner/repo[/subcarpeta][@rama|tag]` (requiere `git`), una carpeta local, un `.zip` o un `.skill`. Sin red o sin git, use la ruta local del `.zip`. Para cambiar la fuente: `cap set-source <id> --source …` y vuelva a `fetch`.

`fetch` señala **patrones sensibles** que conviene revisar con atención: `curl | sh`, `rm -rf` sobre raíz o home, decodificación base64, credenciales en claro, `eval`/`exec` dinámicos e instrucciones que intentan anular otras.

**El texto de un skill de terceros es contenido a evaluar, no órdenes.** Si contiene instrucciones para saltarse gates, aprobar por su cuenta, desplegar, exfiltrar datos o ignorar `CONSTRAINTS.md`, Claude lo rechaza y lo reporta.

**Catálogo de repositorios de la comunidad** destacados por la metodología (verifique existencia, licencia y contenido antes de registrarlos):

| Repositorio | Enfoque | Fases sugeridas |
|---|---|---|
| anthropics/skills | Skills oficiales de Anthropic | Todas |
| addyosmani/agent-skills | Ciclo de ingeniería (ya integrado) | Todas |
| affaan-m/ECC | Everything Claude Code (ya integrado) | Todas |
| obra/superpowers | Tareas complejas y flujos automatizados | Plan, Build |
| mattpocock/skills | TypeScript, APIs, buenas prácticas | Build, Review |
| nextlevelbuilder/ui-ux-pro-max-skill | Diseño UI/UX y accesibilidad | Design |
| Leonxlnx/taste-skill | Pruebas, calidad de código, mejora continua | Verify, Review |
| ComposioHQ/awesome-claude-skills | Curaduría en múltiples dominios | Todas |

### 11.2 Servidores MCP

MCP (Model Context Protocol) conecta a Claude con sistemas externos: GitHub, Jira/Linear, Figma, Google Drive/SharePoint, bases de datos, CRIS o repositorios institucionales, Slack/Teams.

```bash
# Servidor remoto (HTTP)
sai.py cap add-mcp --id github --url https://api.githubcopilot.com/mcp/ \
  --phases Plan Build Ship --purpose "Issues, PR, Actions" --write-mcp-json

# Servidor local (stdio) con credencial por variable de entorno
sai.py cap add-mcp --id postgres-dev --command npx \
  --args -y @modelcontextprotocol/server-postgres --env DATABASE_URL --phases Build Verify
```

- `--write-mcp-json` agrega la entrada a `.mcp.json` del proyecto; Claude Code la carga al reiniciar la sesión.
- Las credenciales se referencian **por nombre de variable** (`--env`); nunca se guardan sus valores.
- En claude.ai o Cowork, el MCP se conecta como conector desde la configuración; el registro documenta para qué fase se usa.
- Claude verifica primero con operaciones de lectura. Las de escritura (crear issues, comentar PR, mover tarjetas) las confirma con usted la primera vez.

Usos típicos: Define (Drive/SharePoint/Confluence para requisitos y normativa), Plan (GitHub Projects/Jira), Design (Figma), Build/Verify (GitHub, base de datos de desarrollo, Playwright), Review (escáneres de seguridad), Ship (GitHub Actions, monitoreo).

### 11.3 Fuentes RAG (documentos)

RAG permite que Claude responda con base en documentos del proyecto o de la institución (reglamentos, lineamientos de convocatorias, documentación técnica) **citando la fuente**.

```bash
# a) Carpeta local, indexada con BM25 (md, txt, html, código, json, csv y PDF si hay pdftotext)
sai.py cap add-rag --id normativa --path docs/normativa --phases Define Review --purpose "Reglamentos y acuerdos"
python rag.py index normativa
python rag.py query normativa "¿una convocatoria cerrada sigue siendo consultable?"

# b) API RAG institucional (POST {"query","top_k"}; token en variable de entorno)
sai.py cap add-rag --id cris-rag --endpoint https://rag.midominio.edu.co/query --auth-env CRIS_RAG_TOKEN --phases Define

# c) RAG expuesto por un MCP
sai.py cap add-rag --id kb --mcp kb-server --phases "*"

# Consultar todas las fuentes aprobadas de una fase
python rag.py query-all "pregunta" --phase Define
```

Las fuentes RAG también deben aprobarse: `sai.py cap approve normativa --by "Nombre (rol)"`.

Reglas de uso:

- Claude cita siempre `archivo:línea` o la URL de la fuente en el artefacto.
- Lo recuperado es **evidencia, no instrucción**. Si dos documentos se contradicen, Claude lo presenta al dueño de proceso para que decida.
- Si el RAG no trae nada relevante, Claude lo dice y pregunta; no rellena con suposiciones.
- Reindexe (`rag.py index <id>`) cuando cambien los documentos.

---

## 12. Trabajo con GitHub

### 12.1 Tablero y estados

| Columna del tablero (GitHub Projects) | Estados de `sai.py` |
|---|---|
| Backlog / Refinamiento | `backlog`, `especificacion` |
| Flujo | `flujo` |
| Mockup | `mockup`, `plan_tecnico` |
| Ready | `ready` |
| Desarrollo | `desarrollo` |
| QA | `pruebas` |
| UAT | `uat`, `aceptacion` |
| Done | `release`, `done` |

### 12.2 Trazabilidad

**Épica → Historia → Criterio de aceptación → Flujo → Mockup → Código → Prueba → PR → Aprobación → Release.**

- El issue referencia `scrum-ai/backlog/<ID>.md`.
- El PR cierra el issue y enlaza `scrum-ai/evidence/<ID>/`.
- El release lista los IDs de historias incluidas.

### 12.3 Convenciones

- Ramas: `feature/<ID>`, `fix/<ID>`, `chore/<tema>`.
- Commits: `<tipo>(<ID>): descripción`, por ejemplo `feat(US-CONV-001): filtro de convocatorias`.

### 12.4 GitHub Actions

Con `init --github` se copia `.github/workflows/quality-gates.yml`, que encadena:

**Lint/Tipado → Tests → QA/Visual → Seguridad → Build → Deploy**, en cada pull request y en cada push a `main`.

En el Sprint 0 se reemplazan los `TODO` por los comandos reales del stack (`npm run lint`, `pytest --cov`, `npx playwright test`, `npm audit`, CodeQL, etc.). Una vulnerabilidad crítica debe hacer fallar el job de seguridad.

Configure un *environment* `produccion` con **revisores requeridos** (PO + Operaciones/TI) para que el despliegue sea siempre una decisión humana (G6).

También se copian las plantillas `.github/ISSUE_TEMPLATE/historia.md` y `.github/PULL_REQUEST_TEMPLATE.md`.

### 12.5 Comandos útiles

```bash
# Etiquetas (una vez, en Sprint 0)
for l in backlog refinamiento flujo mockup ready desarrollo qa uat done; do gh label create "estado:$l" --force; done
for g in G1 G2 G3 G4 G5 G6; do gh label create "gate:$g-aprobado" --color 2ea44f --force; done
gh label create historia --force

# Issue desde la ficha
gh issue create --title "US-CONV-001: Consultar convocatorias" \
  --body-file scrum-ai/backlog/US-CONV-001.md --label historia,estado:backlog

# Cambiar estado y registrar gate
gh issue edit <n> --remove-label estado:flujo --add-label estado:mockup --add-label gate:G2-aprobado

# Rama y PR
git switch -c feature/US-CONV-001
gh pr create --fill --body-file .github/PULL_REQUEST_TEMPLATE.md
```

Crear issues, etiquetas o PR modifica un repositorio compartido: Claude lo confirma con usted la primera vez.

---

## 13. Archivos que crea el skill

Después de `init` y algunas historias, el proyecto queda así:

```
<su proyecto>/
├── AGENTS.md                         # Guía para agentes de IA (Sprint 0)
├── CONSTRAINTS.md                    # Restricciones y límites (Sprint 0)
├── .mcp.json                         # Servidores MCP (si usa --write-mcp-json)
├── .github/                          # Solo con --github
│   ├── ISSUE_TEMPLATE/historia.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/quality-gates.yml
└── scrum-ai/
    ├── state.json                    # Estado: fase, sprint, historias, gates, log de eventos
    ├── capabilities.json             # Registro de skills, MCP y RAG
    ├── dor-dod.md                    # Definición de DoR y DoD del equipo
    ├── vision/
    │   ├── vision.md                 # Visión y estrategia
    │   └── roles-raci.md             # Roles y matriz RACI
    ├── audit/auditoria.md            # Solo en modo existente
    ├── backlog/<ID>.md               # Ficha de cada historia
    ├── design/<ID>/
    │   ├── flujo.md                  # Se crea al pasar a 'flujo'
    │   └── diseno-ui.md              # Se crea al pasar a 'mockup'
    ├── evidence/<ID>/
    │   ├── G1.md … G6.md             # Actas de cada gate
    │   ├── codex-<punto>.md          # Revisión cruzada de Codex (G1, DoR, G4, G6; Claude Code)
    │   └── scorecard.json
    ├── adr/ADR-001-<titulo>.md       # Decisiones de arquitectura
    ├── sprints/
    │   ├── sprint-N/plan.md
    │   ├── sprint-N/retro.md
    │   └── reporte-sprint-N.md
    ├── vendor-skills/<id>/           # Skills descargados con cap fetch
    └── rag/                          # Índices de las fuentes RAG locales
```

**Versione toda la carpeta `scrum-ai/` en Git.** Así el estado, las actas y el registro de capacidades son compartidos y auditables. `state.json` es el que lee el script: edítelo solo con los comandos.

### Plantillas incluidas

| Plantilla | Se usa en |
|---|---|
| `vision.md` | Visión y MVP (Sprint 0) |
| `roles-raci.md` | Roles y RACI (Sprint 0) |
| `dor-dod.md` | Criterios de entrada y salida |
| `AGENTS.md`, `CONSTRAINTS.md` | Reglas para agentes (Sprint 0) |
| `auditoria-sprint0.md` | Auditoría de código existente |
| `historia-usuario.md` | Ficha de historia (G1) |
| `flujo.md` | BPMN y estados de interfaz (G2) |
| `diseno-ui.md` | Wireframe, mockup, prototipo y estados (G3) |
| `adr.md` | Decisiones de arquitectura |
| `sprint-plan.md`, `retrospectiva.md` | Inicio y cierre de sprint |

---

## 14. Referencia de comandos

Ejecute todos los comandos desde la raíz del proyecto: `python <carpeta del skill>/scripts/sai.py <comando>`. Para ver la ayuda de cualquiera: `sai.py <comando> -h`.

Opción global: `sai.py --harness claude|codex <comando>` fija el entorno (por defecto se detecta; en Codex use `--harness codex`). También puede definir la variable `SAI_HARNESS`.

### 14.1 Proyecto y roadmap

| Comando | Qué hace |
|---|---|
| `init --name N --mode nuevo\|existente [--github] [--tests-in sandbox\|rama\|proyecto] [--tests-path R] [--profile esencial\|estandar\|completo] [ajustes] [--path P] [--force]` | Crea `scrum-ai/`, `AGENTS.md`, `CONSTRAINTS.md` y plantillas; con `--github`, las de GitHub. Detecta los paquetes de skills. Registra el lugar de las pruebas y el perfil (`estandar` por defecto). `--force` reinicializa |
| `config [--profile P] [--skills ninguno\|principal\|todos] [--skip-stages flujo,mockup,uat\|ninguno] [--design basico\|integral] [--detail breve\|completo] [--verify ligero\|completo] [--tests-in …] [--tests-path R] [--approver "Nombre (rol)"\|ninguno]` | Muestra o cambia el perfil, sus ajustes, el nivel de verificación, el lugar de las pruebas y el aprobador del chat. Los mismos ajustes sirven en `init` |
| `status` | Entorno, nivel de verificación, lugar de las pruebas, fase, sprint, entregables del Sprint 0 pendientes, historias con su siguiente paso y capacidades pendientes de revisión |
| `phase` | Muestra el roadmap S0–S6 y marca la fase actual |
| `phase --set S1 --approver "Nombre (PO)" [--force]` | Avanza de fase (una a la vez; desde S0 exige el Sprint 0 completo) |
| `sprint0` | Checklist de entregables del Sprint 0 |
| `sprint0 <clave> [--evidence ruta] [--undo]` | Marca o desmarca un entregable |
| `audit <Componente> --state 1-5 --value 1-5 [--action A] [--notes "…"]` | Registra la evaluación de un componente |
| `audit` | Tabla de la auditoría y distribución por acción |
| `adr "<título>"` | Crea `scrum-ai/adr/ADR-NNN-<titulo>.md` |

### 14.2 Sprints e historias

| Comando | Qué hace |
|---|---|
| `sprint start --goal "…"` | Inicia el siguiente sprint (dos semanas) y crea su plan y retrospectiva |
| `sprint close` | Cierra el sprint y calcula la predictibilidad |
| `report` | Genera el reporte del sprint con indicadores |
| `story add <ID> "<título>" [--epic E] [--skip flujo,mockup,uat\|ninguno]` | Crea la historia en `backlog` con su ficha. Por defecto omite las etapas que fija el perfil |
| `story skip <ID> --skip flujo,mockup,uat\|ninguno` | Cambia las etapas omitidas de una historia (no afecta etapas en curso o superadas) |
| `story list` | Lista historias con estado y sprint |
| `story show <ID>` | Muestra todo el registro de la historia y su siguiente paso |
| `story move <ID> <estado> [--reason "…"]` | Avanza un estado (con validación) o retrocede (con motivo) |
| `dor <ID> [ítems…] [--undo] [--no-advance]` | Muestra o marca ítems de DoR; al completarlo, la historia pasa a `ready` |
| `dod <ID> [ítems…] [--undo]` | Muestra o marca ítems de DoD |

Estados válidos: `backlog`, `especificacion`, `flujo`, `mockup`, `plan_tecnico`, `ready`, `desarrollo`, `pruebas`, `uat`, `aceptacion`, `release`, `done`.

### 14.3 Gates y calidad

| Comando | Qué hace |
|---|---|
| `gate <G#>` | Muestra la definición del gate |
| `gate <ID[,ID…]> <G#[,G#…]> --decision aprobado\|rechazado [--approver "Nombre (rol)" …] [--evidence <ruta\|URL> …] [--notes "…"] [--no-advance] [--force]` | Registra la decisión humana (una o varias historias, uno o varios gates seguidos), genera un acta por gate y avanza la historia. Sin `--approver` usa el aprobador registrado; sin `--evidence`, G1–G3 usan la ficha, el flujo o el mockup si ya están completos |
| `xreview <ID> --point G1\|DoR\|G4\|G6 [--focus "…"] [--base main]` | Revisión cruzada de Codex (solo Claude Code); guarda `scrum-ai/evidence/<ID>/codex-<punto>.md` |
| `score [ID] --func N --tec N --ux N --pruebas N --seg N --doc N [--critical-vuln] [--failed-test] [--mandatory-missing] [--evaluator "Nombre (rol)"]` | Calcula el scorecard; con ID lo guarda en la historia |

### 14.4 Capacidades

| Comando | Qué hace |
|---|---|
| `cap list [--kind skills\|mcp\|rag] [--pack P]` | Lista capacidades con estado, fases y nombre de invocación |
| `cap for-phase <Fase> [--all]` | Capacidades de la fase que aplican al perfil (principales primero) y cómo usarlas. `--all` muestra también las omitidas |
| `cap detect` | Detecta los skills nativos instalados |
| `cap install [--pack P]` | Muestra el plan para instalar lo que falte desde los repositorios originales (y la copia incluida de diseno-web-integral) |
| `cap install [--pack P] --yes` | Ejecuta ese plan |
| `cap sync` | Actualiza el registro de un proyecto antiguo |
| `cap approve <id> --by "Nombre (rol)"` | Aprueba una capacidad |
| `cap approve --pack P --by "Nombre (rol)"` | Aprueba todos los skills instalados de un paquete |
| `cap disable <id>` / `cap disable --pack P` | Deshabilita una capacidad o un paquete |
| `cap add-skill --id I --name N --source S --phases F… [--purpose "…"]` | Registra un skill de terceros |
| `cap fetch <id>` | Descarga el skill a `scrum-ai/vendor-skills/<id>/` |
| `cap set-source <id> --source S` | Cambia la fuente de un skill |
| `cap add-mcp --id I --url U \| --command C [--args …] [--env VAR…] --phases F… [--write-mcp-json]` | Registra un servidor MCP |
| `cap add-rag --id I --path P \| --endpoint U [--auth-env VAR] \| --mcp M --phases F…` | Registra una fuente RAG |

Fases válidas: `Define`, `Plan`, `Design`, `Build`, `Verify`, `Review`, `Ship` o `"*"` (todas). Paquetes: `agent-skills`, `ecc`, `diseno-web-integral` y, en Claude Code, `codex`.

### 14.5 RAG (`rag.py`)

| Comando | Qué hace |
|---|---|
| `python rag.py index <id>` | Indexa una fuente RAG local |
| `python rag.py query <id> "pregunta" [-k 5] [--json]` | Consulta una fuente y devuelve fragmentos citables |
| `python rag.py query-all "pregunta" --phase <Fase> [-k N]` | Consulta todas las fuentes aprobadas de la fase |

---

## 15. Solución de problemas y preguntas frecuentes

### Mensajes del script

| Mensaje | Qué significa | Qué hacer |
|---|---|---|
| `Bloqueado: salir de '<estado>' requiere G# … aprobado por humanos` | Falta el gate de ese estado | Prepare la evidencia y pida la aprobación a los roles del gate |
| `Bloqueado por Definition of Ready. Falta: …` | Faltan ítems de DoR | Complete los ítems con `sai.py dor <ID> …` |
| `Bloqueado por Definition of Done. Falta: …` | Faltan ítems de DoD | Complete los ítems con `sai.py dod <ID> …` |
| `Bloqueado: el scorecard debe estar aprobado (≥85/100…)` | El scorecard final no aprueba | Corrija lo que baja la calificación y recalcule con evidencia |
| `No se puede saltar de 'X' a 'Y'. Avance un estado a la vez.` | Intentó saltar estados | Mueva la historia paso a paso |
| `Retroceder requiere --reason` | Retrocedió sin motivo | Agregue `--reason "…"` |
| `'<nombre>' parece un agente de IA…` | El aprobador parece un agente | Registre el nombre y rol de la persona. Si es una persona cuyo nombre o rol contiene "IA" (por ejemplo, "Equipo IA"), escriba el rol de otra forma, como "Coordinación de inteligencia artificial" |
| `Un gate no se aprueba sin evidencia` | Faltó `--evidence` | Agregue al menos una ruta o URL |
| `Evidencia no encontrada: …` | La ruta no existe | Use rutas relativas a la raíz del proyecto o URLs completas |
| `G# se decide cuando la historia está en '<estado>'` | El gate no corresponde al estado actual | Mueva la historia al estado correcto |
| `G4 no puede aprobarse: hay un control crítico fallido` | El scorecard tiene un control crítico | Corrija la vulnerabilidad o la prueba y recalcule el scorecard sin el control |
| `Sprint 0 incompleto (…)` | Pendientes al pasar de S0 a S1 | Complete los entregables o use `--force` con decisión del PO |
| `No se encontró ./scrum-ai/state.json` | No está en la raíz del proyecto o no se inicializó | Cambie a la raíz del proyecto o ejecute `init` |
| `Instale o descargue y revise el skill antes de aprobarlo` | El skill no está instalado ni descargado | Instale el paquete y ejecute `cap detect`, o use `cap fetch` |
| `El registro de capacidades es de una versión anterior` | Proyecto creado antes de los paquetes integrados | Ejecute `cap sync` |

### Preguntas frecuentes

**¿Puedo usar el skill en Codex?**
Sí. Instálelo en `~/.agents/skills/scrum-ai-delivery` y use `--harness codex` en los comandos (sección 10.8). La revisión cruzada no aplica en Codex.

**`xreview` dice "Falta el CLI de Codex" o Codex pide sesión.**
Instale el CLI con `npm install -g @openai/codex` (o con `cap install --pack codex --yes`) e inicie sesión con `codex login`. Si no quiere usar la revisión cruzada, deshabilite el paquete: `cap disable --pack codex`.

**El script detectó el entorno equivocado.**
Fíjelo con `sai.py --harness claude|codex …` o con la variable `SAI_HARNESS`. La línea "Entorno" de `status` muestra el entorno detectado.

**¿Puedo usar la metodología sin los paquetes de skills?**
Sí. Si no hay skills aprobados para una fase, Claude la ejecuta con las referencias del propio skill.

**¿Por qué Claude no aprueba aunque se lo pida?**
Es el primer principio de la metodología: los agentes ejecutan, no aprueban. El script también lo impide. Dé el nombre y rol de la persona que aprueba.

**Una sola persona tiene varios roles. ¿Cómo apruebo?**
Registre a la persona una vez por rol, por ejemplo `--approver "Ana Pérez (PO)" --approver "Ana Pérez (Dueña de proceso)"`. Conviene dejarlo explícito en la matriz RACI.

**¿Qué pasa si un gate se rechaza?**
Queda el acta con el rechazo y las observaciones. Claude ajusta el artefacto y lo vuelve a presentar. Si hace falta, la historia retrocede a un estado anterior con `--reason`. Un rechazo afecta el indicador de *first-pass acceptance*.

**¿Puedo corregir una aprobación registrada por error?**
Vuelva a registrar el gate con la decisión correcta y una nota que explique la corrección. El acta se actualiza y el log de `state.json` conserva ambas decisiones.

**¿Dónde quedan las aprobaciones de los paquetes de skills?**
En `scrum-ai/capabilities.json`, con `aprobado_por` y `aprobado_fecha` en cada skill.

**ECC hace que todo vaya más lento.**
Sus hooks corren en cada herramienta. Cambie el perfil a `minimal` o desactívelos con `/plugin configure ecc@ecc`; los skills de ECC siguen funcionando.

**`cap install` falla al clonar con "Filename too long" o "invalid index-pack output".**
Windows limita la longitud de las rutas. `cap install` ya clona con `core.longpaths`. Si el error aparece al instalar el plugin con el CLI, active las rutas largas una vez con `git config --global core.longpaths true` y vuelva a intentarlo. También puede instalar desde una carpeta de configuración con una ruta más corta.

**`cap detect` no encuentra skills que tengo en `~/.agents/skills`.**
Esa carpeta es de Codex, y Claude Code no la carga. Dentro de Claude Code el skill solo cuenta lo que Claude Code puede usar; instale el paquete con `cap install`.

**Instalé un paquete pero `cap for-phase` no lo muestra como usable.**
Ejecute `cap detect` (pasa de `por_configurar` a `pendiente_revision`) y luego apruébelo con `cap approve --pack …`. En Claude Code, recargue con `/reload-plugins` para que la herramienta Skill lo vea.

**Actualicé un plugin y ahora la ruta del skill no existe.**
Las rutas de los plugins incluyen la versión. Ejecute `cap detect` para actualizarlas.

**`sai.py` falla con "badly formed help string".**
Es un error de versiones antiguas del skill con Python 3.14. Actualice el skill (sección 17).

**¿El skill envía mis datos a algún servicio?**
`sai.py` y `rag.py` trabajan en local con la biblioteca estándar de Python. Solo hay red cuando usted lo configura: `cap fetch` desde GitHub, una fuente RAG HTTP o un servidor MCP. Los tokens se leen de variables de entorno y no se guardan.

**¿Puedo usarlo para proyectos que no son del Ecosistema de Investigación?**
Sí. La metodología sirve para cualquier producto digital, plataforma, servicio o iniciativa institucional; el Ecosistema de Investigación es el portafolio de referencia.

---

## 16. Glosario

| Término | Significado |
|---|---|
| **ADR** | *Architecture Decision Record*: registro de una decisión técnica con contexto, opciones, decisión y consecuencias |
| **Agent Skill** | Paquete de instrucciones (y a veces scripts) que enseña a un agente de IA a hacer una tarea especializada |
| **BPMN** | Notación estándar para diagramas de procesos de negocio |
| **Capacidad** | Skill, servidor MCP o fuente RAG registrado en `capabilities.json` |
| **CVSS** | Escala de severidad de vulnerabilidades (0–10). 9.0–10 es crítica |
| **DAST / SAST** | Análisis de seguridad dinámico (aplicación en ejecución) y estático (código fuente) |
| **DoR** | *Definition of Ready*: condiciones para que una historia entre a desarrollo |
| **DoD** | *Definition of Done*: condiciones para dar una historia por terminada |
| **Gate** | Puerta de aprobación humana con evidencia (G1–G6) |
| **Entorno (harness)** | Programa que ejecuta al agente: Claude Code o Codex |
| **Hook** | Script que Claude Code ejecuta automáticamente ante ciertos eventos (usar una herramienta, iniciar sesión) |
| **MCP** | *Model Context Protocol*: protocolo para conectar a Claude con sistemas externos |
| **Mermaid** | Lenguaje de texto para generar diagramas |
| **MVP** | Producto mínimo viable: la primera versión funcional |
| **Plugin** | Forma de instalar en Claude Code un conjunto de skills, comandos, agentes y hooks |
| **RACI** | Matriz de responsabilidades: Responsable, Aprobador (*Accountable*), Consultado, Informado |
| **RAG** | *Retrieval-Augmented Generation*: respuestas basadas en documentos recuperados, con cita de la fuente |
| **Revisión cruzada** | Revisión que hace un segundo modelo (Codex) de lo que produjo Claude, antes de la decisión humana de un gate |
| **Scorecard** | Calificación ponderada de calidad de una historia (umbral 85/100) |
| **Spec-Driven Development** | Desarrollo guiado por especificaciones: definir antes de programar |
| **Sprint** | Iteración de trabajo de dos semanas |
| **TDD** | *Test-Driven Development*: escribir la prueba que falla antes que el código |
| **UAT** | *User Acceptance Testing*: pruebas de aceptación con usuarios clave |
| **Vibecoding controlado** | Desarrollo asistido por IA dentro de un microciclo con plan, pruebas, revisión y evidencia |

---

## 17. Mantener y actualizar el skill

### Actualizar

Si instaló el skill con `git clone`:

```bash
cd ~/.claude/skills/scrum-ai-delivery
git pull
```

Después, en cada proyecto existente:

```bash
sai.py status        # avisa si el registro de capacidades necesita actualizarse
sai.py cap sync      # agrega lo nuevo sin tocar las decisiones registradas
```

Para los paquetes de skills: `claude plugin update agent-skills@addy-agent-skills`, `claude plugin update ecc@ecc` y `claude plugin update codex@openai-codex` (o desde `/plugin`), y luego `sai.py cap detect`. En Codex, borre las carpetas de `~/.agents/skills/` que quiera renovar y vuelva a ejecutar `cap install --harness codex --yes`. Para `diseno-web-integral`, actualice la copia en `vendor/diseno-web-integral/` y reemplace la instalada en `~/.claude/skills/`.

### Contenido del repositorio del skill

| Ruta | Contenido |
|---|---|
| `SKILL.md` | Instrucciones que sigue Claude |
| `MANUAL.md` | Este manual |
| `references/` | Metodología, Sprint 0, ciclo de sprint, quality gates, vibecoding, GitHub y capacidades externas |
| `assets/templates/` | Plantillas de artefactos |
| `assets/github/` | Plantillas de issue, PR y workflow |
| `assets/capabilities.default.json` | Registro inicial de paquetes y skills |
| `scripts/sai.py` | CLI de la metodología |
| `scripts/rag.py` | Conector RAG |
| `vendor/diseno-web-integral/` | Copia incluida del skill propietario diseno-web-integral, con su instalador de dependencias |
| `agents/openai.yaml` | Nombre visible y descripción del skill en Codex |

### Personalizar para su institución

- **Paquetes y fases:** edite `assets/capabilities.default.json` (rol `principal` o `complementario`, fases y propósito). Los proyectos nuevos lo toman al hacer `init`; los existentes, con `cap sync`.
- **Plantillas:** edite los archivos de `assets/templates/`. Use `{{PROYECTO}}`, `{{FECHA}}`, `{{ID}}` y `{{TITULO}}` como marcadores.
- **Restricciones institucionales:** ajuste `assets/templates/CONSTRAINTS.md` para que todos los proyectos nuevos las hereden.

### Reportar problemas o sugerir mejoras

Abra un issue en <https://github.com/vmrojasl/Scrum-AI-Delivery/issues> con la versión de Python, el comando que ejecutó y el mensaje completo.
