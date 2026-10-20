class TechnicalProposalGenerator:
    """
    Genera mensajes directos (WhatsApp / Redes / SENA / Exterior / Caficultores / Alcaldía)
    100% en español, prácticos y alineados con todas las habilidades del usuario:
    - Cabañas con muro tendinoso, incrustaciones de botellas, muros en vidrio y acabados en guadua
    - Todo tipo de cubiertas y estructuras en guadua y metal (soldadura y remodelación)
    - Secaderos solares/parabólicos para café y compra/comercialización de Café Borbón Rosado de campesinos
    - Diseños de murales artísticos y tatuajes personalizados
    - Pasantías del SENA, intercambios técnicos/artísticos y oportunidades en el exterior
    """

    @classmethod
    def generate_pitch(cls, opp):
        title = opp.get('title', 'Proyecto')
        org = opp.get('organization', 'Cliente').replace('(🇨🇴 Colombia)', '').strip()
        skills_text = f"{title} {opp.get('description', '')} {' '.join(opp.get('skills', []))}".lower()
        obs = opp.get('observed_data', {})
        cat_hint = obs.get('category_hint', '')
        wa_phone = obs.get('whatsapp_phone')
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        curr = opp.get('currency') or 'COP'

        # 0. Clases de Barismo en Colegios/Veredas y Catador Q-Grader (Café de Especialidad)
        if cat_hint == 'barismo_qgrader' or any(k in skills_text for k in ['barismo', 'q-grader', 'q grader', 'catador', 'catación', 'catacion', 'arte latte']):
            subject = f"Clases de Barismo, Catación Q-Grader y Café de Especialidad en Colegios y Veredas — {org}"
            body = f"""¡Hola {org}! 👋 Un cordial saludo desde San Agustín, Huila.

Nos comunicamos respecto a **{title}** para poner a su disposición nuestros servicios profesionales de formación y control de calidad en Café de Especialidad:

☕ **1. Clases y Talleres de Barismo (Colegios, Veredas y Cafeterías)**: Formación práctica para estudiantes de colegios urbanos/rurales, jóvenes caficultores y grupos asociativos en métodos de filtrado (V60, Chemex, Aeropress, Prensa Francesa), calibración de molino, extracción de espresso y texturización / Arte Latte.
🏅 **2. Catación Q-Grader y Análisis Sensorial (Protocolo SCA / CQI)**: Evaluación física y sensorial en mesa de catación de microlotes (Borbón Rosado, Caturra, Geisha, Tabi), identificación de defectos de beneficio/secado, perfilación de taza (84 a 90+ puntos SCA) y talleres para que los productores aprendan a catar su propio café en vereda.

📲 Contacto directo por WhatsApp en San Agustín: **+57 322 273 9034**. ¿Coordinamos una sesión demostrativa o cronograma de clases para el colegio / vereda / asociación?"""
            pricing = f"COP ${int(p_min or 400000):,} — ${int(p_max or 3200000):,} (Por taller, ciclo escolar o jornada de catación Q-Grader)".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Disponibilidad inmediata en colegios y veredas de San Agustín, Isnos y Pitalito",
                'whatsapp_phone': wa_phone
            }

        # 1. Café Borbón Rosado de Campesinos & Construcción de Secaderos para Café (Guadua y Metal)
        if cat_hint == 'cafe_secaderos' or any(k in skills_text for k in ['borbón rosado', 'borbon rosado', 'secadero', 'marquesina', 'caficultor']):
            subject = f"Secaderos de Café (Guadua/Metal) y Café Borbón Rosado en San Agustín — {org}"
            body = f"""¡Hola {org}! 👋 Te saludo desde San Agustín, Huila.

Me comunico respecto a **{title}** para ponernos en contacto directo en dos frentes de trabajo:

☕ **1. Compra y Comercialización de Café Borbón Rosado**: Trabajo directamente con campesinos y fincas productoras de San Agustín y veredas (Alto del Obispo, La Estrella, El Tablón, Mesitas) para acopio y negociación directa de microlotes de **Borbón Rosado** (pergamino seco / cereza).
🎋🔩 **2. Construcción y Remodelación de Secaderos para Café**: Construyo y techo todo tipo de **secaderos parabólicos, marquesinas solares y camas africanas** combinando estructura en **guadua inmunizada y cerchas en metal soldado** con cubierta UV de alta durabilidad.

📲 Mi WhatsApp directo en San Agustín es **+57 322 273 9034**. ¿Hablamos hoy mismo para coordinar lotes de Borbón Rosado o cotizar secaderos?"""
            pricing = f"COP ${int(p_min or 850000):,} — ${int(p_max or 7500000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Atención inmediata en veredas de San Agustín y Sur del Huila",
                'whatsapp_phone': wa_phone
            }

        # 2. Diseño de Murales Artísticos y Tatuajes Personalizados
        if cat_hint == 'murales_tatuajes' or any(k in skills_text for k in ['mural', 'tatuaje', 'tattoo']):
            subject = f"Diseño de Murales Artísticos, Tatuajes y Acabados en San Agustín — {org}"
            body = f"""¡Hola {org}! 👋 Un gusto saludarte desde San Agustín, Huila.

Vi su requerimiento de **{title}** y estoy disponible para trabajar de inmediato:

🎨 **Diseño y Pintura de Murales Artísticos**: Murales de interior y exterior con identidad del Macizo Colombiano, cultura agustiniana, naturaleza y arte orgánico para hostales, cafés, cabañas y negocios.
🖋️ **Tatuajes Personalizados**: Diseño de autor (precolombino, línea fina, blackwork, neotradicional) con bioseguridad total para clientes locales y turistas.
🍾 **Arte Constructivo Integrado**: Además integro murales con **muro tendinoso, incrustaciones de botellas de vidrio y lámparas/acabados en guadua**.

📲 Escríbeme directo a mi WhatsApp **+57 322 273 9034** para enviarte fotos de mis diseños, murales y tatuajes."""
            pricing = f"COP ${int(p_min or 150000):,} — ${int(p_max or 1800000):,} (Por m² de mural o por sesión de tatuaje)".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Boceto en 24h · Disponibilidad inmediata en San Agustín",
                'whatsapp_phone': wa_phone
            }

        # 3. Pasantías del SENA, Intercambios y Oportunidades en el Exterior
        if cat_hint == 'extras_exterior' or any(k in skills_text for k in ['pasantía', 'pasantia', 'etapa productiva', 'intercambio', 'exterior', 'worldpackers']):
            subject = f"Postulación a Pasantía SENA / Intercambio Técnico y Artístico — {title}"
            body = f"""¡Hola equipo de {org}! 👋

Les escribo desde San Agustín, Huila (Colombia) para postularme formalmente a **"{title}"**.

Cuento con un perfil práctico integral y versátil:
✅ **Bioconstrucción y Guadua Certificada**: Cabañas con **muro tendinoso**, **incrustaciones de botellas**, **muros en vidrio** y todo tipo de **cubiertas en guadua y metal**.
✅ **Estructuras en Metal y Soldadura**: Fabricación, montaje y remodelación de estructuras metálicas, cubiertas y secaderos de café.
✅ **Arte Mural, Tatuaje y Diseño 3D (Blender / Planos)**: Pintura de murales temáticos, tatuaje artístico y modelado arquitectónico 3D.

Cumplo con los requisitos solicitados y tengo disponibilidad inmediata.
📲 Contacto directo / WhatsApp (Colombia): **+57 322 273 9034**."""
            pricing = f"COP ${int(p_min or 975000):,} — ${int(p_max or 12000000):,} / Intercambio Acordado".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Disponibilidad inmediata (Local, SENA o Exterior)",
                'whatsapp_phone': wa_phone
            }

        # 4. Cabañas, Bioconstrucción, Muro Tendinoso, Incrustaciones de Botellas, Vidrio, Cubiertas en Guadua y Metal
        if cat_hint in ('guadua_cabanas', 'bioconstruccion_guadua', 'metal_soldadura') or any(
            k in skills_text for k in ['guadua', 'cabaña', 'bamb', 'bioconstrucci', 'tendinoso', 'botella', 'soldadura', 'cubierta', 'metal']
        ):
            subject = f"Cabañas (Muro Tendinoso, Vidrio, Guadua), Cubiertas y Soldadura — {org}"
            body = f"""¡Hola {org}! 👋 Un gusto saludarte desde San Agustín, Huila.

Vi su requerimiento relacionado con **{title}** y me pongo a su disposición:

✅ **Cabañas y Bioconstrucción Innovadora**: Construcción y remodelación con **muro tendinoso**, **incrustaciones de botellas**, **muros en vidrio** y acabados en **guadua certificada**.
✅ **Todo Tipo de Cubiertas en Guadua y Metal + Soldadura**: Cerchas metálicas, techos mixtos (guadua + acero), plataformas para glamping, secaderos de café, portones y remodelaciones.
✅ **Arte Mural y Diseño 3D**: Pintura de murales artísticos y modelado previo en **Blender 3D / Planos** para ver cómo quedará la obra antes de construir.

📲 Estoy en San Agustín (**WhatsApp directo: +57 322 273 9034**). ¿Agendamos una visita o llamada hoy mismo para cotizar sin compromiso?"""
            pricing = f"COP ${int(p_min or 650000):,} — ${int(p_max or 4800000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Visita inmediata en San Agustín / Huila · Boceto 3D en 24-48h",
                'whatsapp_phone': wa_phone
            }

        # 5. Trabajos Informales, Segundo Tiempo y Manualidades
        if cat_hint == 'informales_manualidades' or any(
            k in skills_text for k in ['manualidad', '2do tiempo', 'segundo tiempo', 'informal', 'lámpara', 'lampara', 'artesanía']
        ):
            subject = f"Trabajos de 2do Tiempo, Manualidades, Murales y Soldadura — {org}"
            body = f"""¡Hola {org}! 👋 Te escribo desde San Agustín, Huila.

Estoy disponible para **trabajos por encargo, de segundo tiempo o fin de semana**:
🛠️ **Manualidades y Arte**: Lámparas en guadua, vitrales con botellas de vidrio, muebles en metal + guadua, pintura de murales y tatuajes.
🔩 **Soldadura, Cubiertas y Reparaciones**: Arreglo de techos/cubiertas en guadua y metal, rejas, portones y mantenimiento general.

📲 Mi WhatsApp directo en San Agustín es **+57 322 273 9034**."""
            pricing = f"COP ${int(p_min or 90000):,} — ${int(p_max or 650000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Disponibilidad inmediata / Segundo tiempo",
                'whatsapp_phone': wa_phone
            }

        # 6. General / Alcaldía / Estudiantes / Freelance
        subject = f"Propuesta Directa: {title}"
        body = f"""¡Hola {org}! 👋 Revisé la solicitud exacta de **"{title}"** y cumplo con los requisitos para iniciar de inmediato.

Realizo **bioconstrucción en guadua, muro tendinoso con botellas y vidrio, todo tipo de cubiertas y estructuras en metal/soldadura, secaderos de café, murales artísticos, modelado 3D en Blender y planos**.

📲 Contacto directo en San Agustín, Huila (Colombia): **+57 322 273 9034**."""
        pricing = f"{curr} {int(p_min):,} — {int(p_max):,}" if (p_min and p_max) else "Precio a convenir"
        return {
            'language': 'es',
            'subject': subject,
            'body': body,
            'pricing_recommendation': pricing,
            'turnaround': "24 a 48 horas",
            'whatsapp_phone': wa_phone
        }
