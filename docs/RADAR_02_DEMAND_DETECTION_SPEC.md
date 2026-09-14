# RADAR_02_DEMAND_DETECTION: Motor de Detección de Demanda Oculta
## Especificación Técnica y Arquitectura v1

### 1. Propósito
A diferencia de **RADAR_01_DISCOVERY** (que detecta ofertas explícitas de trabajo, contratos y bounties publicados), **RADAR_02_DEMAND_DETECTION** está diseñado para identificar **demanda latente y problemas repetitivos no resueltos** en el mercado.

Su objetivo es convertir dolores operativos y cuellos de botella frecuentes en:
- Plantillas de automatización (n8n, Make, Python)
- Micro-SaaS o herramientas web especializadas
- Bots (Telegram, Discord, Slack, WhatsApp)
- Conectores e integraciones de API personalizadas
- Scripts de scraping y extracción estructurada
- Activos y herramientas 3D / pipelines (Blender, Unity, Roblox)

---

### 2. Principio Rector: Evidencia vs. Idea

Para evitar el autoengaño o la creación de productos sin mercado, RADAR_02 impone una estricta separación ontológica:

```
+-------------------------------------------------------------------------+
|                         EVIDENCIA DE DEMANDA                            |
| (Hecho empírico observable: post público, queja, pregunta, cuello de   |
| botella documentado, presupuesto mencionado, frecuencia de quejas)      |
+-------------------------------------------------------------------------+
                                    |
                                    v [Procesamiento de RADAR]
+-------------------------------------------------------------------------+
|                        IDEA GENERADA POR RADAR                          |
| (Propuesta de software construible: qué construir, cómo empaquetarlo,   |
| modelo de monetización, stack técnico, esfuerzo estimado, precio)       |
+-------------------------------------------------------------------------+
```

1. **EVIDENCIA DE DEMANDA (Observado)**:
   - `evidence_source`: URL original, plataforma, comunidad o foro.
   - `author_or_entity`: Usuario, perfil o tipo de negocio afectado.
   - `pain_statement`: Texto textual que expresa la molestia o ineficiencia.
   - `frustration_signals`: Indicadores de fricción ("pierdo 3 horas diarias", "pago $500 por una herramienta que no funciona", "necesito conectar X con Y").
   - `urgency_level`: Baja, Media, Crítica.

2. **IDEA GENERADA POR RADAR (Estimado / Sintetizado)**:
   - `proposed_solution_type`: Plantilla n8n, Script Python, Bot, Micro-SaaS, Pipeline 3D.
   - `deliverable_description`: Qué artefacto técnico concreto se entrega.
   - `build_complexity`: Horas hombre estimadas de desarrollo (MVP en <24h).
   - `target_audience`: Quién más sufre exactamente el mismo dolor.
   - `pricing_model`: Pago único (Gumroad / Marketplace), Licencia mensual, Setup + Retainer.
   - `scalability_rating`: 0-100 (potencial de vender 10x, 50x o 100x sin rehacer el trabajo).

---

### 3. Fuentes Públicas Planificadas
- **GitHub Discussions & Feature Requests**: Solicitudes repetidas de integraciones no atendidas.
- **Foros de Comunidades No-Code / Automatización**: Reddit (r/n8n, r/automation, r/nocode, r/smallbusiness), foros públicos de Discourse.
- **Mercados de Plantillas y Plugins**: Reseñas de 1-3 estrellas en plugins populares donde los usuarios expresan qué función crítica falta.
- **StackOverflow & Q&A Públicos**: Preguntas con alta visualización de tipo "¿Cómo automatizo la exportación de X hacia Y?".

---

### 4. Estructura del Workflow n8n (RADAR_02_DEMAND_DETECTION)
- **Trigger**: Programado semanalmente o ejecución manual bajo demanda.
- **Recolección de Señales**: HTTP Request a feeds RSS / APIs públicas de foros de discusión.
- **Filtro de Ruido**: Eliminación de preguntas teóricas o tareas académicas.
- **Clasificador de Dolor**:
  - Detección de patrones de queja o ineficiencia operativa.
  - Extracción de entidades (herramientas involucradas: Airtable, Shopify, WooCommerce, Notion, Google Sheets, HubSpot, etc.).
- **Generador de Hipótesis de Producto**:
  - Creación del registro estructurado de la oportunidad `CONSTRUIR_Y_VENDER`.
- **Persistencia**: Inserción en `radar.db` con flag `opportunity_type = 'demand_signal'`.

---

### 5. Estado Actual
- **Fase**: Especificación y prototipo de workflow listos.
- **Integración**: Los resultados de demand detection se integran al mismo modelo de persistencia `radar.db` y se presentan bajo la categoría `CONSTRUIR_Y_VENDER`.
