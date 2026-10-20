class TechnicalProposalGenerator:
    """
    Genera mensajes directos (WhatsApp / Instagram DM / Facebook / Grupos / Alcaldía / Estudiantes)
    100% en español, prácticos, destacando el perfil completo del usuario en San Agustín Huila y Colombia:
    - Maestro en Construcción en Guadua Certificado & Bioconstrucción innovadora
    - Cabañas con estilo de muro tendinoso, incrustaciones de botellas y muros en vidrio
    - Todo tipo de estructuras en metal y soldadura (cerchas, cubiertas, pérgolas mixtas, portones)
    - Remodelación de estructuras tanto en guadua como en metal
    - Trabajos varios de segundo tiempo, manualidades artísticas y mobiliario (guadua, vidrio y metal)
    - Modelado en Blender 3D, Planos 2D/3D y Automatizaciones
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

        # 1. Cabañas, Bioconstrucción, Muro Tendinoso, Incrustaciones de Botellas, Vidrio, Guadua y Metal
        if cat_hint in ('guadua_cabanas', 'bioconstruccion_guadua', 'metal_soldadura') or any(
            k in skills_text for k in ['guadua', 'cabaña', 'bamb', 'bioconstrucci', 'tendinoso', 'botella', 'soldadura', 'estructuras en metal']
        ):
            subject = f"Bioconstrucción en Guadua, Muro Tendinoso, Vidrio y Estructuras en Metal — {org}"
            body = f"""¡Hola {org}! 👋 Un gusto saludarte desde San Agustín, Huila.

Vi su proyecto relacionado con **{title}** y me pongo a su entera disposición. Soy **Maestro Certificado en Guadua, Bioconstrucción y Estructuras Metálicas/Soldadura**:

✅ **Cabañas y Bioconstrucción Innovadora**: Estilo de **muro tendinoso**, **incrustaciones artísticas de botellas**, **muros en vidrio** y acabados finos en **guadua inmunizada**.
✅ **Estructuras en Metal y Soldadura**: Todo tipo de cubiertas, cerchas, plataformas para glamping, pérgolas mixtas (metal + guadua), barandas y portones.
✅ **Remodelaciones en Guadua y Metal**: Mantenimiento estructural, reemplazo de piezas, ampliación de cabañas y **diseño previo en Blender 3D / Planos** para ver cómo quedará antes de construir.

Estoy aquí mismo en la zona (**San Agustín / Sur del Huila**). ¿Agendamos una visita o llamada rápida por WhatsApp al **+57 322 273 9034** para mostrarles fotos de trabajos y cotizar sin compromiso?"""
            pricing = f"COP ${int(p_min or 650000):,} — ${int(p_max or 4500000):,} (Obra, Remodelación o Diseño 3D a convenir)".replace(',', '.')
            turnaround = "Visita inmediata en San Agustín / Huila · Boceto 3D en 24-48h"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 2. Trabajos Informales, Segundo Tiempo y Manualidades (Lámparas en Guadua, Vidrio, Soldadura rápida)
        if cat_hint == 'informales_manualidades' or any(
            k in skills_text for k in ['manualidad', '2do tiempo', 'segundo tiempo', 'informal', 'lámpara', 'lampara', 'artesanía', 'artesania']
        ):
            subject = f"Trabajos de 2do Tiempo, Manualidades en Guadua/Vidrio y Soldadura — {org}"
            body = f"""¡Hola {org}! 👋 Te escribo desde San Agustín, Huila.

Estoy disponible para **trabajos por encargo, de segundo tiempo o fin de semana** sin trámites complicados:
🛠️ **Manualidades y Decoración Artística**: Lámparas en guadua, vitrales e incrustaciones con botellas de vidrio, letreros rústicos y muebles pequeños en metal soldado + guadua.
🔩 **Soldadura y Reparaciones Locativas**: Arreglo de rejas, portones, techos metálicos, mantenimiento e inmunización de cabañas en guadua y pintura.

Manejamos trato directo y precios justos por día o por trabajo entregado.
📲 Mi WhatsApp directo en San Agustín es **+57 322 273 9034**. ¿Qué trabajo o diseño necesitan sacar adelante esta semana?"""
            pricing = f"COP ${int(p_min or 80000):,} — ${int(p_max or 650000):,} (Pago por día o por encargo)".replace(',', '.')
            turnaround = "Disponibilidad inmediata / Segundo tiempo y fines de semana"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 3. Grupos de Redes y WhatsApp (Publicación lista para pegar o enviar al contratante del grupo)
        if cat_hint == 'grupos_redes' or 'grupo' in skills_text:
            subject = f"Oferta de Servicios en San Agustín y Huila: Guadua, Bioconstrucción, Metal y Soldadura"
            body = f"""👋 ¡Hola! Estoy disponible en **San Agustín, Isnos, Pitalito y alrededores** para proyectos y trabajos de:

🎋 **Bioconstrucción y Guadua Certificada**: Cabañas con **muro tendinoso**, **incrustaciones de botellas**, **muros en vidrio**, kioscos, miradores y pérgolas.
🔩 **Estructuras en Metal y Soldadura**: Techos, cerchas, plataformas para glamping, portones y estructuras mixtas (guadua + metal).
🛠️ **Remodelaciones y Trabajos de 2do Tiempo / Manualidades**: Mantenimiento de guadua y metal, lámparas artesanales, muebles y diseño previo en **Blender 3D / Planos**.

📲 **Contacto directo / WhatsApp: +57 322 273 9034** (Trato directo y presupuesto sin compromiso)."""
            pricing = f"COP ${int(p_min or 150000):,} — ${int(p_max or 4500000):,}".replace(',', '.')
            turnaround = "Atención inmediata en San Agustín y Sur del Huila"
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': turnaround,
                'whatsapp_phone': wa_phone
            }

        # 4. Alcaldía de San Agustín Huila / Alcaldías Cercanas / SECOP II
        if cat_hint == 'alcaldia_huila' or 'alcaldía' in skills_text or 'alcaldia' in skills_text or 'secop' in skills_text:
            subject = f"Propuesta Técnica Local (San Agustín / Huila): {title}"
            body = f"""Cordial saludo, equipo de **{org}**:

Desde **San Agustín, Huila**, presento manifestación de interés y disponibilidad técnica inmediata para el proceso/proyecto **"{title}"**.

Cuento con certificación como **Maestro en Construcción en Guadua**, experiencia en **bioconstrucción (muro tendinoso, vidrio y acabados ecológicos)**, **estructuras metálicas y soldadura**, remodelación de infraestructura turística/cultural, elaboración de planos 2D/3D y modelado en Blender.

📞 Contacto directo en San Agustín Huila: **+57 322 273 9034**
Quedo atento a los requisitos de mínima cuantía o apoyo técnico para radicar propuesta hoy mismo."""
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

        # 5. Estudiantes y Universitarios (Tareas, Entregas de Arquitectura/Ingeniería, Blender 3D, AutoCAD, Maquetas)
        if cat_hint == 'estudiantes_tareas' or 'estudiante' in skills_text or 'universitari' in skills_text or 'sena' in skills_text or 'unad' in skills_text:
            subject = f"Entrega Rápida de Planos, Blender 3D, Maquetas y Tareas Universitarias"
            body = f"""¡Hola! 👋 Vi que necesitas apoyo con **"{title}"**.

Te ayudo a sacar tu entrega universitaria o proyecto práctico a tiempo:
✅ **Modelado y Renders en Blender 3D** (arquitectura, cabañas en guadua, bioconstrucción, estructuras metálicas, animación).
✅ **Planos 2D/3D en AutoCAD (.DWG y PDF listos para imprimir)** y maquetas / manualidades técnicas.
✅ **Detalles constructivos en Guadua / Bambú y Metal** y tareas prácticas (SENA / UNAD / Universidad).

📲 Escríbeme directo a mi WhatsApp: **+57 322 273 9034** (Nequi / Bancolombia)."""
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

        # 6. Clientes directos en Instagram / Facebook Colombia y Proyectos Freelance
        hook = (
            "Soy especialista en **diseño y construcción de cabañas (guadua certificada, muro tendinoso, incrustaciones de botellas y vidrio), "
            "estructuras en metal y soldadura, remodelaciones, modelado 3D en Blender, planos AutoCAD y automatización**."
        )
        pricing = f"{curr} {int(p_min):,} — {int(p_max):,}" if (p_min and p_max) else "Precio cerrado por entregable"
        subject = f"Propuesta Directa: {title}"
        body = f"""¡Hola {org}! 👋 Revisé tu requerimiento **"{title}"** y puedo comenzar hoy mismo.

{hook}

1. En **menos de 24 horas** te envío el primer avance o cotización detallada.
2. Trato directo sin contratos complicados (WhatsApp directo en Colombia: **+57 322 273 9034**).

¿Me compartes los detalles por aquí o por WhatsApp para arrancar de inmediato?"""

        return {
            'language': 'es',
            'subject': subject,
            'body': body,
            'pricing_recommendation': pricing,
            'turnaround': "24 a 48 horas",
            'whatsapp_phone': wa_phone
        }
