import re

class TechnicalProposalGenerator:
    """
    Generates high-conversion, value-first technical proposals tailored
    to the specific skills, problem, and requirements of each opportunity.
    """

    @staticmethod
    def is_english(text):
        common_en = ['the', 'and', 'with', 'for', 'you', 'are', 'looking', 'developer', 'experience']
        common_es = ['el', 'la', 'para', 'con', 'experiencia', 'desarrollador', 'buscamos', 'equipo']
        
        lower = text.lower()
        en_count = sum(1 for w in common_en if re.search(r'\b' + w + r'\b', lower))
        es_count = sum(1 for w in common_es if re.search(r'\b' + w + r'\b', lower))
        return en_count >= es_count

    @classmethod
    def generate_pitch(cls, opp):
        title = opp.get('title', 'Project')
        org = opp.get('organization', 'Client')
        skills = opp.get('skills', [])
        skills_str = ', '.join(skills[:3]) if skills else 'Automation & Software Development'
        desc = opp.get('description', '')
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        curr = opp.get('currency') or 'USD'

        is_en = cls.is_english(f"{title} {desc}")

        # Determine technical architecture hook
        if any(s in skills for s in ['n8n', 'automation', 'workflow', 'bot']):
            arch_hook_en = "I can architect this using an automated workflow with webhook triggers, automated validation, and retry logic to eliminate manual overhead completely."
            arch_hook_es = "Puedo estructurar esto mediante un flujo automatizado con disparadores webhook, validación de datos y lógica de reintento para eliminar la fricción manual por completo."
        elif any(s in skills for s in ['ai', 'llm', 'agent']):
            arch_hook_en = "I can implement this with structured JSON outputs, robust function calling, and prompt grounding to ensure zero hallucination and production reliability."
            arch_hook_es = "Puedo implementar esto con salidas estructuradas en JSON, llamadas a funciones y validación estricta para garantizar fiabilidad en producción."
        elif any(s in skills for s in ['scraping', 'crawler']):
            arch_hook_en = "I can build a resilient extraction pipeline with rate-limit evasion, automated proxy rotation, and structured database output."
            arch_hook_es = "Puedo construir un pipeline de extracción resistente con gestión de límites de tasa y volcado estructurado directo a base de datos."
        elif any(s in skills for s in ['unity', 'roblox', 'blender', '3d']):
            arch_hook_en = "I can deliver optimized assets and clean scripting tailored to performance budgets and smooth gameplay interaction."
            arch_hook_es = "Puedo entregar activos optimizados y código limpio ajustado a los límites de rendimiento para una experiencia fluida."
        else:
            arch_hook_en = "I can deliver a clean, modular, and well-tested implementation focusing on maintainability and speed to delivery."
            arch_hook_es = "Puedo entregar una implementación limpia, modular y bien probada enfocada en mantenibilidad y rapidez de entrega."

        # Pricing proposal
        if p_max:
            pricing_en = f"Target Budget: {curr} {int(p_max):,} (Milestone-based delivery)"
            pricing_es = f"Presupuesto objetivo: {curr} {int(p_max):,} (Entrega por hitos)"
        elif p_min:
            pricing_en = f"Target Rate: {curr} {int(p_min):,} per milestone"
            pricing_es = f"Tarifa objetivo: {curr} {int(p_min):,} por hito"
        else:
            pricing_en = "Flat-rate per milestone or flexible hourly rate depending on scope"
            pricing_es = "Precio cerrado por hito o tarifa horaria flexible según alcance"

        turnaround_en = "48 to 72 hours for initial working prototype / milestone 1"
        turnaround_es = "48 a 72 horas para prototipo inicial funcional / hito 1"

        if is_en:
            subject = f"Technical Proposal: {title} | Solution & Architecture"
            body = f"""Hi {org} Team,

I came across your opening for "{title}" and reviewed your technical requirements.

### Why this is a great fit:
I specialize in {skills_str}. {arch_hook_en}

### Proposed Implementation Plan:
1. **Scope & Architecture (Day 1):** Define core inputs/outputs and map integrations/data models.
2. **Core Implementation (Days 2-3):** Build the functional system with full error-handling and automated tests.
3. **Deployment & Handoff (Day 4):** Verify edge cases, provide concise documentation, and deploy.

### Estimated Turnaround:
{turnaround_en}.

### Next Step:
If you have 5 minutes, let me know when works for a brief chat or reply here, and I'd be glad to share a quick architecture diagram tailored to your needs.

Best regards,
David
Software & Automation Specialist
"""
        else:
            subject = f"Propuesta Técnica: {title} | Arquitectura y Entrega Rápida"
            body = f"""Hola equipo de {org},

Revisé con detalle los requerimientos para "{title}".

### Ajuste Técnico y Solución:
Me especializo en {skills_str}. {arch_hook_es}

### Plan de Trabajo Propuesto:
1. **Definición y Arquitectura (Día 1):** Mapeo de entradas, salidas y estructura de datos.
2. **Desarrollo del Core (Días 2-3):** Implementación de la solución con manejo robusto de errores y pruebas.
3. **Entrega y Documentación (Día 4):** Puesta en marcha, validación de casos borde y transferencia.

### Tiempo Estimado de Entrega:
{turnaround_es}.

### Siguiente Paso:
¿Podemos coordinar una breve conversación de 5 minutos o responder por aquí para compartirte una demo o diagrama de la solución?

Saludos cordiales,
David
Especialista en Software y Automatización
"""

        return {
            'language': 'en' if is_en else 'es',
            'subject': subject,
            'body': body.strip(),
            'pricing_recommendation': pricing_en if is_en else pricing_es,
            'turnaround': turnaround_en if is_en else turnaround_es
        }
