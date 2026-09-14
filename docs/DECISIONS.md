# RADAR: Registro Canónico de Decisiones Técnicas (ADR)

---

## ADR-001: Persistencia Híbrida Local (SQLite + JSONL + Export JSON)
- **Fecha:** 2026-09-13
- **Estado:** Aceptado e Implementado
- **Contexto:**
  RADAR requiere almacenar de manera confiable y continua las oportunidades descubiertas en cada escaneo, sin perder historial, permitiendo deduplicación veloz por ID/URL y facilitando consultas analíticas sin dependencias de servicios externos ni bases de datos pesadas.
- **Decisión:**
  Se implementó una arquitectura de persistencia tripartita:
  1. `data/opportunities/radar.db` (SQLite 3 con WAL y transacciones ACID): Registro maestro con índices sobre `decision`, `overall_score` y `source`, y soporte para `UPSERT` (actualización de última aparición sin duplicar).
  2. `data/opportunities/opportunities.jsonl`: Flujo de auditoría append-only para trazabilidad histórica.
  3. `data/opportunities/latest_scan.json`: Snapshot estructurado del último escaneo para consumo inmediato de frontends y dashboards.
- **Consecuencias:**
  Zero mantenimiento externo, 100% autónomo, portable y de alta velocidad.

---

## ADR-002: Separación Estricta entre Datos Observados y Datos Estimados
- **Fecha:** 2026-09-13
- **Estado:** Aceptado e Implementado
- **Contexto:**
  Muchos scrapers y agregadores inventan salarios, redondean valores ausentes o confunden suposiciones del algoritmo con datos fácticos de la oferta original.
- **Decisión:**
  El esquema canónico de RADAR divide explícitamente:
  - `observed_data`: Datos empíricamente comprobados en la fuente (salario textual, ubicación indicada, tipo de empleo, etiquetas originales, URL intacta). Si el salario no está publicado, su valor numérico es `NULL`.
  - `estimated_data`: Deducciones probabilísticas y analíticas del motor (rango de horas estimado, nivel de dificultad, potencial económico estimado, nivel de competencia, viabilidad de automatización).
- **Consecuencias:**
  Cero alucinaciones, transparencia total ante el operador humano y legitimidad en el análisis.

---

## ADR-003: Arquitectura Modular de Collectors Independientes
- **Fecha:** 2026-09-13
- **Estado:** Aceptado e Implementado
- **Contexto:**
  Depender exclusivamente de una fuente (como Remotive) crea un punto único de fallo y limita el espectro de oportunidades (falta de freelance directo, bounties de código abierto y problemas sin publicar).
- **Decisión:**
  Cada fuente es un módulo colector independiente (`scripts/collectors/`):
  - `remotive_collector.py`: API oficial de Remotive para empleos tecnológicos remotos.
  - `arbeitnow_collector.py`: API pública de Arbeitnow para desarrollo y roles globales.
  - `github_bounties_collector.py`: API pública de GitHub Issues para bounties de código abierto.
  - `collector_manager.py`: Orquestador tolerante a fallos. Si una fuente falla por timeout o red, el escaneo continúa sin bloquear el sistema.
- **Consecuencias:**
  Fácil adición de nuevas fuentes públicas y legales en el futuro.

---

## ADR-004: Coexistencia Sinérgica entre CLI y n8n
- **Fecha:** 2026-09-13
- **Estado:** Aceptado e Implementado
- **Contexto:**
  n8n 2.38.7 está instalado localmente en `C:\Radar\n8n` con interfaz visual en `http://127.0.0.1:5678`, pero los escaneos de alta densidad, procesamiento por lotes y pruebas automatizadas requieren una ejecución rápida por consola sin fricción de interfaz gráfica.
- **Decisión:**
  - El motor analítico, persistencia y colectores residen en Python (`scripts/`), con sincronización directa a n8n.
  - Los workflows canónicos (`RADAR_01_DISCOVERY` y `RADAR_02_DEMAND_DETECTION`) se mantienen como código en `n8n/workflows/` e integrados en la base SQLite interna de n8n para visualización y disparo manual en el editor.
  - El runner `scripts/run_radar_scan.py` permite ejecuciones programadas y manuales completas en menos de 10 segundos.
- **Consecuencias:**
  Máxima velocidad operativa, interfaz web interactiva siempre disponible y cero dependencia de bloqueos de interfaz gráfica.

---

## ADR-005: Registro de Deuda Técnica: Futura Transición a Docker en n8n
- **Fecha:** 2026-09-13
- **Estado:** Documentado como Deuda Técnica (No accionar todavía)
- **Contexto:**
  n8n v2.38.7 emite una advertencia oficial indicando que en futuras versiones mayores de n8n se requerirá Docker para ejecución en producción.
- **Decisión:**
  Se mantiene estrictamente la instalación local en Windows sobre Node.js 24 sin instalar Docker por ahora (cumpliendo los requerimientos del usuario). La transición a contenedor se abordará solo cuando una versión futura de n8n lo haga mandatorio y el usuario lo apruebe.
