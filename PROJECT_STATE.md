# ESTADO CANÓNICO DEL PROYECTO: RADAR v2
**Fecha de última actualización:** 2026-10-19  
**Root Canónico:** `C:\Radar`  
**Estado General:** 100% OPERATIVO EN NUBE (GITHUB PAGES / VERCEL), SAFARI iOS/macOS Y SERVIDOR LOCAL  

---

## 1. ENLACES DE ACCESO EN VIVO (24/7)

| Canal | URL / Ruta | Estado |
| :--- | :--- | :--- |
| **🌐 Web App en la Nube (Safari / Móvil / PC)** | [https://lineage-ttoo.github.io/radar-opportunities/](https://lineage-ttoo.github.io/radar-opportunities/) | **ACTIVO 24/7** |
| **📦 Repositorio Oficial en GitHub** | [https://github.com/LineAge-ttoo/radar-opportunities](https://github.com/LineAge-ttoo/radar-opportunities) | **ACTIVO** |
| **▲ Enlace de Importación 1-Clic en Vercel** | [https://vercel.com/new/clone?repository-url=https://github.com/LineAge-ttoo/radar-opportunities](https://vercel.com/new/clone?repository-url=https://github.com/LineAge-ttoo/radar-opportunities) | **CONFIGURADO (`vercel.json`)** |
| **💻 Servidor Local en PC** | [http://127.0.0.1:8080](http://127.0.0.1:8080) | **ACTIVO (200 OK)** |
| **📱 Servidor en Red Local (Wi-Fi)** | `http://192.168.100.230:8080` | **ACTIVO (200 OK)** |
| **📥 App Portátil Descargable (Offline HTML)** | `C:\Radar\exports\RADAR_Portable_Safari.html` | **GENERADO** |

---

## 2. CORRECCIONES CRÍTICAS Y MEJORAS EN V2 (2026-10-19)

1. **Corrección de Bug Crítico de Sintaxis JS en `app/index.html`:**
   - En la versión anterior existía un salto de línea literal dentro de un string JS en `openBp()`, lo que impedía que el navegador ejecutara `window.onload` y dejaba los contadores en `0`.
   - **Solución:** Código JavaScript reestructurado y validado con `node` (`JS_SYNTAX_OK`), mostrando de inmediato las **151 oportunidades accionables**.
2. **Motor de Frescura ("Ofertas Más Novedosas"):**
   - Normalización de fechas multi-formato (Unix timestamp en Arbeitnow, RFC-2822 en WeWorkRemotely, ISO-8601 en Remotive, RemoteOK, HackerNews y GitHub) a UTC ISO-8601.
   - Bono de frescura automático para ofertas publicadas hace `< 24h` (`🔥 Publicado Hoy`) y `< 72h` (`⚡ Hace 1-3d`), y descarte automático de ofertas antiguas (> 45 días).
   - Consultas de **HackerNews Algolia** actualizadas con `numericFilters=created_at_i` para traer únicamente ofertas y contratos de los últimos 30 días (pasando de 2 a 58 hallazgos frescos).
3. **Escáner en Vivo Directo desde el Navegador (Safari / iPhone / Cloud):**
   - El botón **"⚡ Buscar Ofertas Nuevas en Vivo"** ahora consulta directamente desde el navegador del usuario las APIs públicas con soporte CORS (Hacker News Algolia, GitHub Bounties, Remotive) además del backend local cuando está disponible, permitiendo descubrir ofertas recién publicadas desde Safari en un iPhone sin depender de que la PC esté encendida.
4. **Automatización en la Nube (GitHub Actions):**
   - Workflow `.github/workflows/radar-live.yml` configurado para ejecutar `python scripts/run_radar_scan.py` cada 6 horas en los servidores de GitHub y actualizar automáticamente la aplicación publicada.

---

## 3. MÉTRICAS DEL ESCANEO EN VIVO ACTUAL (2026-10-19)
- **Hallazgos Totales Analizados:** 338
- **Oportunidades Accionables (Sin Ruido):** 151
  - **🚀 PRIORIDAD:** 52 oportunidades de alto ajuste técnico y presupuesto.
  - **💡 CONSTRUIR Y VENDER:** 15 oportunidades ideales para empaquetar y vender múltiples veces.
  - **🔍 INVESTIGAR:** 55 oportunidades viables.
  - **👀 OBSERVAR:** 29 oportunidades.
