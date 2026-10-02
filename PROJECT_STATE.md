# ESTADO DEL PROYECTO: RADAR
**Fecha de última actualización:** 2026-10-02  
**Root Canónico:** `C:\Radar`  
**Estado General:** TOTALMENTE OPERATIVO / MOTOR DE GENERACIÓN DE INGRESOS ACTIVO  

---

## 1. OBJETIVO DEL PROYECTO
RADAR es un motor personal de inteligencia y monetización para descubrir, analizar, estructurar propuestas comerciales y cerrar oportunidades de ingresos en:
- **Automatización & n8n**: Flujos de trabajo, webhooks, bots, integraciones multi-SaaS y eliminación de tareas manuales.
- **Python & Scraping Legal**: Extracción estructurada, APIs personalizadas y scripts de datos.
- **Inteligencia Artificial**: Agentes, llamadas a herramientas (function calling), flujos con LLMs y extracción estructurada.
- **Desarrollo Web & Backend**: Full-stack, React, TypeScript, Node.js y APIs REST.
- **3D & Videojuegos**: Unity, Roblox, Blender y pipelines de activos 3D.
- **Construir y Vender**: Blueprints de productos digitales, plantillas y micro-servicios empaquetados para vender múltiples veces.

---

## 2. ARQUITECTURA TÉCNICA IMPLEMENTADA

```
C:\Radar
│   .gitignore                        -> Exclusiones seguras de git
│   PROJECT_STATE.md                  -> Estado canónico del proyecto
│   README.md                         -> Resumen general
│   START_RADAR.bat                   -> Lanzador turnkey (Inicia App 8080 + n8n 5678)
│   START_RADAR.ps1                   -> Script PowerShell de orquestación dual
│
├── app                               -> APLICACIÓN WEB INTERACTIVA (Local & Móvil)
│   ├── index.html                    -> Dashboard SPA responsivo con pitches y CRM
│   └── server.py                     -> Servidor HTTP API en puerto 8080 (0.0.0.0)
│
├── config
│   ├── radar.config.json             -> Ajustes globales y umbrales
│   ├── scoring
│   │   └── scoring_rules.json        -> Reglas y ponderaciones de habilidades
│   └── sources
│       └── sources.json              -> Metadatos de fuentes
│
├── data
│   ├── incoming                      -> Respuestas crudas de APIs para trazabilidad
│   └── opportunities
│       ├── latest_scan.json          -> Snapshot JSON del último escaneo
│       ├── opportunities.jsonl       -> Stream append-only histórico
│       └── radar.db                  -> SQLite maestro con CRM y propuestas
│
├── docs
│   ├── DECISIONS.md                  -> ADRs del sistema
│   └── RADAR_02_DEMAND_DETECTION_SPEC.md -> Especificación de demanda oculta
│
├── exports
│   ├── RADAR_SCAN_LATEST.html        -> Reporte exportable estático
│   ├── RADAR_SCAN_LATEST.md          -> Reporte Markdown
│   └── RADAR_SUMMARY.json            -> Resumen métrico
│
├── n8n
│   ├── instance/.n8n                 -> Datos persistentes de n8n
│   └── workflows
│       ├── RADAR_01_DISCOVERY.json   -> Workflow v1 en n8n
│       └── RADAR_02_DEMAND_DETECTION.json -> Workflow v1 de demanda en n8n
│
└── scripts
    ├── analyzers
    │   ├── blueprint_generator.py    -> Generador de planes "Construir y Vender"
    │   ├── normalizer.py             -> Normalizador multi-fuente (6 canales)
    │   ├── proposal_generator.py     -> Generador de propuestas técnicas (Sniper Pitch)
    │   └── scoring_engine.py         -> Motor de puntuación (Fit, Dinero, Reusabilidad)
    ├── collectors
    │   ├── arbeitnow_collector.py    -> Colector Arbeitnow API
    │   ├── collector_manager.py      -> Orquestador tolerante a fallos
    │   ├── github_bounties_collector.py -> Colector GitHub Bounties
    │   ├── hackernews_collector.py   -> Colector Hacker News Algolia API
    │   ├── remoteok_collector.py     -> Colector RemoteOK API (Salarios explícitos)
    │   ├── remotive_collector.py     -> Colector Remotive API
    │   └── weworkremotely_collector.py -> Colector WeWorkRemotely RSS
    ├── run_radar_scan.py             -> Runner de escaneo integral
    └── utilities
        ├── backfill_proposals.py     -> Utilidad de backfill
        ├── db.py                     -> Capa de persistencia SQLite + CRM
        └── presenter.py              -> Exportador HTML y Markdown
```

---

## 3. CANALES DE GENERACIÓN DE INGRESOS ACTIVOS (6 FUENTES)
1. **RemoteOK**: Empleos remotos de alta compensación con salarios comprobados en USD ($70K - $250K).
2. **WeWorkRemotely**: Contratos y puestos de programación e infraestructura remota.
3. **Remotive**: Empleos remotos internacionales y posiciones de software/automatización.
4. **Arbeitnow**: Feed masivo de posiciones técnicas y de automatización.
5. **Hacker News (Algolia API)**: Comentarios directos de fundadores y CTOs contratando freelancers y consultores sin intermediarios.
6. **GitHub Bounties**: Tareas y recompensas de código abierto con pagos por issue.

---

## 4. MOTOR DE CIERRE: PROPUESTAS TÉCNICAS (SNIPER PITCH)
Para cada oportunidad en estado `PRIORIDAD`, `INVESTIGAR` o `CONSTRUIR_Y_VENDER`, RADAR genera automáticamente:
- **Asunto de alto impacto**: Específico y profesional.
- **Apertura de entendimiento técnico**: Mapeo directo a los dolores del cliente.
- **Arquitectura de solución**: Propuesta de cómo se construirá (n8n, Python, webhooks, reintentos, validación de datos).
- **Tiempo de entrega estimado**: 48 a 72 horas para MVP o primer hito.
- **Llamado a la acción de baja fricción**: Invitación a llamada rápida o demo en Loom.
- **Botón de copia rápida (1-click copy)** en el dashboard.

---

## 5. PIPELINE "CONSTRUIR Y VENDER" (PRODUCTIZACIÓN)
Para oportunidades donde una necesidad se repite y puede convertirse en producto:
- **Concepto de Producto**: Plantilla n8n, micro-herramienta Python, bot o dataset.
- **Entregable Concreto**: JSON exportable, script Dockerizado o repositorio con documentación.
- **Público Objetivo**: Perfil exacto de empresas que sufren el mismo cuello de botella.
- **Precio Sugerido**: $49 a $299 USD (pago único o suscripción).
- **Guión de Prospección en Frío**: Mensaje listo para enviar a 10-20 negocios similares.

---

## 6. SISTEMA CRM DE SEGUIMIENTO LOCAL
Estados gestionables desde el Dashboard:
- `NUEVA`: Hallazgo reciente pendiente de revisión.
- `REVISADA`: Oportunidad leída y evaluada.
- `PROPUESTA_ENVIADA`: Pitch enviado al cliente/oferente.
- `EN_NEGOCIACION`: Conversación o prueba técnica activa.
- `GANADA`: ¡Contrato cerrado / Ingreso generado!
- `DESCARTADA`: Archivada sin interés.

---

## 7. ACCESO Y PUNTOS DE ENTRADA
- **Dashboard Web Principal (PC):** `http://127.0.0.1:8080`
- **Dashboard Web Móvil (Mismo Wi-Fi):** `http://192.168.0.106:8080` (Ajustado dinámicamente)
- **Editor Visual n8n:** `http://127.0.0.1:5678`
- **Lanzador de un solo clic:** `C:\Radar\START_RADAR.bat`
