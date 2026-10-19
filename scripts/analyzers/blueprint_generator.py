class BlueprintGenerator:
    """
    Genera paquetes prácticos ("Construir una vez y vender a varios negocios en Colombia")
    sin necesidad de contratos legales ni ingeniería compleja.
    """

    @staticmethod
    def generate_blueprint(opp):
        skills_text = ' '.join(opp.get('skills', [])).lower()
        org = opp.get('organization', 'Negocio en Colombia')

        if 'planos' in skills_text or '3d' in skills_text:
            prod_type = "📐 Paquete Express de Planos 2D + Render 3D para Remodeladores y Carpinteros en Colombia"
            deliverable = "Plano acotado en PDF/DWG + 3 vistas Render 3D de cómo quedará la cocina, local o remodelación."
            target_audience = "Maestros de obra, remodeladores, carpinterías, fabricantes de cocinas integrales e inmobiliarias en Colombia (Instagram y Facebook)."
            pricing = "COP $220.000 a $650.000 por proyecto (Pago por Nequi / Bancolombia: 50% al iniciar, 50% al entregar)."
            distribution = "Escribir por WhatsApp o Instagram DM a 10 cuentas de remodelaciones/cocinas en Colombia cada día ofreciendo el servicio por proyecto."
        elif 'whatsapp' in skills_text or 'automatizaci' in skills_text or 'bot' in skills_text:
            prod_type = "🤖 Bot de Respuesta y Agendamiento en WhatsApp 24/7 (Plantilla n8n / WhatsApp)"
            deliverable = "Flujo ya armado que responde precios, envía catálogo PDF/fotos y agenda citas en Google Calendar/Sheets."
            target_audience = "Clínicas odontológicas, centros de estética, barberías, inmobiliarias y tiendas en Instagram Colombia."
            pricing = "COP $350.000 por dejarlo instalado + COP $80.000/mes opcional por mantenimiento."
            distribution = "Contactar por WhatsApp o Instagram DM a negocios locales que dicen 'Citas por WhatsApp' en su biografía."
        else:
            prod_type = "🌐 Catálogo Digital / Menú QR con Carrito Directo a WhatsApp"
            deliverable = "Página web rápida (alojada gratis en GitHub Pages / Vercel) donde el cliente elige productos y envía el pedido armado al WhatsApp del negocio."
            target_audience = "Restaurantes, cafés especiales, glampings, tiendas de ropa y emprendimientos en Instagram/Facebook Colombia."
            pricing = "COP $250.000 a $550.000 pago único (Nequi / Bancolombia)."
            distribution = "Enviar enlace de ejemplo por WhatsApp / DM a negocios en Colombia que aún no tienen página web o solo usan PDF pesado."

        outreach_template = f"""¡Hola {org}! 👋
Vi su perfil en redes y les armé una propuesta rápida de {prod_type} para que ahorren tiempo y cierren más ventas por WhatsApp.
No requiere contratos ni mensualidades costosas. ¿Te envío una muestra rápida por aquí para que la veas en tu celular?"""

        return {
            'product_type': prod_type,
            'deliverable': deliverable,
            'target_audience': target_audience,
            'suggested_pricing': pricing,
            'distribution_channels': distribution,
            'outreach_template': outreach_template
        }
