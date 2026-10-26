class TechnicalProposalGenerator:
    """
    Genera mensajes directos (WhatsApp / Redes / SENA / Exterior / Caficultores / Alcaldía)
    100% en español, prácticos y alineados con todas las habilidades del usuario:
    - Oportunidades de Intercambio y Residencia en Hoteles y Empresas (Tatuajes, Bioconstrucción, Web/3D, Café)
    - Cabañas con muro tendinoso, incrustaciones de botellas, muros en vidrio y acabados en guadua
    - Todo tipo de cubiertas y estructuras en guadua y metal (soldadura y remodelación)
    - Suministro de Café Borbón Rosado (tostado, molido a medida y lotes) & secaderos
    - Clases de barismo en colegios/veredas y catador Q-Grader (análisis sensorial SCA)
    - Diseños de murales artísticos y tatuajes personalizados
    - Pasantías del SENA y oportunidades oficiales en el exterior
    """

    @classmethod
    def generate_pitch(cls, opp):
        title = opp.get('title', 'Proyecto')
        org = opp.get('organization', 'Cliente').replace('(🇨🇴 Colombia)', '').strip()
        obs = opp.get('observed_data', {})
        cat_hint = (obs.get('category_hint') or opp.get('category') or '').lower()
        wa_phone = obs.get('whatsapp_phone') or opp.get('whatsapp_phone')
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        curr = opp.get('currency') or 'COP'

        title_and_desc = f"{title} {opp.get('description', '')}".lower()

        # -------------------------------------------------------------
        # 1. INTERCAMBIOS EN HOTELES, GLAMPINGS & EMPRESAS
        # -------------------------------------------------------------
        if cat_hint == 'intercambios' or any(k in title_and_desc for k in ['intercambio', 'trueque', 'residencia artística', 'residencia constructiva', 'worldpackers', 'workaway']):
            subject = f"Propuesta de Intercambio & Residencia: Tatuador, Bioconstructor, Web/3D y Café — {org}"
            body = f"""¡Hola {org}! 👋 Un cordial saludo desde San Agustín, Huila.

Me pongo en contacto respecto a su propuesta de intercambio para **"{title}"**. Cuento con un perfil técnico y artístico multidisciplinar listo para aportar valor inmediato a su proyecto:

🎨 **1. Tatuador Artístico & Muralista**: Equipo propio estéril descartable (bioseguridad profesional) para brindar sesiones de tatuaje a turistas y huéspedes extranjeros (diseños propios, simbología agustiniana, línea fina, blackwork). Pintura de murales temáticos para embellecer zonas comunes del hotel.
🎋 **2. Bioconstrucción, Cabañas & Guadua**: Construcción de cabañas orgánicas con **muro tendinoso (ferrocemento curvo)**, **incrustaciones de botellas de vidrio** para iluminación natural, **muros en vidrio** y cubiertas de gran formato en **guadua inmunizada y metal**.
💻 **3. Diseño Web con Motor de Reservas & Renders 3D (Blender)**: Creación de página web con catálogo de reservas directas por WhatsApp (sin comisiones) y levantamiento/modelado 3D fotorrealista en Blender para comercializar cabañas y espacios antes de construir.
☕ **4. Emprendimiento de Café Especial Borbón Rosado & Barismo**: Manejo de barra de café, realización de catas guiadas sensoriales (+86-88 SCA) y venta directa de paquetes de café tostado y molido de San Agustín a los huéspedes.

✅ Estoy de acuerdo con las condiciones de estadía (alojamiento + alimentación + bono o espacio comercial acordado).
📲 Mi WhatsApp directo en San Agustín es **+57 322 273 9034**. ¿Les comparto fotos de mis trabajos y coordinamos fecha de inicio?"""
            pricing = f"COP ${int(p_min or 600000):,} — ${int(p_max or 3000000):,} (Hospedaje + Comidas + Bono/Ventas)".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Disponibilidad inmediata para residencia o intercambio (San Agustín, Colombia o Exterior)",
                'whatsapp_phone': wa_phone
            }

        # -------------------------------------------------------------
        # 2. CABAÑAS EN GUADUA, BIOCONSTRUCCIÓN, MURO TENDINOSO & VIDRIO
        # -------------------------------------------------------------
        if cat_hint in ('guadua_cabanas', 'bioconstruccion_guadua') or any(
            k in title_and_desc for k in ['cabaña', 'cabana', 'glamping', 'bioconstrucci', 'tendinoso', 'incrustaci', 'muros en vidrio', 'vidrio']
        ) and not any(k in title_and_desc for k in ['comprador', 'exportador', 'borbón rosado', 'borbon rosado']):
            subject = f"Cabañas (Muro Tendinoso, Incrustación de Botellas, Vidrio y Guadua) — {org}"
            body = f"""¡Hola {org}! 👋 Un gusto saludarte desde San Agustín, Huila.

Vi su requerimiento relacionado con **{title}** y me pongo a su entera disposición:

🎋 **1. Cabañas y Bioconstrucción Innovadora**: Construcción y diseño con **muro tendinoso (ferrocemento curvo orgánico)**, **incrustaciones de botellas de vidrio** para iluminación arquitectónica y vitrales, y acabados de primera en **guadua inmunizada certificada**.
🪟 **2. Muros en Vidrio Panorámicos**: Integración limpia de ventanales y muros en vidrio para conectar las cabañas con el paisaje natural del Huila.
📐 **3. Diseño Previo en Blender 3D y Planos**: Modelado digital en 3D antes de iniciar la obra para visualizar distribución, iluminación y volúmenes con exactitud.
🔩 **4. Cubiertas Mixtas en Guadua y Metal**: Techos resistentes con anclajes metálicos soldados para proteger la estructura de la humedad.

📲 Estoy en San Agustín (**WhatsApp directo: +57 322 273 9034**). ¿Agendamos una visita al terreno o llamada hoy mismo para cotizar a su medida?"""
            pricing = f"COP ${int(p_min or 650000):,} — ${int(p_max or 4800000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Visita inmediata en San Agustín / Huila · Boceto 3D en 24-48h",
                'whatsapp_phone': wa_phone
            }

        # -------------------------------------------------------------
        # 3. COMPRADORES DE CAFÉ BORBÓN ROSADO & PRODUCTORES
        # -------------------------------------------------------------
        if cat_hint == 'cafe_secaderos' or any(
            k in title_and_desc for k in ['borbón rosado', 'borbon rosado', 'pink bourbon', 'comprador', 'microlote', 'café especial', 'cafe especial', 'tostado', 'molienda', 'lotes grandes']
        ):
            subject = f"Suministro Directo de Café Especial Borbón Rosado (Tostado, Molido a Medida y Lotes) — Origen San Agustín, Huila"
            body = f"""¡Hola {org}! 👋 Un cordial saludo desde San Agustín, Huila.

Somos un emprendimiento productor y comercializador de **Café Especial de Origen San Agustín / Sur del Huila** con perfilación sensorial avalada por **Catador Q-Grader (+85 a 89 puntos SCA)** y nos comunicamos respecto a **{title}**:

☕ **1. Café Borbón Rosado Tostado y Molido a Medida**: Entregamos en grano entero o con el **nivel exacto de molienda** (fina espresso, media V60/Chemex/filtro, gruesa prensa francesa) y **curva de tostión** (clara, media o media-oscura) que requiera su empresa o cliente (presentaciones de 250g, 500g y bolsas institucionales por kilos con válvula desgasificadora).
📦 **2. Lotes Más Grandes y Microlotes**: Disponibilidad de lotes mayores en pergamino seco seleccionado (humedad 10%-11.5%), café verde tipo exportación o tostado por volumen con trazabilidad directa de vereda en San Agustín (Alto del Obispo, La Estrella, El Tablón, Los Cauchos).
🏅 **3. Calidad Garantizada**: Perfil dulce, limpio, notas a panela, melocotón y flor de café, libre de defectos primarios.

📲 Nuestro WhatsApp directo es **+57 322 273 9034**. ¿A qué dirección o laboratorio les enviamos muestra física y ficha técnica de nuestro Borbón Rosado?"""
            pricing = f"COP ${int(p_min or 850000):,} — ${int(p_max or 35000000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Despacho inmediato de muestras y pedidos desde San Agustín, Huila",
                'whatsapp_phone': wa_phone
            }

        # -------------------------------------------------------------
        # 4. ESTRUCTURAS EN METAL, SOLDADURA ESTRUCTURAL & CUBIERTAS
        # -------------------------------------------------------------
        if cat_hint == 'metal_soldadura' or any(
            k in title_and_desc for k in ['soldadura', 'soldador', 'cercha', 'portón', 'porton', 'baranda', 'ornamentaci', 'acero', 'hierro']
        ):
            subject = f"Estructuras Metálicas, Soldadura Estructural y Cubiertas — {org}"
            body = f"""¡Hola {org}! 👋 Un cordial saludo desde San Agustín, Huila.

Me pongo en contacto respecto a su requerimiento de **{title}**:

🔩 **1. Soldadura y Estructuras Metálicas**: Fabricación y montaje de cerchas, perfiles estructurales, pórticos, plataformas elevadas para glampings, balcones y barandas de seguridad.
🏠 **2. Cubiertas y Techos Mixtos**: Instalación y remodelación de cubiertas en estructura metálica combinada con guadua tratada, impermeabilización y canales pluviales.
🛠️ **3. Remodelación y Mantenimiento**: Refuerzo de estructuras existentes, portones y ornamentación metálica de alta resistencia.

📲 WhatsApp directo en San Agustín: **+57 322 273 9034**. Cuento con equipo propio (inversor, pulidora, herramienta de corte) y disponibilidad inmediata."""
            pricing = f"COP ${int(p_min or 550000):,} — ${int(p_max or 3800000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Visita y presupuesto detallado en el día",
                'whatsapp_phone': wa_phone
            }

        # -------------------------------------------------------------
        # 5. CLASES DE BARISMO EN COLEGIOS/VEREDAS & Q-GRADER
        # -------------------------------------------------------------
        if cat_hint == 'barismo_qgrader' or any(
            k in title_and_desc for k in ['barismo', 'q-grader', 'q grader', 'catador', 'catación', 'catacion', 'arte latte']
        ):
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

        # -------------------------------------------------------------
        # 6. DISEÑO DE MURALES ARTÍSTICOS & TATUAJES
        # -------------------------------------------------------------
        if cat_hint == 'murales_tatuajes' or any(
            k in title_and_desc for k in ['mural', 'tatuaje', 'tattoo']
        ):
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

        # -------------------------------------------------------------
        # 7. PASANTÍAS SENA & CONVOCATORIAS EXTERIOR
        # -------------------------------------------------------------
        if cat_hint == 'extras_exterior' or any(
            k in title_and_desc for k in ['pasantía', 'pasantia', 'etapa productiva', 'ape sena', 'canadá', 'españa']
        ):
            subject = f"Postulación a Pasantía SENA / Convocatoria Internacional — {title}"
            body = f"""¡Hola equipo de {org}! 👋

Les escribo desde San Agustín, Huila (Colombia) para postularme formalmente a **"{title}"**.

Cuento con un perfil técnico certificado y experiencia práctica verificable:
✅ **Bioconstrucción y Guadua Certificada**: Cabañas con muro tendinoso, botellas de vidrio y cubiertas en guadua.
✅ **Estructuras en Metal y Soldadura**: Armado y soldadura de cerchas, plataformas y cubiertas estructurales.
✅ **Modelado 3D (Blender / Planos)** y acabados artísticos.

Cumplo con los requisitos solicitados y tengo total disponibilidad de inicio.
📲 Contacto directo / WhatsApp (Colombia): **+57 322 273 9034**."""
            pricing = f"COP ${int(p_min or 975000):,} — ${int(p_max or 12000000):,}".replace(',', '.')
            return {
                'language': 'es',
                'subject': subject,
                'body': body,
                'pricing_recommendation': pricing,
                'turnaround': "Disponibilidad inmediata (Local, SENA o Exterior)",
                'whatsapp_phone': wa_phone
            }

        # -------------------------------------------------------------
        # 8. TRABAJOS INFORMALES, SEGUNDO TIEMPO & MANUALIDADES
        # -------------------------------------------------------------
        if cat_hint == 'informales_manualidades' or any(
            k in title_and_desc for k in ['manualidad', '2do tiempo', 'segundo tiempo', 'informal', 'lámpara', 'lampara', 'artesanía']
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

        # -------------------------------------------------------------
        # 9. GENERAL / ALCALDÍA / ESTUDIANTES / FREELANCE
        # -------------------------------------------------------------
        subject = f"Propuesta Directa: {title}"
        body = f"""¡Hola {org}! 👋 Revisé la solicitud exacta de **"{title}"** y cumplo con los requisitos para iniciar de inmediato.

Realizo **bioconstrucción en guadua, muro tendinoso con botellas y vidrio, todo tipo de cubiertas y estructuras en metal/soldadura, café especial borbón rosado, murales artísticos, modelado 3D en Blender y planos**.

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
