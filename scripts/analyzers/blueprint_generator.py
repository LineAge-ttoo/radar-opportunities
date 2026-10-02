class BlueprintGenerator:
    """
    Generates actionable commercialization blueprints for opportunities
    marked as 'CONSTRUIR_Y_VENDER' (Build Once, Sell Many Times).
    """

    @staticmethod
    def generate_blueprint(opp):
        title = opp.get('title', 'Automation Product')
        org = opp.get('organization', 'Target Market')
        skills = opp.get('skills', [])

        if any(s in skills for s in ['n8n', 'automation', 'bot', 'workflow']):
            prod_type = "Plantilla de Automatización n8n / Bot Integrado"
            deliverable = "Flujo exportable en JSON de n8n con documentación de variables y webhook de conexión."
            target_audience = "Agencias de marketing, e-commerce y startups que usan herramientas SaaS dispersas."
            pricing = "USD $99 - $199 (pago único) o $49/mes con soporte y hosting."
            distribution = "Gumroad, comunidades de n8n/Reddit y outreach directo por LinkedIn/Email a empresas similares."
        elif any(s in skills for s in ['ai', 'llm', 'agent']):
            prod_type = "Micro-Herramienta de IA / Agente de Extracción y Clasificación"
            deliverable = "Script Python / Docker container con API REST para procesar documentos/leads automáticamente."
            target_audience = "Empresas B2B con alto volumen de atención al cliente o entrada de datos manual."
            pricing = "USD $149 - $299 por setup inicial + $50/mes de mantenimiento."
            distribution = "Product Hunt, Twitter/X tech demo y prospección directa B2B."
        elif any(s in skills for s in ['scraping', 'crawler']):
            prod_type = "Dataset Especializado / API de Monitoreo de Competencia"
            deliverable = "Extracción periódica con entrega en Google Sheets / Notion / API JSON."
            target_audience = "Analistas de mercado, reclutadores o tiendas que monitorean precios."
            pricing = "USD $79/mes por fuente de datos actualizada."
            distribution = "RapidAPI, marketplaces de datos y outreach a negocios del nicho."
        elif any(s in skills for s in ['unity', 'roblox', 'blender', '3d']):
            prod_type = "Pack de Assets 3D Optimizados / Template de Sistema Interactivo"
            deliverable = "Archivos .blend, prefabs de Unity o modelos Roblox listos para producción con rigging y colisiones."
            target_audience = "Estudios indie de videojuegos, creadores de contenido 3D y desarrolladores de Roblox."
            pricing = "USD $29 - $89 en marketplaces de assets."
            distribution = "Unity Asset Store, Roblox Creator Store, ArtStation, CGTrader."
        else:
            prod_type = "Herramienta Web Ligera / Micro-SaaS"
            deliverable = "Aplicación web de una sola función que resuelve un dolor puntual."
            target_audience = "Profesionales independientes y pequeñas empresas."
            pricing = "USD $19 - $49/mes."
            distribution = "Directorios de software, comunidades y SEO orgánico."

        outreach_template = f"""Asunto: Automatización para {org} - Ahorro de horas manuales

Hola,
Noté que en {org} manejan procesos relacionados con {', '.join(skills[:2]) if skills else 'operaciones digitales'}.
Desarrollé una solución que automatiza exactamente este flujo ({prod_type}), reduciendo los tiempos de ejecución a segundos y eliminando errores manuales.

Si te interesa ver un demo en video de 2 minutos sin compromiso, ¿me confirmas si te parece bien que te lo envíe por aquí?

Saludos,
David
"""

        return {
            'product_type': prod_type,
            'deliverable': deliverable,
            'target_audience': target_audience,
            'suggested_pricing': pricing,
            'distribution_channels': distribution,
            'outreach_template': outreach_template.strip()
        }
