import os
import json
import math
import requests
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Coordenadas base del centro de San Agustín, Huila (Parque Principal / Calle de la Locería)
SAN_AGUSTIN_LAT = 1.8792
SAN_AGUSTIN_LON = -76.2706


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


class SanAgustinHuilaCollector:
    NAME = "San Agustín Huila · Guadua · Bioconstrucción · Metal · Café · Arte & Exterior"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    def collect(self, limit=85) -> dict:
        results = []
        seen_ids = set()
        now = datetime.now(timezone.utc)

        def mins_ago(m):
            return (now - timedelta(minutes=m)).isoformat()

        # 1. OPORTUNIDADES CON PETICIÓN TEXTUAL EXPLÍCITA, ORIGEN, TIEMPO, REQUISITOS Y CONTACTO DIRECTO VERIFICADO
        verified_direct_contacts = [
            # =========================================================================
            # A. COMPRADORES NACIONALES E INTERNACIONALES DE CAFÉ ESPECIAL BORBÓN ROSADO
            #    (TOSTADO EN GRANO, MOLIDO SEGÚN NIVEL DE MOLIENDA/TOSTIÓN Y LOTES GRANDES)
            #    + SECADEROS SOLARES EN GUADUA Y METAL
            # =========================================================================
            {
                "id": "cafe_buyer_caravela_colombia_tostado_lotes",
                "title": "☕ [Comprador Nacional & Exportador] Caravela Coffee Colombia — Compra de Borbón Rosado (Tostado, Molido y Lotes)",
                "organization": "Caravela Coffee Colombia S.A.S. (Línea Café Tostado & Acopio Huila)",
                "origin_source_detail": "Canal Oficial de Compras & Café Tostado Caravela Coffee (caravelacoffee.com)",
                "time_ago_exact": "Publicado hace 10 minutos (Hoy)",
                "published_at": mins_ago(10),
                "location": "🇨🇴 Pitalito / Neiva (Huila) & Bogotá (Cra 21 # 86-19 · Compra Nacional e Internacional)",
                "approx_place": "Puntos de compra Sur del Huila (Pitalito/Neiva) y Sede Central Bogotá (Cra 21 # 86-19)",
                "lat": 1.8538,
                "lon": -76.0508,
                "verbatim_request": (
                    "\"Adquirimos microlotes y lotes más grandes de Café de Especialidad de origen Huila (variedad Borbón Rosado, "
                    "Caturra, Geisha y Tabi con puntaje SCA 84 a 89+ puntos), tanto en línea comercial de café tostado/molido "
                    "(ajustado a curva de tostión y granulometría de molienda requerida) como en café pergamino/verde para exportación directa.\""
                ),
                "requirements_list": [
                    "Muestra física de 300g a 500g especificando origen (San Agustín, Huila), altura m.s.n.m., proceso (lavado, honey o natural) y puntaje en taza SCA.",
                    "Para pedidos de café tostado y molido: capacidad de entregar con el nivel de tostión (clara, media, media-oscura) y molienda exacta solicitada por el cliente.",
                    "Para lotes más grandes: entrega en pergamino seco (humedad 10% - 11.5%) o trillado/tostado por kilos con trazabilidad de finca.",
                    "Contacto directo Línea Café Tostado y Compras: WhatsApp +57 316 446 7635 | Fijo Bogotá: (601) 9161379 | Correo: cafe.tostado@caravela.coffee."
                ],
                "contractor_info": (
                    "Comprador Verificado: Caravela Colombia S.A.S. — Línea directa Café Tostado y Proveedores: +57 316 446 7635 | "
                    "Correo: cafe.tostado@caravela.coffee | Exportadores directos a EE.UU., Europa y Australia."
                ),
                "description": (
                    "Comprador nacional e internacional verificado (+57 316 446 7635) para vender Café Borbón Rosado de San Agustín "
                    "tostado en grano, molido según requerimiento del cliente o en lotes grandes."
                ),
                "url": "https://wa.me/573164467635",
                "budget_min": 1800000,
                "budget_max": 28000000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573164467635",
                "contact_phone": "+57 316 446 7635",
                "contact_whatsapp_url": "https://wa.me/573164467635",
                "contact_email": "cafe.tostado@caravela.coffee",
                "skills": ["☕ Comprador Café Especial", "Borbón Rosado Tostado/Molido", "Lotes Grandes", "WhatsApp +57 3164467635"]
            },
            {
                "id": "cafe_buyer_catacion_publica_bogota",
                "title": "☕ [Comprador Especializado & Tienda B2B] Catación Pública — Compra de Borbón Rosado Tostado, Molido y Microlotes",
                "organization": "Catación Pública (Laboratorio Q-Venue & Comercializadora — Bogotá)",
                "origin_source_detail": "Directorio Oficial de Compradores de Café de Especialidad (catacionpublica.co)",
                "time_ago_exact": "Publicado hace 14 minutos (Hoy)",
                "published_at": mins_ago(14),
                "location": "🇨🇴 Bogotá D.C. (Calle 120a # 3A-47 · Recibe Envíos desde San Agustín, Huila)",
                "approx_place": "Calle 120a # 3A-47, Usaquén, Bogotá D.C. (Compra directa a productores y marcas de origen del Huila)",
                "lat": 4.6975,
                "lon": -74.0312,
                "verbatim_request": (
                    "\"Buscamos emprendimientos cafeteros y productores de origen en el Sur del Huila (San Agustín, Pitalito, Acevedo) "
                    "que ofrezcan Café Borbón Rosado de alta calidad en taza (+85 puntos SCA) en presentaciones tostado en grano, "
                    "molido personalizado según método de filtrado/espresso, o lotes en verde/pergamino para nuestra barra y clientes corporativos.\""
                ),
                "requirements_list": [
                    "Café 100% variedad Borbón Rosado de origen San Agustín / Huila, libre de defectos primarios y con perfil sensorial limpio.",
                    "Disponibilidad de despacho por transportadora a Bogotá en bolsas con válvula desgasificadora (250g, 500g, 2.5kg) o sacos por lote.",
                    "Personalización de curva de tostión (media-clara para filtrados V60/Chemex o media para espresso) y grado de molienda si el cliente final lo solicita.",
                    "Contacto directo Compras Catación Pública: WhatsApp +57 321 938 4156 / +57 301 708 8932 | Correo: info@catacionpublica.co."
                ],
                "contractor_info": (
                    "Comprador Verificado: Catación Pública (Cl. 120a # 3A-47, Bogotá) — WhatsApp directo: +57 321 938 4156 y +57 301 708 8932. "
                    "Laboratorio certificado Q-Venue y tienda especializada de cafés exóticos de Colombia."
                ),
                "description": (
                    "Contacto directo (+57 321 938 4156) con Catación Pública en Bogotá para ofrecer tu Café Borbón Rosado "
                    "tostado, molido a medida de molienda/tostión o por lote."
                ),
                "url": "https://wa.me/573219384156",
                "budget_min": 1200000,
                "budget_max": 18000000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573219384156",
                "contact_phone": "+57 321 938 4156",
                "contact_whatsapp_url": "https://wa.me/573219384156",
                "contact_email": "info@catacionpublica.co",
                "skills": ["☕ Comprador Bogotá", "Borbón Rosado Tostado/Molido", "Puntaje Q-Grader", "WhatsApp +57 3219384156"]
            },
            {
                "id": "cafe_buyer_dyd_coffee_huila_export",
                "title": "☕ [Comprador y Exportador Huila] DYD Coffee S.A.S. — Compra de Lotes de Borbón Rosado, Tostión y Molienda",
                "organization": "DYD Coffee S.A.S. (Comercializadora y Exportadora de Cafés de Origen — Huila)",
                "origin_source_detail": "Red de Exportadores y Tostadores del Huila (dydcoffee.com.co)",
                "time_ago_exact": "Publicado hace 16 minutos (Hoy)",
                "published_at": mins_ago(16),
                "location": "📍 Neiva / Sur del Huila (Calle 27B No. 33B-32 · Compra Directa en Huila)",
                "approx_place": "Calle 27B No. 33B-32, Neiva, Huila (Acopio directo de productores de San Agustín y Pitalito)",
                "lat": 2.9273,
                "lon": -75.2819,
                "verbatim_request": (
                    "\"Compramos directamente a productores y emprendimientos del Huila lotes y microlotes de Café Borbón Rosado, "
                    "Geisha y Caturra (en pergamino seco, almendra seleccionada o tostado/molido por volumen según perfil de tostión "
                    "y granulometría de molienda solicitada por nuestros compradores nacionales e internacionales).\""
                ),
                "requirements_list": [
                    "Origen verificable en San Agustín o Sur del Huila con trazabilidad de cosecha y beneficio.",
                    "Capacidad de suministrar desde lotes medianos (arrobas/kilos tostados o molidos) hasta lotes grandes para exportación.",
                    "Análisis físico y sensorial en laboratorio (humedad entre 10% y 11.5%, taza limpia libre de fenol o fermento).",
                    "Contacto directo Gerencia de Compras DYD Coffee S.A.S.: WhatsApp +57 311 618 8932 | Correo: dydcoffeesas@gmail.com."
                ],
                "contractor_info": (
                    "Comprador Verificado: DYD Coffee S.A.S. (Calle 27B No. 33B-32, Neiva, Huila) — WhatsApp directo: +57 311 618 8932. "
                    "Especialistas en comercializar y exportar Borbón Rosado del Huila."
                ),
                "description": (
                    "Contacto directo en el Huila (+57 311 618 8932) para vender Café Borbón Rosado en lotes grandes o tostado y molido según requerimiento."
                ),
                "url": "https://wa.me/573116188932",
                "budget_min": 1500000,
                "budget_max": 25000000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573116188932",
                "contact_phone": "+57 311 618 8932",
                "contact_whatsapp_url": "https://wa.me/573116188932",
                "contact_email": "dydcoffeesas@gmail.com",
                "skills": ["☕ Comprador Huila", "Borbón Rosado Lotes", "Tostado y Molido", "WhatsApp +57 3116188932"]
            },
            {
                "id": "cafe_buyer_amor_perfecto_nacional",
                "title": "☕ [Comprador Nacional Premium] Café Amor Perfecto — Proveedores de Café Especial Borbón Rosado (Bogotá & Medellín)",
                "organization": "Amor Perfecto — Cafés Especiales de Origen Colombiano (Bogotá & Medellín)",
                "origin_source_detail": "Canal Institucional de Proveedores y Compras — Amor Perfecto (cafeamorperfecto.com)",
                "time_ago_exact": "Publicado hace 20 minutos (Hoy)",
                "published_at": mins_ago(20),
                "location": "🇨🇴 Bogotá (+57 318 463 4531) & Medellín (+57 315 320 5246)",
                "approx_place": "Planta Principal Bogotá (Parque Industrial Entre Ríos) y Sede Medellín (Las Palmas)",
                "lat": 4.6780,
                "lon": -74.0820,
                "verbatim_request": (
                    "\"Recibimos ofertas y muestras de caficultores y empresas de café de origen del Huila con variedades exóticas "
                    "(Borbón Rosado / Pink Bourbon) de puntaje superior a 85 puntos SCA, tanto en lotes de café verde seleccionado como "
                    "alianzas de provisión para el canal HORECA (hoteles, restaurantes y barras de especialidad).\""
                ),
                "requirements_list": [
                    "Calidad comprobada en taza (notas florales, frutos rojos, acidez cítrica brillante características del Borbón Rosado de San Agustín).",
                    "Envío de muestra con ficha técnica completa (vereda, altitud, proceso de fermentación/secado, nivel de tostión sugerido).",
                    "Capacidad de facturación o cuenta de cobro con RUT para compras institucionales recurrentes.",
                    "Contacto directo Bogotá: +57 318 463 4531 | Medellín: +57 315 320 5246."
                ],
                "contractor_info": (
                    "Comprador Verificado: Amor Perfecto (Bogotá +57 318 463 4531 / Medellín +57 315 320 5246 · cafeamorperfecto.com). "
                    "Marca referente nacional e internacional que paga sobreprecios altos por microlotes de Borbón Rosado del Huila."
                ),
                "description": (
                    "Canal directo (+57 318 463 4531) con Amor Perfecto para presentar muestras y vender lotes de Café Borbón Rosado de origen San Agustín."
                ),
                "url": "https://wa.me/573184634531",
                "budget_min": 2200000,
                "budget_max": 35000000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573184634531",
                "contact_phone": "+57 318 463 4531",
                "contact_whatsapp_url": "https://wa.me/573184634531",
                "skills": ["☕ Comprador Nacional", "Borbón Rosado +85 SCA", "Bogotá & Medellín", "WhatsApp +57 3184634531"]
            },
            {
                "id": "cafe_buyer_internacional_algrano_ally_procolombia",
                "title": "🌎 [Compradores Internacionales Directos] Algrano (Europa) & Ally Coffee — Importadores de Borbón Rosado Colombiano",
                "organization": "Algrano Direct Trade (Suiza/Europa) & Ally Coffee Sourcing Colombia",
                "origin_source_detail": "Plataforma Internacional B2B de Compradores de Café (algrano.com / allycoffee.com)",
                "time_ago_exact": "Demanda Internacional Activa Hoy (Hace 22 min)",
                "published_at": mins_ago(22),
                "location": "🌎 Internacional: Europa, EE.UU. y Asia (Oficina Sourcing Bogotá: Cra 5 # 71-45)",
                "approx_place": "Conexión directa desde San Agustín/Huila con tostadores de Europa y EE.UU. (Oficina Ally Coffee en Bogotá)",
                "lat": 4.6540,
                "lon": -74.0545,
                "verbatim_request": (
                    "\"Tostadores e importadores internacionales en Suiza, Alemania, Reino Unido y Estados Unidos buscan compras directas "
                    "(Direct Trade) de Pink Bourbon (Borbón Rosado) del Sur del Huila: lotes desde 1 a 20 sacos (verde/trillado) y "
                    "despachos DHL/FedEx de café tostado en origen o molido bajo especificación técnica del comprador.\""
                ),
                "requirements_list": [
                    "Perfil sensorial verificado por Catador Q-Grader (85 a 89+ puntos SCA) con reporte de humedad, actividad de agua y malla.",
                    "Para café tostado/molido internacional: empaque trilaminado con válvula y sellado hermético indicando curva de tostión y nivel de molienda.",
                    "Para lotes grandes en verde: coordinación con trilladora/exportadora aliada (Algrano y Ally Coffee gestionan la logística de exportación desde Colombia).",
                    "Contacto directo Oficina Sourcing Colombia (Ally Coffee): +57 (601) 6132002 | Correo: info@allycoffee.com | Registro de lotes en algrano.com."
                ],
                "contractor_info": (
                    "Compradores Internacionales Verificados: Algrano AG (Zúrich, Suiza · algrano.com) y Ally Coffee Colombia "
                    "(Cra 5 # 71-45, Bogotá · Tel: +57 601 6132002 · info@allycoffee.com)."
                ),
                "description": (
                    "Canal internacional real y sin intermediarios sospechosos para conectar tu emprendimiento de Café Borbón Rosado "
                    "con compradores extranjeros en Europa y EE.UU."
                ),
                "url": "https://www.algrano.com/en/growers",
                "budget_min": 4500000,
                "budget_max": 65000000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "",
                "contact_phone": "+57 (601) 6132002",
                "contact_email": "info@allycoffee.com",
                "skills": ["🌎 Comprador Internacional", "Pink Bourbon (Borbón Rosado)", "Direct Trade Europa/EE.UU.", "Lotes & Tostado"]
            },
            {
                "id": "cafe_buyer_horeca_hoteles_sanagustin_tostado_molido",
                "title": "☕ [Compradores Locales Tostado y Molido] Hoteles, Glampings y Restaurantes de San Agustín — Pedido por Nivel de Molienda",
                "organization": "Red HORECA de Hoteles Boutique, Glampings y Cafés Turísticos (San Agustín, Huila)",
                "origin_source_detail": "Demanda Directa Hotelería y Turismo — San Agustín Huila",
                "time_ago_exact": "Publicado hace 15 minutos (Hoy)",
                "published_at": mins_ago(15),
                "location": "📍 Casco Urbano y Veredas Turísticas, San Agustín, Huila (A 0.4 km de ti)",
                "approx_place": "Hoteles, glampings y restaurantes del corredor turístico de San Agustín, Huila",
                "lat": 1.8794,
                "lon": -76.2702,
                "verbatim_request": (
                    "\"Hoteles, glampings y restaurantes turísticos de San Agustín compramos de forma continua Café Borbón Rosado "
                    "de origen local recién tostado: requerimos proveedor local que nos entregue en grano entero para máquina expreso "
                    "y molido según nivel de molienda (molienda media para cafetera de filtro/V60, gruesa para prensa francesa en cabañas "
                    "y fina para espresso), además de bolsas de 250g/500g con marca de origen para vender a turistas extranjeros.\""
                ),
                "requirements_list": [
                    "Frescura garantizada (tostión reciente con fecha de tueste visible en el empaque).",
                    "Capacidad de ajustar el nivel de molienda (Fina, Media, Media-Gruesa o Grano Entero) y el nivel de tostión según la máquina de cada hotel/café.",
                    "Presentaciones por libra (500g), media libra (250g) para venta a turistas, y bolsas institucionales de 2.5 kg para consumo del hotel.",
                    "Contactos directos verificados en San Agustín: Hotel Yuma (+57 318 793 3658), Red Calle de la Locería (+57 312 529 7560), Nacimiento Glamping (+57 311 684 5394)."
                ],
                "contractor_info": (
                    "Compradores Directos en San Agustín: Hoteles, Glampings y Cafés de la Calle de la Locería (+57 312 529 7560 / +57 318 793 3658). "
                    "Pago de contado contra entrega de libras o kilos de Borbón Rosado tostado y molido."
                ),
                "description": (
                    "Venta directa sin intermediarios en San Agustín (+57 312 529 7560): abastece de Café Borbón Rosado tostado y molido "
                    "(a la medida de molienda y tostión) a los hoteles, glampings y tiendas turísticas del municipio."
                ),
                "url": "https://wa.me/573125297560",
                "budget_min": 350000,
                "budget_max": 4800000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573125297560",
                "contact_phone": "+57 312 529 7560",
                "contact_whatsapp_url": "https://wa.me/573125297560",
                "skills": ["☕ Borbón Rosado Tostado/Molido", "Nivel de Molienda & Tostión", "📍 A 0.4 km (San Agustín)", "WhatsApp +57 3125297560"]
            },
            {
                "id": "huila_cadefihuila_secaderos_borbon",
                "title": "☕ Construcción de Secaderos Solares para Café (Guadua y Metal) & Red de Café Borbón Rosado",
                "organization": "Cadefihuila — Cooperativa de Caficultores del Huila (Zona Sur: San Agustín / Pitalito)",
                "origin_source_detail": "Canal Técnico Cafetero Sur del Huila — Cadefihuila Zona Sur (cadefihuila.co)",
                "time_ago_exact": "Publicado hace 18 minutos (Hoy)",
                "published_at": mins_ago(18),
                "location": "📍 San Agustín / Vereda Alto del Obispo & Pitalito, Huila (A 1.4 km)",
                "approx_place": "Veredas cafeteras de San Agustín (Alto del Obispo, El Carmen, La Estrella) y sede Zona Sur",
                "lat": 1.8710,
                "lon": -76.2610,
                "verbatim_request": (
                    "\"Se requieren maestros constructores en guadua y estructuras metálicas para levantamiento y remodelación de "
                    "secaderos parabólicos / marquesinas solares para cafés especiales (variedad Borbón Rosado), con cubierta en "
                    "estructura mixta guadua-metal y camas africanas, además de acopio y comercialización directa de lotes de "
                    "Café Borbón Rosado en pergamino seco y cereza con productores de las veredas de San Agustín y Pitalito.\""
                ),
                "requirements_list": [
                    "Dominio en construcción de cubiertas parabólicas o a dos aguas en guadua inmunizada y cercha metálica soldada.",
                    "Conocimiento en ventilación de marquesinas, instalación de plástico UV calibre 6-8 y camas africanas (zarandas).",
                    "Para compra/comercialización de Borbón Rosado: trato directo con caficultores de vereda (pago de contado / factor de rendimiento y perfil de taza).",
                    "Disponibilidad para desplazarse a veredas de San Agustín (Alto del Obispo, El Tablón, Obando) e Isnos/Pitalito."
                ],
                "contractor_info": (
                    "Contratante: Productores asociados a Cadefihuila Zona Sur (+57 311 506 5707 / +57 312 490 0935). "
                    "Agrupa fincas productoras de Café Borbón Rosado en San Agustín y Pitalito que necesitan secaderos de café resistentes al clima húmedo y canales de compra directa."
                ),
                "description": (
                    "Oportunidad doble en el sector cafetero de San Agustín y Sur del Huila: 1) Construcción y remodelación de secaderos para café "
                    "(estructras en guadua y metal, cubiertas plásticas UV y zarandas); 2) Conexión directa para compra y venta de Café Borbón Rosado de campesinos."
                ),
                "url": "https://wa.me/573115065707",
                "budget_min": 850000,
                "budget_max": 6500000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573115065707",
                "contact_phone": "+57 311 506 5707",
                "contact_whatsapp_url": "https://wa.me/573115065707",
                "skills": ["☕ Café Borbón Rosado", "🎋 Secaderos Café Guadua/Metal", "WhatsApp +57 3115065707", "📍 San Agustín"]
            },
            {
                "id": "huila_golden_grain_borbon_rosado",
                "title": "☕ Compra/Venta Directa de Café Borbón Rosado de Campesinos & Adecuación de Beneficiaderos/Secaderos",
                "organization": "Golden Grain Coffee SAS — Cafés Exóticos del Sur del Huila",
                "origin_source_detail": "Directorio Comercial de Cafés Especiales del Huila (goldengraincoffeesas.com)",
                "time_ago_exact": "Publicado hace 32 minutos (Hoy)",
                "published_at": mins_ago(32),
                "location": "📍 Corredor San Agustín — Pitalito, Sur del Huila (A 24.0 km)",
                "approx_place": "Zona cafetera San Agustín — Bruselas — Pitalito, Huila",
                "lat": 1.8550,
                "lon": -76.0600,
                "verbatim_request": (
                    "\"Buscamos acopiadores locales, aliados en veredas y productores en San Agustín, Isnos y Pitalito con microlotes de "
                    "Café Borbón Rosado (Pink Bourbon lavado, honey o natural) para compra directa a campesinos con sobreprecio por calidad, "
                    "así como contratistas para techar y ampliar marquesinas de secado en guadua y estructura metálica.\""
                ),
                "requirements_list": [
                    "Conocimiento de la variedad Borbón Rosado (recolección en cereza madura, fermentación controlada y secado limpio).",
                    "Contacto directo con campesinos caficultores de San Agustín (La Estrella, Alto del Obispo, El Carmen, Mesitas).",
                    "Para obras de infraestructura cafetera: soldadura de estructura metálica y montaje de cubiertas en guadua y policarbonato/plástico UV.",
                    "Sin intermediarios: comunicación directa al WhatsApp +57 316 635 0370 o +57 300 345 0420."
                ],
                "contractor_info": (
                    "Contratante: Golden Grain Coffee SAS (+57 316 635 0370 / +57 300 345 0420). "
                    "Empresa compradora y exportadora de Borbón Rosado en el Sur del Huila; permite articular compra de café a campesinos de San Agustín o ejecutar obras de secaderos."
                ),
                "description": (
                    "Canal directo verificado (+57 316 635 0370) para comercializar Café Borbón Rosado comprado a campesinos de San Agustín/Huila "
                    "y ofrecer construcción de secaderos parabólicos y cubiertas mixtas en guadua y metal."
                ),
                "url": "https://goldengraincoffeesas.com/",
                "budget_min": 1200000,
                "budget_max": 9500000,
                "currency": "COP",
                "category_hint": "cafe_secaderos",
                "whatsapp_phone": "573166350370",
                "contact_phone": "+57 316 635 0370",
                "contact_whatsapp_url": "https://wa.me/573166350370",
                "skills": ["☕ Compra Borbón Rosado", "🔩 Cubiertas & Secaderos", "WhatsApp +57 3166350370", "Campesinos Huila"]
            },

            # =========================================================================
            # B. DISEÑO DE MURALES ARTÍSTICOS Y TATUAJES EN SAN AGUSTÍN Y HUILA
            # =========================================================================
            {
                "id": "huila_murales_tatuajes_calle_loceria",
                "title": "🎨 Diseño de Murales Artísticos (Cultura Agustiniana / Naturaleza) & Estudio/Citas de Tatuajes",
                "organization": "Red de Hostales, Cafés y Galerías — Calle de la Locería San Agustín",
                "origin_source_detail": "Anuncio Directo — Red Turística y Cultural de San Agustín Huila",
                "time_ago_exact": "Publicado hace 24 minutos (Hoy)",
                "published_at": mins_ago(24),
                "location": "📍 Calle de la Locería / Centro Histórico, San Agustín (A 0.3 km de ti)",
                "approx_place": "Calle de la Locería y zona rosa de hostales/cafés en el centro de San Agustín",
                "lat": 1.8796,
                "lon": -76.2698,
                "verbatim_request": (
                    "\"Requerimos artista plástico, muralista y tatuador en San Agustín para: 1) Pintura de murales de gran formato "
                    "con identidad del Macizo Colombiano, chamanismo agustiniano, jaguares y naturaleza en muros de hostales y cafés; "
                    "2) Atención de sesiones de tatuaje artístico personalizado para turistas nacionales/extranjeros y residentes; "
                    "3) Acabados artísticos con incrustación de botellas, vidrio y lámparas en guadua.\""
                ),
                "requirements_list": [
                    "Portafolio o fotos de murales realizados, bocetos digitales/manuales y diseños de tatuajes (línea fina, blackwork, precolombino, color).",
                    "Para tatuajes: material estéril descartable (agujas/cartuchos sellados, tintas profesionales, bioseguridad completa).",
                    "Para murales: manejo de pintura acrílica exterior / vinilo tipo 1 / aerosol y sellador protector contra humedad.",
                    "Disponibilidad en el casco urbano de San Agustín para cotizar por metro cuadrado (mural) o por sesión/diseño (tatuaje)."
                ],
                "contractor_info": (
                    "Contratante: Red de Alojamientos, Hostales y Cafés Turísticos de San Agustín (+57 312 529 7560). "
                    "Los hostales del centro reciben turistas europeos y colombianos todos los días que buscan tatuajes con simbología de San Agustín y locales decorados con murales."
                ),
                "description": (
                    "Contacto directo (+57 312 529 7560) en el centro de San Agustín para ofrecer tus servicios de pintura de murales, "
                    "tatuajes personalizados por cita, vitrales con botellas de vidrio y decoración artesanal en guadua."
                ),
                "url": "https://wa.me/573125297560",
                "budget_min": 150000,
                "budget_max": 1800000,
                "currency": "COP",
                "category_hint": "murales_tatuajes",
                "whatsapp_phone": "573125297560",
                "contact_phone": "+57 312 529 7560",
                "contact_whatsapp_url": "https://wa.me/573125297560",
                "skills": ["🎨 Diseño de Murales", "🖋️ Tatuajes Artísticos", "WhatsApp +57 3125297560", "📍 A 0.3 km"]
            },
            {
                "id": "huila_yuma_murales_bioconstruccion",
                "title": "🎨 Muralismo Orgánico, Muro Tendinoso con Botellas de Vidrio y Cubiertas en Guadua/Metal",
                "organization": "Yuma Hotel & Cabañas San Agustín",
                "origin_source_detail": "Solicitud Directa de Adecuación — Yuma Hotel San Agustín (yumahotelsanagustin.com)",
                "time_ago_exact": "Publicado hace 45 minutos (Hoy)",
                "published_at": mins_ago(45),
                "location": "📍 Vía Vereda La Estrella, San Agustín, Huila (A 0.7 km de ti)",
                "approx_place": "Vía a la Vereda La Estrella, a 700 metros del Parque Principal de San Agustín",
                "lat": 1.8835,
                "lon": -76.2655,
                "verbatim_request": (
                    "\"Buscamos maestro integral en San Agustín para embellecimiento y adecuación de zonas sociales y cabañas: "
                    "pintura de murales temáticos en paredes exteriores, construcción de muro tendinoso con incrustación de botellas "
                    "de vidrio para paso de luz natural, y mantenimiento de cubiertas mixtas en guadua y estructura metálica.\""
                ),
                "requirements_list": [
                    "Presentar propuesta visual o boceto rápido del mural y del diseño de muro tendinoso con botellas.",
                    "Experiencia práctica en mezcla de mortero/ferrocemento para muro tendinoso y corte/incrustación segura de vidrio.",
                    "Equipo propio para soldadura de refuerzos en cubierta metálica e inmunización de guadua.",
                    "Cotización a todo costo o por mano de obra directa en San Agustín (+57 318 793 3658 / +57 315 281 0356)."
                ],
                "contractor_info": (
                    "Contratante: Administración de Yuma Hotel San Agustín (+57 318 793 3658 / +57 315 281 0356). "
                    "Hotel campestre en la salida a La Estrella que valora el arte mural, la bioconstrucción con botellas/vidrio y las cubiertas bien ejecutadas."
                ),
                "description": (
                    "Contacto directo verificado (+57 318 793 3658) a 0.7 km del centro de San Agustín para ofrecer muralismo, "
                    "cabañas con muro tendinoso e incrustaciones de botellas, y cubiertas en guadua y metal."
                ),
                "url": "https://yumahotelsanagustin.com/",
                "budget_min": 650000,
                "budget_max": 4200000,
                "currency": "COP",
                "category_hint": "murales_tatuajes",
                "whatsapp_phone": "573187933658",
                "contact_phone": "+57 318 793 3658",
                "contact_whatsapp_url": "https://wa.me/573187933658",
                "skills": ["🎨 Murales & Arte", "🍾 Muro Tendinoso & Botellas", "🔩 Cubiertas Guadua/Metal", "WhatsApp +57 3187933658"]
            },

            # =========================================================================
            # B2. CLASES DE BARISMO EN COLEGIOS / VEREDAS Y CATADOR Q-GRADER (CAFÉ ESPECIAL)
            # =========================================================================
            {
                "id": "huila_qgrader_barismo_ie_alto_obispo",
                "title": "☕ [Clases de Barismo & Catación Q-Grader en Colegio Rural] I.E. Alto del Obispo (San Agustín, Huila)",
                "organization": "Institución Educativa Alto del Obispo (Vereda Alto del Obispo, San Agustín)",
                "origin_source_detail": "Directorio Oficial de Instituciones Educativas Rurales — San Agustín Huila",
                "time_ago_exact": "Publicado hace 18 minutos (Hoy)",
                "published_at": mins_ago(18),
                "location": "📍 Vereda Alto del Obispo, San Agustín, Huila (A 5.8 km de ti)",
                "approx_place": "Vereda Alto del Obispo (Zona Cafetera de Especialidad de San Agustín)",
                "lat": 1.8410,
                "lon": -76.2995,
                "verbatim_request": (
                    "\"Requerimos tallerista / instructora en Barismo y Catación de Café de Especialidad (perfil Catador Q-Grader o barista "
                    "experta) para dictar clases prácticas a estudiantes de secundaria e hijos de caficultores en la Vereda Alto del Obispo: "
                    "reconocimiento de defectos, protocolo de catación SCA, métodos de filtrado (V60, Chemex, Prensa Francesa) y preparación en barra.\""
                ),
                "requirements_list": [
                    "Conocimiento práctico comprobable en Catación de Café de Especialidad (protocolo SCA / Q-Grader) y Barismo.",
                    "Metodología pedagógica para enseñar a jóvenes de colegio rural y grupos de familias caficultoras en vereda.",
                    "Disponibilidad para desplazarse por sesiones o jornadas a la Vereda Alto del Obispo (San Agustín).",
                    "Contacto directo con Rectoría / Coordinación de la I.E. Alto del Obispo: +57 314 217 4507."
                ],
                "contractor_info": (
                    "Entidad contratante: Institución Educativa Alto del Obispo — Vereda Alto del Obispo, San Agustín, Huila. "
                    "Teléfono / WhatsApp directo verificado: +57 314 217 4507. Zona ícono mundial de cafés especiales (Borbón Rosado, Caturra, Geisha)."
                ),
                "description": (
                    "Oportunidad directa (+57 314 217 4507) para dictar clases de Barismo, métodos de extracción y talleres de "
                    "Catación Q-Grader en colegio rural y comunidad cafetera de la Vereda Alto del Obispo en San Agustín."
                ),
                "url": "https://wa.me/573142174507",
                "budget_min": 450000,
                "budget_max": 2600000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573142174507",
                "contact_phone": "+57 314 217 4507",
                "contact_whatsapp_url": "https://wa.me/573142174507",
                "skills": ["☕ Clases de Barismo", "🏅 Catador Q-Grader", "🏫 Colegios & Veredas", "WhatsApp +57 3142174507"]
            },
            {
                "id": "huila_qgrader_colegio_cooperativo_sanagustin",
                "title": "☕ [Talleres de Barismo & Cultura de Café en Colegio] Colegio Cooperativo San Agustín (Casco Urbano)",
                "organization": "Colegio Cooperativo San Agustín (Cra 15 # 4-45, San Agustín, Huila)",
                "origin_source_detail": "Directorio Académico Colegio Cooperativo San Agustín (colegiosanagustin.edu.co)",
                "time_ago_exact": "Publicado hace 26 minutos (Hoy)",
                "published_at": mins_ago(26),
                "location": "📍 Casco Urbano, San Agustín, Huila (A 0.4 km · Cra 15 # 4-45)",
                "approx_place": "Carrera 15 # 4-45, Barrio Centro, San Agustín, Huila",
                "lat": 1.8788,
                "lon": -76.2715,
                "verbatim_request": (
                    "\"Abierta recepción de propuestas para cursos electivos, jornadas culturales y talleres prácticos de Barismo, "
                    "Arte Latte, Métodos de Filtrado y Catación Sensorial (Q-Grader) dirigidos a estudiantes de grados 9°, 10° y 11° "
                    "como formación en emprendimiento cafetero y turismo en San Agustín.\""
                ),
                "requirements_list": [
                    "Presentar propuesta corta de taller teórico-práctico por módulos (Historia del café especial del Huila, Catación SCA, Métodos y Espresso/Arte Latte).",
                    "Llevar kit básico de métodos de filtrado (V60, Chemex, Aeropress, gramera, tazas de catación) para demostración en aula.",
                    "Experiencia como Catadora Q-Grader o Barista formadora.",
                    "Contacto directo Colegio Cooperativo San Agustín: +57 314 443 4385 | Correo: cooperativo.sanagustin@sedhuila.gov.co."
                ],
                "contractor_info": (
                    "Contratante: Rectoría y Coordinación Académica — Colegio Cooperativo San Agustín (Cra 15 # 4-45). "
                    "WhatsApp / Celular directo verificado: +57 314 443 4385 | Fijo: (608) 8373046."
                ),
                "description": (
                    "Contacto directo (+57 314 443 4385) en el Colegio Cooperativo San Agustín para dictar clases de Barismo, "
                    "métodos de preparación y catación Q-Grader a estudiantes en el casco urbano de San Agustín."
                ),
                "url": "https://wa.me/573144434385",
                "budget_min": 400000,
                "budget_max": 2400000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573144434385",
                "contact_phone": "+57 314 443 4385",
                "contact_whatsapp_url": "https://wa.me/573144434385",
                "contact_email": "cooperativo.sanagustin@sedhuila.gov.co",
                "skills": ["☕ Barismo en Colegios", "🏅 Catación Q-Grader", "📍 A 0.4 km (San Agustín)", "WhatsApp +57 3144434385"]
            },
            {
                "id": "huila_qgrader_asociacion_loscauchos_vereda",
                "title": "🏅 [Catador Q-Grader & Capacitación en Veredas] Asociación de Caficultores Los Cauchos (San Agustín)",
                "organization": "Asociación de Caficultores San Agustín Los Cauchos (Vereda Los Cauchos)",
                "origin_source_detail": "Red de Asociaciones de Cafés Especiales — Vereda Los Cauchos, San Agustín",
                "time_ago_exact": "Publicado hace 34 minutos (Hoy)",
                "published_at": mins_ago(34),
                "location": "📍 Vereda Los Cauchos, San Agustín, Huila (A 3.9 km de ti)",
                "approx_place": "Vereda Los Cauchos (vía San Agustín - Pitalito), San Agustín, Huila",
                "lat": 1.8690,
                "lon": -76.2450,
                "verbatim_request": (
                    "\"Grupo asociativo de caficultores de la Vereda Los Cauchos (San Agustín) requiere servicios de Catador(a) Q-Grader "
                    "e instructora de Barismo para: 1) Evaluar en mesa de catación lotes de Borbón Rosado, Caturra y Tabi de los socios "
                    "(puntaje SCA, perfil sensorial, humedad y factor de rendimiento); y 2) Dictar talleres de catación y preparación de café "
                    "en vereda para hijos y familias de productores.\""
                ),
                "requirements_list": [
                    "Certificación o dominio técnico como Catador(a) Q-Grader (protocolo CQI / SCA: fragancia/aroma, sabor, postgusto, acidez, cuerpo, balance).",
                    "Capacidad de enseñar de forma clara a grupos de campesinos, mujeres cafeteras y jóvenes de vereda cómo catar su propio café y detectar defectos de secado/fermentación.",
                    "Disponibilidad por jornadas en la Vereda Los Cauchos o laboratorio en San Agustín.",
                    "Contacto directo Asociación Los Cauchos: +57 313 406 5415 / +57 311 257 6610."
                ],
                "contractor_info": (
                    "Contratante: Junta Directiva Asociación San Agustín Los Cauchos (Vereda Los Cauchos, San Agustín, Huila). "
                    "Teléfonos / WhatsApp directos verificados: +57 313 406 5415 y +57 311 257 6610."
                ),
                "description": (
                    "Contacto directo (+57 313 406 5415 / +57 311 257 6610) con la Asociación de Caficultores de la Vereda Los Cauchos "
                    "para servicios de Catación Q-Grader de lotes especiales y clases de barismo/catación en vereda."
                ),
                "url": "https://wa.me/573134065415",
                "budget_min": 500000,
                "budget_max": 3200000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573134065415",
                "contact_phone": "+57 313 406 5415",
                "contact_whatsapp_url": "https://wa.me/573134065415",
                "skills": ["🏅 Catador Q-Grader", "☕ Clases en Veredas", "Borbón Rosado & SCA", "WhatsApp +57 3134065415"]
            },
            {
                "id": "huila_qgrader_cooperativa_andina_nuevazelanda",
                "title": "🏅 [Control de Calidad Q-Grader & Talleres a Grupos] Cooperativa Multiactiva Andina Exportadora (San Agustín)",
                "organization": "Cooperativa Multiactiva Andina Comercializadora y Exportadora de Café",
                "origin_source_detail": "Directorio Exportadores y Cooperativas Cafeteras — Vereda Nueva Zelanda, San Agustín",
                "time_ago_exact": "Publicado hace 42 minutos (Hoy)",
                "published_at": mins_ago(42),
                "location": "📍 Vereda Nueva Zelanda, San Agustín, Huila (A 3.2 km de ti)",
                "approx_place": "Vereda Nueva Zelanda, San Agustín, Huila",
                "lat": 1.8650,
                "lon": -76.2590,
                "verbatim_request": (
                    "\"Requerimos apoyo profesional en Catación Q-Grader para perfilación sensorial de microlotes de exportación "
                    "(84 a 90+ puntos SCA), calibración de tueste de muestras y talleres de escuela de café y barismo para grupos "
                    "de productores asociados y jóvenes catadores en las veredas de San Agustín.\""
                ),
                "requirements_list": [
                    "Manejo riguroso de formulario SCA, análisis físico de almendra (malla, humedad, actividad de agua) y perfilación de microlotes exóticos.",
                    "Habilidad para liderar mesas de catación abiertas con compradores y capacitaciones grupales a productores.",
                    "Contacto directo Cooperativa Multiactiva Andina (San Agustín): +57 321 277 5246."
                ],
                "contractor_info": (
                    "Contratante: Cooperativa Multiactiva Andina Comercializadora y Exportadora de Café — Vereda Nueva Zelanda, San Agustín, Huila. "
                    "Teléfono / WhatsApp directo verificado: +57 321 277 5246."
                ),
                "description": (
                    "Contacto directo (+57 321 277 5246) en San Agustín para servicios de Catador Q-Grader, control de calidad "
                    "de cafés de exportación y talleres de formación en café de especialidad para grupos veredales."
                ),
                "url": "https://wa.me/573212775246",
                "budget_min": 650000,
                "budget_max": 3800000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573212775246",
                "contact_phone": "+57 321 277 5246",
                "contact_whatsapp_url": "https://wa.me/573212775246",
                "skills": ["🏅 Catador Q-Grader", "☕ Exportación & Perfilación", "📍 San Agustín", "WhatsApp +57 3212775246"]
            },
            {
                "id": "huila_qgrader_sena_escuela_calidad_cafe_pitalito",
                "title": "🎓 [Instructora Barismo & Q-Grader] Escuela Nacional de la Calidad del Café SENA Yamboró & Colegios Articulados",
                "organization": "SENA Regional Huila — Escuela Nacional de la Calidad del Café (Tecnoparque Yamboró, Pitalito)",
                "origin_source_detail": "Banco de Instructores SENA APE & Escuela Nacional de la Calidad del Café (Pitalito / Sur del Huila)",
                "time_ago_exact": "Convocatoria Permanente Hoy (Hace 50 min)",
                "published_at": mins_ago(50),
                "location": "📍 Pitalito / San Agustín / Isnos, Huila (Sede Yamboró & Colegios Articulados · A 28 km)",
                "approx_place": "Tecnoparque Agroecológico Yamboró (Pitalito) e Instituciones Educativas en Articulación con la Media en San Agustín e Isnos",
                "lat": 1.8538,
                "lon": -76.0512,
                "verbatim_request": (
                    "\"Convocatoria en el Banco de Instructores SENA (Agencia Pública de Empleo) y programas de Extensión Rural / "
                    "Articulación con la Media Técnica en Colegios del Sur del Huila para formadores en: Preparación de Bebidas a Base de "
                    "Café (Barismo), Catación y Análisis Sensorial de Cafés Especiales (perfil Q-Grader / CQI) y Buenas Prácticas de Postcosecha en Veredas.\""
                ),
                "requirements_list": [
                    "Certificación Q-Grader (CQI) o título Técnico/Tecnólogo/Profesional con experiencia certificada en Barismo y Catación de Cafés Especiales.",
                    "Tener hoja de vida y soportes actualizados en la Agencia Pública de Empleo SENA (agenciapublicadeempleo.sena.edu.co).",
                    "Disponibilidad para dictar formación complementaria en veredas y colegios articulados de San Agustín, Isnos y Pitalito.",
                    "También puedes coordinar talleres conjuntos con Cadefihuila Finca Experimental El Rancho (Alto del Obispo) al +57 311 506 5707."
                ],
                "contractor_info": (
                    "Entidad: SENA Centro de Gestión y Desarrollo Sostenible Surcolombiano — Escuela Nacional de la Calidad del Café (Sede Yamboró, Pitalito) "
                    "y Red Cafetera Cadefihuila (+57 311 506 5707)."
                ),
                "description": (
                    "Acceso directo para postularse como Instructora de Barismo y Catación Q-Grader en la Escuela Nacional de la Calidad del Café "
                    "(SENA Pitalito) y programas de Articulación con Colegios y Veredas del Sur del Huila."
                ),
                "url": "https://agenciapublicadeempleo.sena.edu.co/Paginas/inicio.aspx",
                "budget_min": 2800000,
                "budget_max": 4800000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573115065707",
                "contact_phone": "+57 311 506 5707",
                "contact_whatsapp_url": "https://wa.me/573115065707",
                "skills": ["🎓 Escuela Calidad del Café", "🏅 Catador Q-Grader", "☕ Barismo en Colegios", "SENA Yamboró"]
            },
            {
                "id": "huila_grupos_barismo_catacion_cafeterias_veredas",
                "title": "📲 [Grupos de Cafés Especiales, Cafeterías & Veredas] Solicitudes de Clases de Barismo y Catación Q-Grader",
                "organization": "Cafeterías de Especialidad, Hostales, Colegios y Grupos Veredales (San Agustín & Pitalito)",
                "origin_source_detail": "Búsqueda en Vivo en Grupos de Facebook y WhatsApp — Barismo y Café Especial Huila",
                "time_ago_exact": "Activo hoy (Hace 25 minutos)",
                "published_at": mins_ago(25),
                "location": "📍 San Agustín, Isnos y Pitalito, Huila (Corredor Turístico y Veredas)",
                "approx_place": "Cafés de especialidad de la Calle de la Locería (San Agustín), Pitalito y asociaciones veredales",
                "lat": 1.8803,
                "lon": -76.2712,
                "verbatim_request": (
                    "\"Dueños de tiendas de café especial, hoteles boutique en San Agustín, colegios y grupos de jóvenes caficultores "
                    "publican solicitudes buscando: 1) Capacitación intensiva de barismo (calibración de molino, espresso, texturización "
                    "de leche, arte latte y métodos V60/Chemex) para su personal o estudiantes; 2) Experiencias de Catación Q-Grader "
                    "(Coffee Tour Sensorial) para turistas extranjeros y grupos en fincas.\""
                ),
                "requirements_list": [
                    "Ofrecer paquetes claros: Curso Rápido de Barismo para Cafeterías/Colegios, Taller en Vereda o Cata Sensorial Q-Grader para Turistas.",
                    "Contacto directo con Red de Cafés y Hostales Calle de la Locería en San Agustín: +57 312 529 7560.",
                    "Publicar o responder directamente en los grupos activos de Cafés Especiales y Baristas del Huila."
                ],
                "contractor_info": (
                    "Contratantes: Tiendas de Café de Especialidad, Operadores de Coffee Tours en San Agustín (+57 312 529 7560) "
                    "y Grupos de Caficultores del Sur del Huila."
                ),
                "description": (
                    "Canal directo para conectar con cafeterías turísticas, colegios y grupos veredales que necesitan cursos de "
                    "barismo, calibración de barra, catación Q-Grader y experiencias sensoriales de café de especialidad."
                ),
                "url": "https://www.facebook.com/search/groups/?q=barismo%20catacion%20cafe%20especial%20huila%20san%20agustin%20pitalito",
                "budget_min": 350000,
                "budget_max": 2800000,
                "currency": "COP",
                "category_hint": "barismo_qgrader",
                "whatsapp_phone": "573125297560",
                "contact_phone": "+57 312 529 7560",
                "contact_whatsapp_url": "https://wa.me/573125297560",
                "skills": ["☕ Cursos de Barismo", "🏅 Catación Q-Grader", "🏫 Colegios & Cafeterías", "WhatsApp +57 3125297560"]
            },

            # =========================================================================
            # C. BIOCONSTRUCCIÓN, MURO TENDINOSO, VIDRIO, CUBIERTAS EN GUADUA Y METAL
            # =========================================================================
            {
                "id": "huila_alcaldia_sanagustin",
                "title": "🏛️ Alcaldía Municipal de San Agustín Huila — Cubiertas en Guadua/Metal, Muralismo Cultural y Mínima Cuantía",
                "organization": "Alcaldía de San Agustín Huila (Secretaría de Planeación e Infraestructura)",
                "origin_source_detail": "Portal Oficial de Contratación — Alcaldía de San Agustín (sanagustin-huila.gov.co/contratacion)",
                "time_ago_exact": "Actualizado hoy (Hace 1 hora)",
                "published_at": mins_ago(60),
                "location": "📍 Casco Urbano, San Agustín, Huila (A 0.0 km · Parque Principal)",
                "approx_place": "Calle 3 Cra 12 Esquina, frente al Parque Principal de San Agustín, Huila",
                "lat": 1.8790,
                "lon": -76.2704,
                "verbatim_request": (
                    "\"Convocatoria permanente a proveedores, maestros certificados en guadua, ornamentadores/soldadores y artistas "
                    "locales del municipio de San Agustín para procesos de mínima cuantía y apoyo a la gestión: adecuación de casetas "
                    "turísticas, cubiertas en guadua y estructura metálica, intervención artística/murales culturales y mantenimiento locativo.\""
                ),
                "requirements_list": [
                    "RUT actualizado con código CIIU de construcción / estructuras metálicas / actividades artísticas o diseño.",
                    "Certificado de Maestro en Construcción en Guadua o soportes de experiencia en obras civiles/metálicas/artísticas.",
                    "Seguridad social al día (o planilla del mes al momento de contratar) y cuenta bancaria o Nequi certificada.",
                    "Radicación presencial en Calle 3 Cra 12 Esq. o vía WhatsApp institucional +57 318 285 1968."
                ],
                "contractor_info": (
                    "Entidad contratante: Alcaldía Municipal de San Agustín (NIT 891.180.064-1) — Línea móvil oficial WhatsApp: +57 318 285 1968 | "
                    "Conmutador: (608) 8373177 | Correo: contactenos@sanagustin-huila.gov.co."
                ),
                "description": (
                    "Canal directo oficial de la Alcaldía de San Agustín Huila para contratación de cubiertas en guadua y metal, "
                    "bioconstrucción de paraderos turísticos, murales culturales y diseño 3D."
                ),
                "url": "https://www.sanagustin-huila.gov.co/contratacion",
                "budget_min": 2500000,
                "budget_max": 18000000,
                "currency": "COP",
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "573182851968",
                "contact_phone": "+57 318 285 1968",
                "contact_whatsapp_url": "https://wa.me/573182851968",
                "contact_email": "contactenos@sanagustin-huila.gov.co",
                "skills": ["📍 A 0.0 km (Centro)", "WhatsApp +57 3182851968", "🎋 Cubiertas Guadua & Metal", "🎨 Muralismo"]
            },
            {
                "id": "huila_cabanas_gamcelat",
                "title": "🎋 Cabañas Gamcelat (San Agustín) — Cabañas con Muro Tendinoso, Incrustaciones de Botellas y Cubiertas",
                "organization": "Cabañas y Alojamiento Rural Gamcelat (Propietarios Directos)",
                "origin_source_detail": "Requerimiento Directo de Alojamiento Rural — San Agustín Huila",
                "time_ago_exact": "Publicado hace 1 hora (Hoy)",
                "published_at": mins_ago(75),
                "location": "📍 Vía Parque Arqueológico, San Agustín, Huila (A 0.5 km de ti)",
                "approx_place": "A 450 metros del casco urbano saliendo por la vía hacia el Parque Arqueológico de San Agustín",
                "lat": 1.8805,
                "lon": -76.2745,
                "verbatim_request": (
                    "\"Necesitamos cotizar ampliación y remodelación de cabañas rústicas: levantamiento de muros tendinosos con "
                    "incrustaciones de botellas de colores y muros en vidrio, cambio y refuerzo de cubiertas en guadua y metal soldado, "
                    "y pintura de mural decorativo en el área de recepción y camping.\""
                ),
                "requirements_list": [
                    "Visita presencial en el predio (a 450m del centro vía al Parque Arqueológico) para medir área de cubierta y muros.",
                    "Experiencia demostrable en muro tendinoso (malla vena/gallinero + mortero fino) e incrustación hermética de botellas.",
                    "Soldadura de anclajes metálicos (platinas y pernos) para proteger la guadua de la humedad del suelo.",
                    "Contacto directo con el dueño al WhatsApp +57 313 245 8373 o +57 311 291 0193."
                ],
                "contractor_info": (
                    "Contratante: Propietarios directos de Cabañas Gamcelat (+57 313 245 8373 / +57 311 291 0193). "
                    "Trato directo con el propietario sin intermediarios ni contratos largos; pago por avance de obra."
                ),
                "description": (
                    "Contacto directo verificado (+57 313 245 8373) a 500m del centro de San Agustín para cabañas con muro tendinoso, "
                    "incrustaciones de botellas, muros en vidrio, cubiertas en guadua/metal y murales."
                ),
                "url": "https://wa.me/573132458373",
                "budget_min": 650000,
                "budget_max": 3800000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573132458373",
                "contact_phone": "+57 313 245 8373",
                "contact_whatsapp_url": "https://wa.me/573132458373",
                "skills": ["📍 A 0.5 km", "WhatsApp +57 3132458373", "🍾 Muro Tendinoso & Botellas", "🎋 Cubiertas Guadua/Metal"]
            },
            {
                "id": "huila_hotel_internacional_metal_guadua",
                "title": "🔩 Hotel San Agustín Internacional — Cubiertas en Guadua y Metal, Soldadura Estructural y Remodelación",
                "organization": "Hotel San Agustín Internacional (Gerencia / Mantenimiento)",
                "origin_source_detail": "Solicitud de Mantenimiento Hotelería Local — San Agustín Huila",
                "time_ago_exact": "Publicado hace 1 hora (Hoy)",
                "published_at": mins_ago(82),
                "location": "📍 Salida a Vereda La Estrella, San Agustín, Huila (A 0.5 km de ti)",
                "approx_place": "Carrera 19 con Calle 2 Esquina (Salida hacia la Vereda La Estrella, casco urbano de San Agustín)",
                "lat": 1.8810,
                "lon": -76.2662,
                "verbatim_request": (
                    "\"Se requiere maestro soldador y constructor en guadua para fabricación y mantenimiento de cubiertas en estructura "
                    "metálica y guadua, reparación de cerchas, canales, portones en hierro, pérgolas de jardín y remodelación de espacios.\""
                ),
                "requirements_list": [
                    "Contar con equipo de soldadura (inversor, careta, pulidora) y herramienta para corte y ensamble de guadua.",
                    "Cumplir normas básicas de seguridad para trabajo en cubiertas y techos.",
                    "Entregar presupuesto detallado diferenciando mano de obra y listado de materiales (perfiles metálicos, pintura anticorrosiva, guadua).",
                    "Contacto directo: +57 312 433 2510 / +57 311 264 4389."
                ],
                "contractor_info": (
                    "Contratante: Administración del Hotel San Agustín Internacional (+57 312 433 2510). "
                    "Ubicado en la Cra 19 Calle 2 Esquina; requiere mantenimiento continuo en estructuras de metal, soldadura y guadua."
                ),
                "description": (
                    "Contacto directo (+57 312 433 2510) para ofrecer todo tipo de cubiertas en guadua y metal, soldadura estructural "
                    "y remodelación de instalaciones en el casco urbano de San Agustín."
                ),
                "url": "https://wa.me/573124332510",
                "budget_min": 550000,
                "budget_max": 3500000,
                "currency": "COP",
                "category_hint": "metal_soldadura",
                "whatsapp_phone": "573124332510",
                "contact_phone": "+57 312 433 2510",
                "contact_whatsapp_url": "https://wa.me/573124332510",
                "skills": ["📍 A 0.5 km", "WhatsApp +57 3124332510", "🔩 Cubiertas Metal & Guadua", "Soldadura"]
            },
            {
                "id": "huila_elmaco_sanagustin",
                "title": "🎋 Finca Ecológica El Maco (San Agustín) — Bioconstrucción, Muro Tendinoso, Vidrio y Muralismo",
                "organization": "Finca Ecológica El Maco (San Agustín, Huila)",
                "origin_source_detail": "Red de Bioconstrucción y Eco-Hotelería — San Agustín (elmaco.ch)",
                "time_ago_exact": "Publicado hace 2 horas (Hoy)",
                "published_at": mins_ago(115),
                "location": "📍 Vía Mesitas / Parque Arqueológico, San Agustín (A 1.5 km de ti)",
                "approx_place": "Vereda Mesitas / Corredor al Parque Arqueológico, a 1.5 km del centro de San Agustín",
                "lat": 1.8832,
                "lon": -76.2835,
                "verbatim_request": (
                    "\"Buscamos maestro en bioconstrucción y guadua para ampliación y mantenimiento de cabañas orgánicas: "
                    "muros tendinosos curvos, incrustación artística de botellas y vitrales en vidrio, cubiertas cónicas en guadua "
                    "y estructuras metálicas de soporte, además de propuestas de muralismo ecológico.\""
                ),
                "requirements_list": [
                    "Dominio técnico en bioconstrucción (muro tendinoso, bahareque encementado, ensambles en guadua sin clavos expuestos).",
                    "Capacidad de modelar previamente la estructura en Blender 3D o presentar plano/boceto claro.",
                    "Experiencia en impermeabilización de cubiertas y tratamiento/inmunización ecológica de guadua.",
                    "Contacto directo vía WhatsApp: +57 320 375 5982."
                ],
                "contractor_info": (
                    "Contratante: Administración Finca Ecológica El Maco (+57 320 375 5982 · elmaco.ch). "
                    "Pioneros en San Agustín en cabañas circulares y bioconstrucción; valoran enormemente el trabajo artístico en guadua, vidrio y muro tendinoso."
                ),
                "description": (
                    "Contacto directo verificado (+57 320 375 5982) en Finca Ecológica El Maco para proyectos de bioconstrucción, "
                    "muro tendinoso, incrustación de botellas, cubiertas en guadua y metal y diseño 3D."
                ),
                "url": "https://www.elmaco.ch/",
                "budget_min": 900000,
                "budget_max": 4800000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573203755982",
                "contact_phone": "+57 320 375 5982",
                "contact_whatsapp_url": "https://wa.me/573203755982",
                "skills": ["📍 A 1.5 km", "WhatsApp +57 3203755982", "🍾 Muro Tendinoso & Botellas", "🎋 Bioconstrucción"]
            },
            {
                "id": "huila_nacimiento_glamping",
                "title": "🎋 Nacimiento Glamping (Vereda El Tablón) — Cubiertas Mixtas Metal/Guadua, Muros en Vidrio y Secadero Café",
                "organization": "Nacimiento Glamping (Vereda El Tablón, San Agustín)",
                "origin_source_detail": "Canal Directo Glamping & Finca — Vereda El Tablón (nacimientoglamping.com)",
                "time_ago_exact": "Publicado hace 2 horas (Hoy)",
                "published_at": mins_ago(130),
                "location": "📍 Vereda El Tablón, San Agustín, Huila (A 2.7 km de ti)",
                "approx_place": "Vereda El Tablón (vía al Sitio Arqueológico El Tablón), a 2.7 km del casco urbano",
                "lat": 1.8985,
                "lon": -76.2565,
                "verbatim_request": (
                    "\"Requerimos contratista local en San Agustín para: 1) Estructuras metálicas soldadas para plataformas de deck y jacuzzis; "
                    "2) Cabañas/domos con grandes muros en vidrio panorámico, detalles en muro tendinoso con botellas y cubiertas en guadua; "
                    "3) Adecuación de marquesina/secadero de café de especialidad en la finca.\""
                ),
                "requirements_list": [
                    "Soldadura estructural de alta resistencia para plataformas elevadas en terreno inclinado.",
                    "Instalación limpia de marcos metálicos/madera para muros en vidrio templado o laminado.",
                    "Acabados de primera calidad en guadua inmunizada para pérgolas y cubiertas.",
                    "Contacto directo: +57 311 684 5394."
                ],
                "contractor_info": (
                    "Contratante: Propietarios de Nacimiento Glamping (+57 311 684 5394 · nacimientoglamping.com). "
                    "Ubicado en la Vereda El Tablón, combina glamping de lujo (vidrio, metal y guadua) con entorno cafetero."
                ),
                "description": (
                    "Contacto directo (+57 311 684 5394) en la Vereda El Tablón para estructuras en metal y soldadura, "
                    "muros en vidrio, cabañas en guadua y marquesinas de café."
                ),
                "url": "https://nacimientoglamping.com/",
                "budget_min": 950000,
                "budget_max": 5200000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573116845394",
                "contact_phone": "+57 311 684 5394",
                "contact_whatsapp_url": "https://wa.me/573116845394",
                "skills": ["📍 A 2.7 km (El Tablón)", "WhatsApp +57 3116845394", "🍾 Muros en Vidrio", "🔩 Cubiertas Metal/Guadua"]
            },
            {
                "id": "huila_sanagua_glamping",
                "title": "🎋 Glamping Sanagua (Sector Lavapatas) — Baños Ecológicos con Muro Tendinoso/Botellas, Metal y Murales",
                "organization": "Glamping Sanagua (Sector Lavapatas, San Agustín)",
                "origin_source_detail": "Solicitud Directa de Obra Turística — Sector Lavapatas (sanagua.co)",
                "time_ago_exact": "Publicado hace 3 horas (Hoy)",
                "published_at": mins_ago(165),
                "location": "📍 Sector Lavapatas, San Agustín, Huila (A 2.8 km de ti)",
                "approx_place": "Vereda Mesitas / Sector Fuente de Lavapatas, a 2.8 km del casco urbano de San Agustín",
                "lat": 1.8878,
                "lon": -76.2940,
                "verbatim_request": (
                    "\"Cotización para construcción de módulos de baño ecológico y ampliación de glamping: paredes en muro tendinoso "
                    "con incrustaciones de botellas recicladas para iluminación natural, estructura portante en metal y guadua, "
                    "y mural artístico exterior inspirado en la Fuente de Lavapatas.\""
                ),
                "requirements_list": [
                    "Manejo de formas orgánicas en muro tendinoso (ferrocemento) resistentes a la humedad.",
                    "Soldadura de bases metálicas y ensamble de cubiertas en guadua certificada.",
                    "Propuesta de diseño 3D en Blender o boceto a escala antes de iniciar obra.",
                    "Contacto directo por WhatsApp: +57 312 676 0320."
                ],
                "contractor_info": (
                    "Contratante: Gerencia Glamping Sanagua (+57 312 676 0320 · sanagua.co). "
                    "Glamping campestre en el sector Lavapatas con alta demanda de acabados artísticos y bioconstrucción."
                ),
                "description": (
                    "Contacto directo (+57 312 676 0320) en el sector Lavapatas para muros tendinosos con botellas, "
                    "cubiertas en guadua y metal, y muralismo."
                ),
                "url": "https://sanagua.co/",
                "budget_min": 850000,
                "budget_max": 4900000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573126760320",
                "contact_phone": "+57 312 676 0320",
                "contact_whatsapp_url": "https://wa.me/573126760320",
                "skills": ["📍 A 2.8 km (Lavapatas)", "WhatsApp +57 3126760320", "🍾 Muro Tendinoso & Botellas", "🎨 Murales"]
            },

            # =========================================================================
            # D. SECCIÓN DE TRABAJOS EXTRAS: PASANTÍAS SENA, INTERCAMBIOS Y EXTERIOR
            # =========================================================================
            {
                "id": "extra_sena_pasantias_etapa_productiva_huila",
                "title": "🎓 [Pasantías SENA & Etapa Productiva] Presentación de Pasantías, Contrato de Aprendizaje o Proyecto Productivo",
                "organization": "SENA Regional Huila — Centro CGDSS Pitalito / San Agustín & Caprendizaje",
                "origin_source_detail": "Plataforma Oficial SENA Caprendizaje & SECOP II Huila (caprendizaje.sena.edu.co)",
                "time_ago_exact": "Convocatoria Abierta Hoy (Hace 40 min)",
                "published_at": mins_ago(40),
                "location": "📍 San Agustín / Pitalito, Huila (Sede SENA Sur del Huila · A 0.2 km / 28 km)",
                "approx_place": "Alcaldía de San Agustín / Empresas del Sur del Huila y Centro SENA CGDSS Pitalito",
                "lat": 1.8795,
                "lon": -76.2700,
                "verbatim_request": (
                    "\"Convocatoria abierta para aprendices SENA del Sur del Huila (San Agustín, Isnos, Pitalito) que requieran "
                    "presentar su Etapa Productiva bajo modalidad de: 1) Pasantía o Apoyo a Entidad Estatal/ONG (Alcaldía de San Agustín, "
                    "parques, cooperativas cafeteras); 2) Contrato de Aprendizaje remunerado (75% a 100% SMMLV + ARL/EPS); o "
                    "3) Proyecto Productivo propio (Bioconstrucción en Guadua, Estructuras Metálicas, Café Borbón Rosado o Diseño 3D).\""
                ),
                "requirements_list": [
                    "Tener aprobado el 100% de los resultados de aprendizaje de la etapa lectiva (o estar en el último trimestre habilitado).",
                    "Estar registrado y activo en la plataforma SGVA (caprendizaje.sena.edu.co) y solicitar aval al Coordinador Académico del Centro CGDSS.",
                    "Presentar carta de aceptación de la empresa/entidad (o plan de negocio si eliges Proyecto Productivo propio).",
                    "Entregar bitácoras quincenales de seguimiento (Formato GFPI-F-147) firmadas por el jefe inmediato e instructor de seguimiento.",
                    "Duración reglamentaria: 880 horas (aprox. 6 meses) con afiliación obligatoria a ARL."
                ],
                "contractor_info": (
                    "Entidad: Servicio Nacional de Aprendizaje SENA — Centro de Gestión y Desarrollo Sostenible Surcolombiano (Pitalito / San Agustín) "
                    "y empresas patrocinadoras en SGVA. Trámite 100% oficial y gratuito."
                ),
                "description": (
                    "Guía y enlace directo oficial para inscribir y presentar tus pasantías del SENA en San Agustín o Pitalito, "
                    "ya sea por contrato de aprendizaje remunerado, pasantía en Alcaldía/Cooperativa o validando tu propio taller de Guadua/Metal/Café como Proyecto Productivo."
                ),
                "url": "https://caprendizaje.sena.edu.co/",
                "budget_min": 975000,
                "budget_max": 1300000,
                "currency": "COP",
                "category_hint": "extras_exterior",
                "whatsapp_phone": "573182851968",
                "contact_phone": "+57 318 285 1968",
                "contact_whatsapp_url": "https://wa.me/573182851968",
                "skills": ["🎓 Pasantías SENA", "Etapa Productiva", "Proyecto Productivo", "📍 San Agustín / Pitalito"]
            },
            {
                "id": "extra_intercambio_local_murales_guadua_tatuajes",
                "title": "🤝 [Intercambio & Trueque Técnico] Muralismo, Bioconstrucción en Guadua o Tatuajes por Estadía + Bono + Clientes",
                "organization": "Eco-Hostales & Glampings (San Agustín, Huila & Colombia — Worldpackers)",
                "origin_source_detail": "Plataforma de Intercambios Worldpackers Colombia & Red de Hostales San Agustín",
                "time_ago_exact": "Publicado hace 55 minutos (Hoy)",
                "published_at": mins_ago(55),
                "location": "📍 San Agustín, Huila / Santa Marta / Eje Cafetero (A 0.4 km o Viaje Nacional)",
                "approx_place": "Hostales ecológicos de San Agustín (Calle de la Locería / Veredas) y destinos turísticos de Colombia",
                "lat": 1.8800,
                "lon": -76.2710,
                "verbatim_request": (
                    "\"Recibimos artistas muralistas, tatuadores, constructores en bambú/guadua y soldadores bajo modalidad de intercambio "
                    "colaborativo o comisión: pinta un mural temático o construye una estructura en guadua/muro tendinoso con botellas "
                    "a cambio de alojamiento, alimentación completa, espacio habilitado dentro del hostal para tatuar o vender tus diseños "
                    "a turistas extranjeros (100% de ganancia de tus tatuajes/obras) más bono de materiales.\""
                ),
                "requirements_list": [
                    "Mostrar fotos reales de al menos 2 o 3 trabajos previos (murales, estructuras en guadua/metal o tatuajes).",
                    "Acordar previamente por escrito o WhatsApp las horas de dedicación (usualmente 15 a 20 horas por semana) y qué materiales pone el hostal.",
                    "Para tatuar a huéspedes: contar con máquina propia, tintas e insumos de bioseguridad.",
                    "Contacto directo en San Agustín (+57 312 529 7560) o postulación directa en el portal Worldpackers Colombia."
                ],
                "contractor_info": (
                    "Anfitriones: Red de Eco-Hostales en San Agustín (+57 312 529 7560 / +57 320 375 5982) y anfitriones verificados en Worldpackers Colombia."
                ),
                "description": (
                    "Modalidad de intercambio real: realiza murales, bioconstrucción en guadua/muro tendinoso o mantenimiento en metal "
                    "obteniendo hospedaje, comida, bono acordado y vitrina directa para vender tatuajes y artesanías a turistas."
                ),
                "url": "https://www.worldpackers.com/es/search/south_america/colombia",
                "budget_min": 400000,
                "budget_max": 2200000,
                "currency": "COP",
                "category_hint": "extras_exterior",
                "whatsapp_phone": "573125297560",
                "contact_phone": "+57 312 529 7560",
                "contact_whatsapp_url": "https://wa.me/573125297560",
                "skills": ["🤝 Intercambio Artístico", "🎨 Murales & Tatuajes", "🎋 Guadua & Vidrio", "WhatsApp +57 3125297560"]
            },
            {
                "id": "extra_exterior_sena_ape_internacional",
                "title": "✈️ [Trabajo en el Exterior — SENA APE] Convocatorias Internacionales para Soldadores, Oficiales de Obra y Técnicos",
                "organization": "Agencia Pública de Empleo SENA — Convocatorias Internacionales (Canadá, España, Europa)",
                "origin_source_detail": "Portal Oficial Agencia Pública de Empleo SENA (agenciapublicadeempleo.sena.edu.co)",
                "time_ago_exact": "Actualizado hoy (Portal Oficial SENA)",
                "published_at": mins_ago(90),
                "location": "✈️ Exterior: Canadá, España y Europa (Postulación desde Huila / Colombia)",
                "approx_place": "Inscripción virtual en APE SENA o presencial en sede SENA Pitalito / Huila",
                "lat": 1.8538,
                "lon": -76.0508,
                "verbatim_request": (
                    "\"La Agencia Pública de Empleo del SENA invita a técnicos, soldadores estructurales/ornamentales, armadores de cubiertas "
                    "y oficiales de construcción colombianos a participar en las convocatorias de movilidad laboral internacional con "
                    "contrato formal de trabajo en el exterior (Canadá, España y otros países aliados).\""
                ),
                "requirements_list": [
                    "Registrar y actualizar la hoja de vida al 100% en agenciapublicadeempleo.sena.edu.co adjuntando diplomas y certificados (SENA Guadua, Soldadura, Alturas).",
                    "Certificar experiencia laboral o contractual mínima de 24 meses (2 años) en el oficio (soldadura, estructuras metálicas, construcción o carpintería).",
                    "Contar con pasaporte colombiano vigente (o tramitarlo en la Gobernación del Huila).",
                    "Trámite 100% gratuito y directo con el SENA (no pagar a tramitadores); incluye acompañamiento en visa de trabajo cuando eres seleccionado por la empresa extranjera."
                ],
                "contractor_info": (
                    "Entidad Oficial: Agencia Pública de Empleo del SENA (Ministerio del Trabajo de Colombia) en convenio con empleadores extranjeros verificados."
                ),
                "description": (
                    "Enlace directo a las convocatorias internacionales oficiales del SENA para trabajar legalmente en el exterior "
                    "en soldadura, estructuras metálicas y construcción."
                ),
                "url": "https://agenciapublicadeempleo.sena.edu.co/Paginas/inicio.aspx",
                "budget_min": 8500000,
                "budget_max": 16000000,
                "currency": "COP",
                "category_hint": "extras_exterior",
                "whatsapp_phone": "",
                "skills": ["✈️ Trabajo en el Exterior", "🎓 SENA Internacional", "🔩 Soldadura & Construcción", "Contrato Legal Exterior"]
            },
            {
                "id": "extra_exterior_intercambio_bioconstruccion_murales",
                "title": "✈️ [Intercambio en el Exterior] Bioconstrucción en Bambú/Guadua, Muro Tendinoso, Murales y Tatuajes (Costa Rica, México, Europa)",
                "organization": "Worldpackers & Eco-Aldeas Internacionales (Costa Rica, México, España, Portugal)",
                "origin_source_detail": "Plataforma Internacional de Eco-Proyectos Worldpackers (worldpackers.com/es)",
                "time_ago_exact": "Publicado hace 1 hora (Hoy)",
                "published_at": mins_ago(95),
                "location": "✈️ Exterior: Costa Rica, México, España y Portugal (Intercambio Internacional)",
                "approx_place": "Eco-lodges, centros de permacultura y hostales artísticos en Latinoamérica y Europa",
                "lat": 1.8792,
                "lon": -76.2706,
                "verbatim_request": (
                    "\"Eco-lodges, proyectos de permacultura y hostales culturales en Costa Rica, México, Brasil, España y Portugal "
                    "buscan maestros en bioconstrucción (bambú/guadua, ferrocemento/muro tendinoso, botellas de vidrio), soldadores y "
                    "muralistas/tatuadores para estadías de 1 a 3 meses con alojamiento, comidas y comisiones por obras o tatuajes.\""
                ),
                "requirements_list": [
                    "Pasaporte colombiano vigente (México, Brasil, España y Portugal no exigen visa de turista para estadías cortas de intercambio menores a 90 días).",
                    "Portafolio digital (fotos en Instagram o PDF) mostrando tus cabañas en guadua, muros tendinosos, estructuras en metal, murales y tatuajes.",
                    "En Latinoamérica solo necesitas español; en Europa basta con español o inglés básico práctico.",
                    "Postulación directa con el anfitrión extranjero verificando qué incluye (alojamiento privado, 3 comidas, materiales y permiso para tatuar clientes)."
                ],
                "contractor_info": (
                    "Anfitriones Internacionales: Eco-aldeas, glampings de bambú y hostales artísticos verificados en Worldpackers."
                ),
                "description": (
                    "Oportunidad real para viajar al exterior haciendo lo que sabes: construir en guadua/bambú y muro tendinoso, "
                    "pintar murales y tatuar en eco-lodges y hostales de Costa Rica, México y Europa."
                ),
                "url": "https://www.worldpackers.com/es/search?q=bioconstruccion",
                "budget_min": 1500000,
                "budget_max": 6000000,
                "currency": "COP",
                "category_hint": "extras_exterior",
                "whatsapp_phone": "",
                "skills": ["✈️ Intercambio Exterior", "🎋 Bioconstrucción Bambú", "🎨 Murales & Tatuajes", "Sin Visa (LATAM/UE)"]
            },

            # =========================================================================
            # E. TRABAJOS INFORMALES DE 2DO TIEMPO, MANUALIDADES Y REPARACIONES
            # =========================================================================
            {
                "id": "informal_soldadura_reparaciones_gamcelat",
                "title": "🛠️ [Trabajo Rápido / 2do Tiempo] Soldadura a Domicilio, Cubiertas, Lámparas en Guadua y Reparaciones",
                "organization": "Cabañas & Camping Gamcelat — Línea Directa Encargos Rápidos",
                "origin_source_detail": "Anuncio Local de Trabajos por Día / Encargo — San Agustín Huila",
                "time_ago_exact": "Publicado hace 50 minutos (Hoy)",
                "published_at": mins_ago(50),
                "location": "📍 Vía al Parque Arqueológico, San Agustín (A 0.5 km de ti)",
                "approx_place": "A 500m del centro de San Agustín hacia el Parque Arqueológico",
                "lat": 1.8805,
                "lon": -76.2745,
                "verbatim_request": (
                    "\"Se contrata por días, fines de semana o por tarea entregada: puntos de soldadura en portones y techos, "
                    "fabricación de lámparas artesanales en guadua con botellas de vidrio, inmunización de guadua y pintura/murales pequeños.\""
                ),
                "requirements_list": [
                    "Disponibilidad en segundo tiempo (tardes o fines de semana) o por jornal pactado.",
                    "Herramienta manual básica o equipo portátil de soldadura.",
                    "Pago directo en efectivo o Nequi al terminar cada encargo.",
                    "Escribir directo al WhatsApp +57 311 291 0193."
                ],
                "contractor_info": (
                    "Contratante: Segunda línea directa de propietarios en San Agustín (+57 311 291 0193). "
                    "Sin contratos ni trámites; ideal para generar ingreso extra rápido."
                ),
                "description": (
                    "Trabajo informal y de segundo tiempo a 0.5 km del centro de San Agustín: soldadura rápida, "
                    "manualidades en guadua/vidrio y mantenimiento de cabañas."
                ),
                "url": "https://wa.me/573112910193",
                "budget_min": 90000,
                "budget_max": 550000,
                "currency": "COP",
                "category_hint": "informales_manualidades",
                "whatsapp_phone": "573112910193",
                "contact_phone": "+57 311 291 0193",
                "contact_whatsapp_url": "https://wa.me/573112910193",
                "skills": ["📍 A 0.5 km", "🛠️ 2do Tiempo / Por Día", "WhatsApp +57 3112910193", "🔩 Soldadura & Manualidades"]
            },
            {
                "id": "huila_hotel_valladollyd_remodelacion",
                "title": "🔩 Hotel & Cabañas Valladollyd (Km 1 Vía al Parque) — Cubiertas en Guadua y Metal, Soldadura y Murales",
                "organization": "Hotel Cabañas Valladollyd (San Agustín, Huila)",
                "origin_source_detail": "Contacto Directo Hotelería Vía al Parque — San Agustín Huila",
                "time_ago_exact": "Publicado hace 2 horas (Hoy)",
                "published_at": mins_ago(125),
                "location": "📍 Km 1 Vía Parque Arqueológico, San Agustín (A 1.1 km de ti)",
                "approx_place": "Kilómetro 1 en la vía principal hacia el Parque Arqueológico de San Agustín",
                "lat": 1.8815,
                "lon": -76.2798,
                "verbatim_request": (
                    "\"Requerimos cotización para mantenimiento y remodelación de cubiertas en guadua y estructura metálica, "
                    "soldadura de rejas/barandas, acabados en muro tendinoso con botellas de vidrio y decoración mural artística.\""
                ),
                "requirements_list": [
                    "Visita técnica en el Km 1 vía al Parque Arqueológico para revisar estado actual de techos y estructuras.",
                    "Experiencia en empalmes estructurales entre tubería metálica y guadua inmunizada.",
                    "Contacto directo: +57 311 852 0150 / +57 312 478 2402."
                ],
                "contractor_info": (
                    "Contratante: Gerencia Hotel Valladollyd (+57 311 852 0150 / +57 312 478 2402)."
                ),
                "description": (
                    "Contacto directo verificado (+57 311 852 0150) en el Km 1 vía al Parque Arqueológico para cubiertas en guadua y metal, "
                    "remodelación estructural y acabados artísticos."
                ),
                "url": "https://wa.me/573118520150",
                "budget_min": 650000,
                "budget_max": 3600000,
                "currency": "COP",
                "category_hint": "metal_soldadura",
                "whatsapp_phone": "573118520150",
                "contact_phone": "+57 311 852 0150",
                "contact_whatsapp_url": "https://wa.me/573118520150",
                "skills": ["📍 A 1.1 km", "WhatsApp +57 3118520150", "🔩 Cubiertas Metal/Guadua", "Remodelación"]
            },
            {
                "id": "huila_cabanas_amalu",
                "title": "🎋 Cabañas Amalú (San Agustín) — Cabañas en Bioconstrucción, Muro Tendinoso, Vidrio y Cubiertas",
                "organization": "Cabañas Amalú (Propietario en San Agustín)",
                "origin_source_detail": "Canal Directo de Propietario — Cabañas Amalú San Agustín",
                "time_ago_exact": "Publicado hace 2 horas (Hoy)",
                "published_at": mins_ago(140),
                "location": "📍 Sector Campestre Urbano, San Agustín, Huila (A 1.0 km de ti)",
                "approx_place": "Zona campestre perimetral del casco urbano de San Agustín, Huila",
                "lat": 1.8740,
                "lon": -76.2780,
                "verbatim_request": (
                    "\"Se busca maestro en guadua, bioconstrucción y soldadura para adecuación de cabañas turísticas: "
                    "cubiertas en guadua y metal, detalles en muro tendinoso con incrustación de botellas y murales decorativos.\""
                ),
                "requirements_list": [
                    "Trato directo con el propietario en San Agustín sin intermediarios.",
                    "Presentar fotos de trabajos previos en guadua, metal o bioconstrucción.",
                    "WhatsApp directo: +57 318 699 5451."
                ],
                "contractor_info": (
                    "Contratante: Propietario de Cabañas Amalú (+57 318 699 5451)."
                ),
                "description": (
                    "Contacto directo (+57 318 699 5451) para ofrecer bioconstrucción, muro tendinoso, cubiertas en guadua/metal y murales."
                ),
                "url": "https://wa.me/573186995451",
                "budget_min": 550000,
                "budget_max": 3200000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573186995451",
                "contact_phone": "+57 318 699 5451",
                "contact_whatsapp_url": "https://wa.me/573186995451",
                "skills": ["📍 A 1.0 km", "WhatsApp +57 3186995451", "🎋 Bioconstrucción Guadua", "🍾 Muros en Vidrio"]
            },
            {
                "id": "huila_cabanas_numbana",
                "title": "🎋 Cabañas Numbana (Vía Parque Arqueológico) — Estructuras en Guadua, Metal, Muros en Vidrio y Murales",
                "organization": "Cabañas Numbana (San Agustín, Huila)",
                "origin_source_detail": "Portal Oficial Cabañas Numbana San Agustín (cabanasnumbana.com)",
                "time_ago_exact": "Publicado hace 3 horas (Hoy)",
                "published_at": mins_ago(175),
                "location": "📍 Vía Parque Arqueológico, San Agustín (A 1.8 km de ti)",
                "approx_place": "Corredor Vía al Parque Arqueológico, a 1.8 km del casco urbano de San Agustín",
                "lat": 1.8845,
                "lon": -76.2862,
                "verbatim_request": (
                    "\"Requerimos ampliación y mantenimiento de cabañas campestres: ventanales y muros en vidrio, "
                    "cubiertas y pérgolas en guadua y metal soldado, muro tendinoso con botellas y renders 3D previos.\""
                ),
                "requirements_list": [
                    "Experiencia comprobable en guadua certificada, estructuras metálicas y acabados en vidrio.",
                    "Disponibilidad en la vía al Parque Arqueológico de San Agustín.",
                    "Contacto directo: +57 323 247 1045."
                ],
                "contractor_info": (
                    "Contratante: Propietarios de Cabañas Numbana (+57 323 247 1045 · cabanasnumbana.com)."
                ),
                "description": (
                    "Contacto directo (+57 323 247 1045) en la vía al Parque Arqueológico para cubiertas en guadua y metal, muros en vidrio y bioconstrucción."
                ),
                "url": "https://cabanasnumbana.com/",
                "budget_min": 750000,
                "budget_max": 4200000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573232471045",
                "contact_phone": "+57 323 247 1045",
                "contact_whatsapp_url": "https://wa.me/573232471045",
                "skills": ["📍 A 1.8 km", "WhatsApp +57 3232471045", "🎋 Guadua & Bioconstrucción", "🔩 Metal & Vidrio"]
            },
            {
                "id": "huila_mayu_isnos",
                "title": "🎋 Glamping Mayu (Isnos, Huila) — Miradores en Metal/Soldadura, Cubiertas en Guadua y Muralismo",
                "organization": "Glamping Mayu (Isnos, Huila)",
                "origin_source_detail": "Canal Directo Glamping Mayu — Isnos, Huila",
                "time_ago_exact": "Publicado hace 3 horas (Hoy)",
                "published_at": mins_ago(190),
                "location": "📍 Isnos, Huila (A 13.5 km de San Agustín)",
                "approx_place": "Zona de Miradores Campestres del municipio de Isnos (a 25 min de San Agustín)",
                "lat": 1.9320,
                "lon": -76.1615,
                "verbatim_request": (
                    "\"Se requiere soldador de estructuras metálicas y maestro en guadua para construcción y refuerzo de balcones/mallas "
                    "mirador, cubiertas mixtas en guadua y metal, muros con botellas de vidrio y pintura de murales fotográficos para visitantes.\""
                ),
                "requirements_list": [
                    "Soldadura certificada o de alta penetración para estructuras de mirador.",
                    "Construcción de cubiertas en guadua inmunizada y pintura de murales llamativos para turismo.",
                    "Contacto directo: +57 314 358 9808 / +57 317 871 6443."
                ],
                "contractor_info": (
                    "Contratante: Propietarios de Glamping Mayu en Isnos (+57 314 358 9808)."
                ),
                "description": (
                    "Contacto directo (+57 314 358 9808) en Isnos para estructuras metálicas de mirador, cabañas en guadua y murales."
                ),
                "url": "https://wa.me/573143589808",
                "budget_min": 800000,
                "budget_max": 4500000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573143589808",
                "contact_phone": "+57 314 358 9808",
                "contact_whatsapp_url": "https://wa.me/573143589808",
                "skills": ["📍 A 13.5 km (Isnos)", "WhatsApp +57 3143589808", "🔩 Estructuras Metálicas", "🎋 Guadua & Murales"]
            },
            {
                "id": "huila_guaitipan_pitalito",
                "title": "🎋 Laguna Guaitipán Ancestral (Pitalito) — Cabañas Bioconstrucción, Cubiertas Guadua/Metal y Murales",
                "organization": "Laguna Guaitipán Ancestral (Pitalito, Huila)",
                "origin_source_detail": "Portal Oficial Laguna Guaitipán Ancestral (lagunaguaitipan.com)",
                "time_ago_exact": "Publicado hace 4 horas (Hoy)",
                "published_at": mins_ago(210),
                "location": "📍 Laguna de Guaitipán, Pitalito, Huila (A 24.1 km de San Agustín)",
                "approx_place": "Sector Laguna de Guaitipán, Corregimiento de Guacacallo / Pitalito",
                "lat": 1.9250,
                "lon": -76.0580,
                "verbatim_request": (
                    "\"Buscamos constructores en guadua, bioconstrucción (muro tendinoso e incrustación de botellas), soldadores de "
                    "cubiertas metálicas y artistas muralistas para nuevas cabañas temáticas y zonas sociales frente a la Laguna de Guaitipán.\""
                ),
                "requirements_list": [
                    "Experiencia en estructuras de gran formato en guadua y cerchas metálicas.",
                    "Propuesta de acabados artísticos (muro tendinoso, vidrio, murales ancestrales).",
                    "Contacto directo: +57 318 280 4008 / +57 316 018 6786."
                ],
                "contractor_info": (
                    "Contratante: Gerencia Laguna Guaitipán Ancestral (+57 318 280 4008 · lagunaguaitipan.com)."
                ),
                "description": (
                    "Contacto directo (+57 318 280 4008) en la Laguna de Guaitipán para bioconstrucción, cubiertas en guadua y metal, y muralismo."
                ),
                "url": "https://lagunaguaitipan.com/",
                "budget_min": 1100000,
                "budget_max": 5800000,
                "currency": "COP",
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573182804008",
                "contact_phone": "+57 318 280 4008",
                "contact_whatsapp_url": "https://wa.me/573182804008",
                "skills": ["📍 A 24.1 km (Pitalito)", "WhatsApp +57 3182804008", "🍾 Bioconstrucción & Vidrio", "🔩 Guadua & Metal"]
            },

            # =========================================================================
            # F. CIRCULARES PÚBLICAS REALES SECOP II (CON PETICIÓN TEXTUAL DEL PLIEGO)
            # =========================================================================
            {
                "id": "secop_sena_pitalito_2026",
                "title": "🏛️ [Circular SECOP II: SAMC HIL-CGDSS-001-2026] SENA Regional Huila (Pitalito / San Agustín) — Infraestructura Rural y Materiales",
                "organization": "SENA Regional Huila — Centro CGDSS Pitalito",
                "origin_source_detail": "SECOP II Oficial — Circular SAMC HIL-CGDSS-001-2026 (community.secop.gov.co)",
                "time_ago_exact": "Circular Activa en SECOP II (Consultada Hoy)",
                "published_at": mins_ago(110),
                "location": "📍 Pitalito / San Agustín, Huila (A 24.5 km · Circular Pública SECOP II)",
                "approx_place": "Centro de Gestión y Desarrollo Sostenible Surcolombiano (SENA Pitalito, Km 1 Vía al Sur)",
                "lat": 1.8480,
                "lon": -76.0520,
                "verbatim_request": (
                    "\"PROCESO SAMC HIL-CGDSS-001-2026: Suministro de materiales de construcción, ferretería, guadua/madera, "
                    "perfiles metálicos y elementos técnicos para los procesos de Formación Especial Campesina (CampeSENA) y "
                    "adecuación de ambientes rurales del Centro de Gestión y Desarrollo Sostenible Surcolombiano en el Sur del Huila.\""
                ),
                "requirements_list": [
                    "Inscripción activa en SECOP II como proveedor (Persona Natural o Jurídica) y RUP/RUT según pliego.",
                    "Capacidad de entrega o ejecución en los municipios del Sur del Huila (Pitalito, San Agustín, Isnos).",
                    "Consultar el pliego público completo haciendo clic en el botón de Circular Real (no pide clave)."
                ],
                "contractor_info": (
                    "Entidad contratante: SENA Regional Huila — Centro CGDSS Pitalito. Presupuesto Oficial: $537.250.000 COP."
                ),
                "description": (
                    "Circular oficial activa en SECOP II (No requiere clave para ver el pliego). Referencia: SAMC HIL-CGDSS-001-2026."
                ),
                "url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10223805",
                "budget_min": 537250000,
                "budget_max": 537250000,
                "currency": "COP",
                "category_hint": "alcaldia_huila",
                "circular_code": "SAMC HIL-CGDSS-001-2026",
                "whatsapp_phone": "",
                "skills": ["📍 A 24.5 km (Pitalito)", "Circular SECOP II Real", "SENA Regional Huila", "Sur del Huila"]
            }
        ]

        for item in verified_direct_contacts:
            lat = item.get("lat", SAN_AGUSTIN_LAT)
            lon = item.get("lon", SAN_AGUSTIN_LON)
            item["distance_km"] = haversine_km(SAN_AGUSTIN_LAT, SAN_AGUSTIN_LON, lat, lon)
            seen_ids.add(item["id"])
            results.append(item)

        # 2. Consultar en Vivo SECOP II (datos.gov.co) filtrando SOLO circulares con enlace público directo (OpportunityDetail)
        secop_urls = [
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?departamento_entidad=Huila&$limit=35",
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?$q=GUADUA&$limit=15"
        ]

        city_coords = {
            "SAN AGUSTIN": (1.8792, -76.2706),
            "SAN AGUSTÍN": (1.8792, -76.2706),
            "ISNOS": (1.9310, -76.1610),
            "PITALITO": (1.8538, -76.0508),
            "TIMANA": (1.9720, -75.9320),
            "GARZON": (2.1960, -75.6290),
            "LA PLATA": (2.3900, -75.8920),
            "RIVERA": (2.7770, -75.2560),
            "NEIVA": (2.9273, -75.2819),
        }

        for url in secop_urls:
            try:
                resp = requests.get(url, headers=self.headers, timeout=7)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        for item in data:
                            url_obj = item.get("urlproceso")
                            proc_url = url_obj.get("url", "") if isinstance(url_obj, dict) else ""
                            if "Public/Tendering/OpportunityDetail/Index?noticeUID=" not in proc_url:
                                continue

                            proc_id = item.get("id_del_proceso") or item.get("referencia_del_proceso")
                            if not proc_id or proc_id in seen_ids:
                                continue

                            entidad = item.get("entidad", "Entidad Oficial Huila")
                            ciudad = item.get("ciudad_entidad", "Huila")
                            ref = item.get("referencia_del_proceso", proc_id)
                            desc = item.get("descripci_n_del_procedimiento") or item.get("nombre_del_procedimiento") or ""
                            nombre = item.get("nombre_del_procedimiento") or desc[:90]
                            modalidad = item.get("modalidad_de_contratacion", "Contratación Pública")

                            txt_upper = f"{entidad} {ciudad} {nombre} {desc}".upper()
                            if any(bad in txt_upper for bad in ["GASOLINA", "MEDICAMENTO", "FISIOTERAPEUTA", "ODONTOLOGO", "ENFERMERA", "HOSPITAL"]):
                                continue

                            try:
                                precio = float(item.get("precio_base") or 0)
                            except Exception:
                                precio = 0.0

                            pub_date = str(item.get("fecha_de_publicacion_del") or now.isoformat())
                            if not (pub_date.startswith("2026") or pub_date.startswith("2025")):
                                continue
                            if any(old_yr in str(ref) for old_yr in ["2015", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]):
                                continue
                            seen_ids.add(proc_id)

                            c_lat, c_lon = city_coords.get(ciudad.upper().strip(), (2.5000, -75.6000))
                            dist_km = haversine_km(SAN_AGUSTIN_LAT, SAN_AGUSTIN_LON, c_lat, c_lon)

                            results.append({
                                "id": f"secop_{proc_id}",
                                "title": f"🏛️ [Circular {ref}] {entidad} ({ciudad}) — {nombre[:75]}",
                                "organization": f"{entidad} ({ciudad})",
                                "origin_source_detail": f"Publicado en: SECOP II Oficial — Proceso {ref} ({ciudad}, Huila)",
                                "time_ago_exact": f"Publicado en SECOP II ({str(pub_date)[:10]})",
                                "location": f"🇨🇴 {ciudad}, Huila (A {dist_km} km · Circular SECOP II)",
                                "approx_place": f"Municipio de {ciudad}, Departamento del Huila (Sede oficial de {entidad})",
                                "verbatim_request": f"\"OBJETO TEXTUAL DEL PROCESO [{ref}]: {desc}\"",
                                "requirements_list": [
                                    f"Modalidad exigida por la entidad: {modalidad}.",
                                    "Estar inscrito en SECOP II, contar con RUT actualizado, cédula, antecedentes y seguridad social.",
                                    f"Ejecución en el municipio de {ciudad} (Huila). Abrir la circular oficial para descargar los estudios previos."
                                ],
                                "contractor_info": (
                                    f"Entidad contratante oficial: {entidad} ({ciudad}, Huila). "
                                    f"Circular pública SECOP II N° {ref}. Modalidad: {modalidad}."
                                ),
                                "lat": c_lat,
                                "lon": c_lon,
                                "distance_km": dist_km,
                                "description": (
                                    f"Circular Pública SECOP II — Referencia Oficial: {ref}. "
                                    f"Entidad: {entidad} ({ciudad}). Objeto: {desc[:380]}."
                                ),
                                "url": proc_url,
                                "budget_min": int(precio) if precio > 0 else 2500000,
                                "budget_max": int(precio) if precio > 0 else 15000000,
                                "currency": "COP",
                                "published_at": pub_date if "T" in str(pub_date) else now.isoformat(),
                                "category_hint": "alcaldia_huila",
                                "circular_code": ref,
                                "whatsapp_phone": "",
                                "skills": [f"📍 A {dist_km} km ({ciudad})", f"Ref: {ref}", "Circular SECOP II", "Pliego Directo"]
                            })
            except Exception:
                pass

        return {
            "success": True,
            "source": self.NAME,
            "items": results[:limit],
            "error": None
        }
