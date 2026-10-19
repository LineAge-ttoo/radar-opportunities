class TechnicalProposalGenerator:
    """
    Genera mensajes directos (WhatsApp / Instagram DM / Facebook / Workana / Alcaldía / Estudiantes)
    100% en español, prácticos, destacando el perfil de Maestro en Construcción en Guadua Certificado,
    Diseño de Cabañas, Blender 3D, Planos AutoCAD y Automatizaciones en San Agustín Huila y Colombia.
    """

    @classmethod
    def generate_pitch(cls, opp):
        title = opp.get('title', 'Proyecto')
        org = opp.get('organization', 'Cliente').replace('(🇨🇴 Colombia)', '').strip()
        skills_text = f"{title} {opp.get('description', '')} {' '.join(opp.get('skills', []))}".lower()
        obs = opp.get('observed_data', {})
        offer_type = obs.get('offer_type', '')
        cat_hint = obs.get('category_hint', '')
        wa_phone = obs.get('whatsapp_phone')
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        curr = opp.get('currency') or 'COP'

        # 1. Cabañas en Guadua / Maestro Certificado en Guadua / San Agustín Huila
        if cat_hint == 'guadua_cabanas' or 'guadua' in skills_text or 'cabaña' in skills_text or 'bamb' in skills_text:
            subject = f"Diseño 3D y Construcción en Guadua Certificada — {org}"
            body = f"""¡Hola {org}! 👋 Un gusto saludarte desde San Agustín, Huila.

Vi su proyecto relacionado con **{title}** y me pongo a su disposición: soy **Maestro en Construcción en Guadua Certificado** y además realizo el **modelado arquitectónico en Blender 3D y planos técnicos 2D/3D**.

✅ Diseño de cabañas, glampings, malokas, kioscos y estructuras bioclimáticas en guadua inmunizada.
✅ Entrega de renders realistas en Blender 3D + cortes y despiece para saber exactamente cuánta guadua y material se necesita antes de construir.
✅ Disponibilidad inmediata en **San Agustín, Pitalito, Isnos y todo el Huila** (o envío de planos y modelos 3D a cualquier parte de Colombia).

¿Agendamos una llamada o visita rápida por WhatsApp al **322 273 9034** para mostrarles diseños de cabañas y presupuestos?"""
            pricing = f"COP ${int(p_min or 650000):,} — ${int(p_max or 3800000):,} (Diseño 3D / Obra a convenir)".replace(',', '.')
            turnaround = "Boceto 3D en 24-48 horas · Visita en San Agustín / Huila"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 2. Alcaldía de San Agustín Huila / Alcaldías Cercanas / SECOP II
        if cat_hint == 'alcaldia_huila' or 'alcaldía' in skills_text or 'alcaldia' in skills_text or 'secop' in skills_text:
            subject = f"Propuesta Técnica Local (San Agustín / Huila): {title}"
            body = f"""Cordial saludo, equipo de **{org}**:

Desde **San Agustín, Huila**, presento manifestación de interés y disponibilidad técnica inmediata para el proceso/proyecto **"{title}"**.

Cuento con certificación como **Maestro en Construcción en Guadua**, experiencia en diseño y adecuación de infraestructura turística/cultural, elaboración de planos 2D/3D, modelado en Blender y apoyo técnico operativo en el Sur del Huila.

📞 Contacto directo en San Agustín Huila: **+57 322 273 9034**
Quedo atento a los requisitos de mínima cuantía o apoyo técnico para radicar propuesta formal hoy mismo."""
            pricing = f"COP ${int(p_min or 1500000):,} — ${int(p_max or 15000000):,}".replace(',', '.')
            turnaround = "Radicación inmediata en San Agustín / Huila"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 3. Estudiantes y Universitarios (Tareas, Entregas de Arquitectura/Ingeniería, Blender 3D, AutoCAD)
        if cat_hint == 'estudiantes_tareas' or 'estudiante' in skills_text or 'universitari' in skills_text or 'sena' in skills_text or 'unad' in skills_text:
            subject = f"Entrega Rápida de Planos, Blender 3D y Tareas Universitarias"
            body = f"""¡Hola! 👋 Vi que necesitas apoyo con **"{title}"**.

Te ayudo a sacar tu entrega universitaria o proyecto práctico a tiempo y con excelente presentación:
✅ **Modelado y Renders en Blender 3D** (arquitectura, cabañas en guadua, objetos, animación).
✅ **Planos 2D/3D en AutoCAD (.DWG y PDF listos para plotear)**.
✅ **Detalles constructivos en Guadua / Bambú**, maquetas digitales y tareas prácticas (SENA / UNAD / Universidad).

Te muestro avances por WhatsApp en menos de 24 horas y manejamos precios accesibles para estudiantes por Nequi o Bancolombia.
📲 Escríbeme directo a mi WhatsApp: **+57 322 273 9034** y lo revisamos ya mismo."""
            pricing = f"COP ${int(p_min or 90000):,} — ${int(p_max or 380000):,} (Tarifa Estudiante · Nequi)".replace(',', '.')
            turnaround = "12 a 24 horas (Entregas urgentes)"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 4. Clientes directos en Instagram / Facebook Colombia
        if opp.get('opportunity_type') == 'cliente_directo_colombia':
            if offer_type == 'planos_3d' or 'planos' in skills_text or '3d' in skills_text:
                subject = f"Planos 2D/3D, Blender Renders y Guadua para {org}"
                body = f"""¡Hola equipo de {org}! 👋

Vi sus proyectos en redes y me gustó mucho su trabajo. Elaboro **planos arquitectónicos 2D/3D, renders en Blender, diseños de cabañas en guadua certificada y despieces de mobiliario** en 24-48 horas por proyecto (sin contratos ni mensualidades, pago por Nequi / Bancolombia).

¿Les envío un par de muestras de planos y renders 3D a su WhatsApp? (Mi línea directa: +57 322 273 9034)."""
                pricing = f"COP ${int(p_min or 250000):,} — ${int(p_max or 850000):,}".replace(',', '.')
                turnaround = "24 a 48 horas"
            elif offer_type == 'whatsapp_bot' or 'whatsapp' in skills_text:
                subject = f"Bot de WhatsApp y Citas 24/7 para {org}"
                body = f"""¡Hola {org}! 👋

Noté que atienden clientes por WhatsApp e Instagram. Implemento **asistentes automáticos 24/7** que responden precios, ubicación y agendan citas solos para no perder clientes fuera de horario.

Lo entrego funcionando en 48 horas con pago único en Colombia (Nequi / Bancolombia). ¿Te envío una demostración rápida? (WhatsApp: +57 322 273 9034)."""
                pricing = f"COP ${int(p_min or 300000):,} — ${int(p_max or 850000):,}".replace(',', '.')
                turnaround = "48 horas"
            else:
                subject = f"Catálogo Digital con Pedidos a WhatsApp para {org}"
                body = f"""¡Hola {org}! 👋

Les armo un **Catálogo Digital / Web Interactiva** donde sus clientes eligen productos o reservan cabañas desde el celular y el pedido llega listo a su WhatsApp.

Listo en 2 días, sin mensualidades ni comisiones (pago por Nequi / Bancolombia). ¿Te muestro un ejemplo en vivo? (WhatsApp: +57 322 273 9034)."""
                pricing = f"COP ${int(p_min or 250000):,} — ${int(p_max or 750000):,}".replace(',', '.')
                turnaround = "2 a 3 días"

            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 5. Proyectos en Workana / Freelancer.co
        if 'planos' in skills_text or '3d' in skills_text or 'blender' in skills_text or 'autocad' in skills_text:
            hook = "Soy especialista en **modelado 3D en Blender, planos 2D/3D en AutoCAD y diseño estructural de cabañas/espacios (Maestro Certificado en Guadua)**."
            turnaround = "24 horas para el primer avance 3D / plano"
        elif 'whatsapp' in skills_text or 'automatizaci' in skills_text or 'bot' in skills_text:
            hook = "Configuro **bots de WhatsApp y automatizaciones prácticas (n8n / IA)** listas en 24-48 horas."
            turnaround = "24 a 48 horas"
        else:
            hook = "Me encargo de este proyecto de forma rápida, práctica y entregando archivos editables listos."
            turnaround = "24 a 48 horas"

        pricing = f"{curr} {int(p_min):,} — {int(p_max):,}" if (p_min and p_max) else "Precio cerrado por entregable"
        subject = f"Entrega en 24-48h: {title}"
        body = f"""¡Hola! Revisé tu encargo **"{title}"** y puedo comenzar hoy mismo.

{hook}

1. En **menos de 24 horas** te envío el primer avance real para validar cada detalle.
2. Entrega rápida sin trámites complicados (Contacto directo en Colombia: +57 322 273 9034).

¿Me compartes los detalles por aquí para arrancar de inmediato?"""

        return {
            'language': 'es',
            'subject': subject,
            'body': body,
            'pricing_recommendation': pricing,
            'turnaround': turnaround,
            'whatsapp_phone': None
        }
