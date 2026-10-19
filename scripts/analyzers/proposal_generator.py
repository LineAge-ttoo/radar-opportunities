class TechnicalProposalGenerator:
    """
    Genera mensajes directos (WhatsApp / Instagram DM / Facebook / Workana)
    100% en español, prácticos, sin tecnicismos de ingeniería ni contratos legales.
    """

    @classmethod
    def generate_pitch(cls, opp):
        title = opp.get('title', 'Proyecto')
        org = opp.get('organization', 'Cliente').replace('(🇨🇴 Colombia)', '').strip()
        skills_text = ' '.join(opp.get('skills', [])).lower()
        obs = opp.get('observed_data', {})
        offer_type = obs.get('offer_type', '')
        wa_phone = obs.get('whatsapp_phone')
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        curr = opp.get('currency') or 'COP'

        # 1. Clientes directos en Instagram / Facebook Colombia
        if opp.get('opportunity_type') == 'cliente_directo_colombia':
            if offer_type == 'planos_3d' or 'planos' in skills_text or '3d' in skills_text:
                subject = f"Apoyo en Planos 2D/3D y Renders para {org}"
                body = f"""¡Hola equipo de {org}! 👋 ¿Cómo están?

Vi sus proyectos en redes y me gustó mucho su trabajo. Escribo porque elaboro **planos arquitectónicos 2D/3D, distribución de espacios, despieces de mobiliario y renders realistas** de entrega rápida para mostrarle al cliente cómo quedará su obra antes de iniciar.

✅ Trabajo por tarea/proyecto puntual (sin contratos complicados ni mensualidades).
✅ Entrego boceto / vista previa en 24-48 horas.
✅ Pago fácil en Colombia (Nequi / Bancolombia / transferencia).

¿Les gustaría que les envíe un par de muestras de planos y renders 3D por aquí para que me tengan a la mano en su próxima cotización?"""
                pricing = f"COP ${int(p_min or 250000):,} - ${int(p_max or 850000):,} por proyecto (50% inicio / 50% entrega)".replace(',', '.')
                turnaround = "24 a 48 horas por plano / render"

            elif offer_type == 'whatsapp_bot' or 'whatsapp' in skills_text:
                subject = f"Automatización de WhatsApp y Citas 24/7 para {org}"
                body = f"""¡Hola {org}! 👋 ¿Cómo van?

Los encontré en redes y noté que atienden a sus clientes por WhatsApp / mensajes directos. 

Implemento **asistentes automáticos de WhatsApp e Instagram** que:
1. Responden preguntas frecuentes, precios y ubicación al instante (24/7).
2. Filtran a los clientes realmente interesados y agendan citas/visitas solas.
3. Te evitan perder clientes cuando están ocupados o fuera de horario.

No requiere contratos largos: lo dejo funcionando en 48 horas con un pago único accesible (Nequi / Bancolombia). ¿Te envío un video corto de 1 minuto por WhatsApp mostrando cómo respondería para tu negocio?"""
                pricing = f"COP ${int(p_min or 300000):,} - ${int(p_max or 900000):,} pago único por montaje".replace(',', '.')
                turnaround = "48 horas listo y funcionando"

            else:
                subject = f"Catálogo Digital Interactivo con Pedidos a WhatsApp para {org}"
                body = f"""¡Hola {org}! 👋

Vi su página en redes y quería proponerles algo muy práctico para vender más rápido: les armo un **Catálogo Digital / Página Web Interactiva** donde sus clientes ven fotos, precios actualizados, eligen lo que quieren y el pedido te llega armado directo a tu WhatsApp listo para despachar o reservar.

✅ Sin comisiones por venta ni contratos complicados.
✅ Listo en 2 a 3 días.
✅ Pago en Colombia (Nequi / Bancolombia).

¿Te paso un enlace de demostración por aquí para que veas cómo se ve desde el celular?"""
                pricing = f"COP ${int(p_min or 250000):,} - ${int(p_max or 800000):,} pago único".replace(',', '.')
                turnaround = "2 a 3 días"

            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 2. Tareas en Workana / Freelancer.co
        if 'planos' in skills_text or '3d' in skills_text or 'autocad' in skills_text:
            hook = "Tengo experiencia práctica haciendo **planos 2D/3D, modelado (AutoCAD / Blender / STL / DWG) y renders listos para fabricación o presentación**."
            turnaround = "24 a 48 horas para el primer avance / vista previa"
        elif 'whatsapp' in skills_text or 'automatizaci' in skills_text or 'bot' in skills_text:
            hook = "Me dedico a armar **automatizaciones prácticas y bots de WhatsApp / n8n / IA** que quedan funcionando rápido, sin complicar la operación."
            turnaround = "24 a 48 horas funcionando y probado"
        elif 'web' in skills_text or 'catálogo' in skills_text or 'diseño' in skills_text:
            hook = "Desarrollo **páginas web rápidas, catálogos interactivos, vectorizaciones y piezas visuales limpias** listas para usar en móvil y PC."
            turnaround = "24 a 72 horas para entrega completa"
        else:
            hook = "Puedo encargarme de esta tarea de forma práctica, rápida y cuidando cada detalle de lo que necesitas."
            turnaround = "24 a 48 horas"

        if p_min and p_max:
            pricing = f"Presupuesto: {curr} {int(p_min):,} - {int(p_max):,} (Pago por entregable)"
        else:
            pricing = "Precio fijo cerrado por tarea terminada"

        subject = f"Propuesta directa y entrega rápida: {title}"
        body = f"""¡Hola! Revisé lo que necesitas para **"{title}"** y puedo empezar hoy mismo.

{hook}

**Cómo lo trabajamos fácil y rápido:**
1. Me pasas los detalles o archivos base hoy.
2. En **menos de 24-48 horas** te envío el primer avance real para que veas cómo va quedando y ajustemos lo que quieras.
3. Te entrego los archivos finales editables y listos para usar.

Escríbeme por aquí para confirmar un par de detalles y arrancar de una vez. ¡Un saludo!"""

        return {
            'language': 'es',
            'subject': subject,
            'body': body,
            'pricing_recommendation': pricing,
            'turnaround': turnaround,
            'whatsapp_phone': None
        }
