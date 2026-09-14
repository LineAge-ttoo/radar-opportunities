# ESTADO DEL PROYECTO: RADAR
**Fecha de última actualización:** 2026-09-13  
**Root Canónico:** `C:\Radar`  
**Estado General:** OPERATIVO / V1 IMPLEMENTADO Y VERIFICADO  

---

## 1. OBJETIVO DEL PROYECTO
RADAR es un motor personal de inteligencia de oportunidades para descubrir, analizar, puntuar, almacenar y presentar opciones legítimas de generación de ingresos mediante:
- Programación & Automatización (Python, JavaScript/TypeScript, n8n, APIs, bots, scraping legal)
- Inteligencia Artificial & Agentes (LLMs, agentes autónomos, integraciones)
- Desarrollo Web & Aplicaciones
- Desarrollo 3D & Gaming (Blender, Unity, Roblox)
- Diseño Digital & UI/UX
- Tareas técnicas pagadas, freelance, contratos, bounties y proyectos cortos
- **Construir y Vender**: Detección de problemas repetitivos y demanda desatendida para empaquetar soluciones de software reutilizables.

### Dos Clases Principales de Oportunidades:
- **Clase A: Dinero Publicado**: Ofertas directas de trabajo, contrato, bounty o pago explícito.
- **Clase B: Demanda Detectada**: Señales públicas de dolor o ineficiencia para construir y vender herramientas.

---

## 2. VERSIONES Y ENTORNO DEL SISTEMA
- **Sistema Operativo:** Windows 11 / Windows Server (PowerShell 5.1 / UTF-8)
- **Node.js:** v24.15.0
- **npm:** 11.12.1
- **Git:** 2.55.0.windows.2
- **Python:** 3.14.6
- **n8n:** 2.38.7 (Instalación local en `C:\Radar\n8n`, datos en `C:\Radar\n8n\instance\.n8n`)
- **Editor Local n8n:** `http://127.0.0.1:5678` (Activo y respondiendo)

---

## 3. ARQUITECTURA ACTUAL DE ARCHIVOS

```
C:\Radar
│   .gitignore                        -> Exclusiones seguras de git (node_modules, cache, logs)
│   PROJECT_STATE.md                  -> Estado canónico del proyecto (este archivo)
│   README.md                         -> Resumen general del pipeline
│   START_RADAR.bat                   -> Lanzador bat para iniciar n8n
│   START_RADAR.ps1                   -> Lanzador powershell con variables seguras
│
├── config
│   ├── radar.config.json             -> Configuración global de rutas, umbrales y seguridad
│   ├── scoring
│   │   └── scoring_rules.json        -> Reglas de habilidades, señales y pesos del scoring
│   └── sources
│       └── sources.json              -> Definición y parámetros de colectores activos
│
├── data
│   ├── archive                       -> Histórico de scans anteriores
│   ├── incoming                      -> Respuestas JSON crudas por colector para auditoría
│   ├── opportunities
│   │   ├── latest_scan.json          -> Snapshot completo del último scan
│   │   ├── opportunities.jsonl       -> Stream append-only para auditoría continua
│   │   └── radar.db                  -> Base SQLite maestra de oportunidades (ACID / WAL)
│   └── rejected                      -> Registro de oportunidades descartadas
│
├── docs
│   ├── DECISIONS.md                  -> Registro de Decisiones de Arquitectura (ADR)
│   └── RADAR_02_DEMAND_DETECTION_SPEC.md -> Especificación para detección de demanda
│
├── exports
│   ├── RADAR_SCAN_LATEST.html        -> Dashboard web responsivo para consulta móvil y local
│   ├── RADAR_SCAN_LATEST.md          -> Reporte detallado en Markdown
│   └── RADAR_SUMMARY.json            -> Resumen métrico del último scan
│
├── logs
│   └── radar.log                     -> Logs de ejecución
│
├── n8n
│   ├── backup
│   │   └── RADAR_01_DISCOVERY_v0.json-> Respaldo del workflow original
│   ├── instance
│   │   └── .n8n
│   │       └── database.sqlite       -> Base interna de n8n (workflows y usuarios)
│   └── workflows
│       ├── RADAR_01_DISCOVERY.json   -> Workflow v1 normalizado y probado
│       └── RADAR_02_DEMAND_DETECTION.json -> Workflow v1 de demanda latente
│
└── scripts
    ├── analyzers
    │   ├── normalizer.py             -> Normalización a esquema canónico (limpieza HTML, sueldos)
    │   └── scoring_engine.py         -> Motor de puntuación (fit, dinero, confianza, reusabilidad)
    ├── collectors
    │   ├── arbeitnow_collector.py    -> Colector API de Arbeitnow
    │   ├── collector_manager.py      -> Orquestador tolerante a fallos de colectores
    │   ├── github_bounties_collector.py -> Colector API de GitHub Issues Bounties
    │   └── remotive_collector.py     -> Colector API de Remotive
    ├── run_radar_scan.py             -> Script maestro de escaneo integral
    └── utilities
        ├── db.py                     -> Módulo de persistencia SQLite y JSONL
        ├── presenter.py              -> Generador de reportes Markdown y HTML responsivo
        ├── register_radar02.py       -> Registro sincronizado de workflows en SQLite de n8n
        └── update_n8n_workflow.py    -> Sincronizador de RADAR_01 en SQLite de n8n
```

---

## 4. WORKFLOWS REGISTRADOS EN N8N
1. **`RADAR_01_DISCOVERY` (ID: `RADAR01DISCOV01`)**:
   - **Trigger:** Manual (`ESCANEAR AHORA`)
   - **Nodo HTTP:** Descarga de ofertas de Remotive (`https://remotive.com/api/remote-jobs`)
   - **Nodo Código:** Motor normalizador, cálculo de 5 dimensiones de score, clasificación en `PRIORIDAD`, `CONSTRUIR_Y_VENDER`, `INVESTIGAR`, `OBSERVAR`, `DESCARTAR`, y separación entre datos observados y estimados.
   - **Estado en n8n:** Registrado y visible en el editor local en `http://127.0.0.1:5678`.

2. **`RADAR_02_DEMAND_DETECTION` (ID: `RADAR02DEMAND01`)**:
   - **Trigger:** Manual (`DETECCION DE DEMANDA MANUAL`)
   - **Nodo HTTP:** Captura de señales públicas en foros de discusión y automatización
   - **Nodo Código:** Extractor de fricción operativa y generador de propuestas de software reutilizable.
   - **Estado en n8n:** Registrado y visible en el editor local.

---

## 5. COLECTORES Y FUENTES ACTIVAS
- **Remotive (`remotive_collector.py`)**: API pública y legal de empleos tecnológicos remotos.
- **Arbeitnow (`arbeitnow_collector.py`)**: API pública de empleo con foco en tech, desarrollo e ingeniería remota.
- **GitHub Bounties (`github_bounties_collector.py`)**: Búsqueda pública por API de GitHub de issues abiertas con etiqueta `bounty` en repositorios de código abierto.

---

## 6. ESQUEMA DE DATOS CANÓNICO
Cada oportunidad persistida en `radar.db` contiene:
- `opportunity_id` (Identificador determinístico único)
- `source` & `source_url` (Fuente y enlace original intacto)
- `discovered_at` & `published_at`
- `title`, `organization`, `category`, `opportunity_type`, `location`, `remote`
- `payment_min`, `payment_max`, `currency` (Números reales parseados; `NULL` si no están publicados)
- `skills` (Lista JSON de tecnologías coincidentes)
- `raw_data` (Snippet original de la fuente)
- `observed_data` (Datos fácticos textuales comprobados en la oferta)
- `estimated_data` (Estimación analítica de RADAR: horas, dificultad, potencial económico, nivel de competencia, viabilidad de automatización)
- `fit_score`, `money_score`, `difficulty_score`, `trust_score`, `reusability_score`, `scalability_score`, `competition_score`, `overall_score`
- `decision` (`PRIORIDAD`, `INVESTIGAR`, `OBSERVAR`, `DESCARTAR`, `CONSTRUIR_Y_VENDER`)
- `reasoning` (Explicación honesta de 1 a 2 líneas de por qué fue seleccionada o clasificada)
- `next_action` (Paso táctico inmediato recomendado)

---

## 7. BLOQUEOS
- **Ninguno actualmente.** Todo el pipeline corre de punta a punta de forma desatendida.

---

## 8. DEUDA TÉCNICA REGISTRADA
- **Advertencia de Docker en n8n:** n8n 2.38.7 emite una advertencia de que versiones futuras requerirán Docker. Actualmente opera de forma local y estable sobre Node.js 24 en Windows. No se migrará a Docker hasta que sea estrictamente indispensable y aprobado por el usuario.
- **Concurrencia en SQLite de n8n:** Cuando n8n está arrancando o ejecutando, la base interna `C:\Radar\n8n\instance\.n8n\database.sqlite` adquiere bloqueos de lectura/escritura. Las operaciones sobre esa base deben realizarse de forma atómica o con el servicio detenido. La base de oportunidades `data/opportunities/radar.db` es independiente y opera en WAL sin interferir con n8n.
- **Límites de Rate Limit en APIs públicas sin autenticación:** La API de búsqueda de GitHub sin token tiene un límite de 10 requests por minuto. Si se escala la frecuencia de escaneo de bounties, se requerirá configurar un `GITHUB_TOKEN` opcional en `config/sources/sources.json`.

---

## 9. PRÓXIMOS PASOS RECOMENDADOS
1. Probar la ejecución manual del workflow desde la interfaz web de n8n (`http://127.0.0.1:5678`) presionando "Test step" en `RADAR_01_DISCOVERY`.
2. Añadir nuevos colectores públicos (p. ej., feeds RSS de HackerNews Who is Hiring, Upwork RSS público si está disponible, o agregadores especializados en bots y Python).
3. Programar el escaneo automático periódico (vía Windows Task Scheduler o n8n cron trigger) llamando a `python C:\Radar\scripts\run_radar_scan.py`.
