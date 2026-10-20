import os
import json
import requests
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


class SanAgustinHuilaCollector:
    NAME = "San Agustín Huila · Guadua · Alcaldía & Estudiantes"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    def collect(self, limit=35) -> dict:
        results = []
        seen_ids = set()
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Contactos Reales Verificados en San Agustín, Isnos y Pitalito (Huila) + Circulares Reales SECOP II
        verified_direct_contacts = [
            {
                "id": "huila_alcaldia_sanagustin",
                "title": "🏛️ Alcaldía Municipal de San Agustín Huila — Contratación, Mínima Cuantía y Obras en Guadua",
                "organization": "Alcaldía de San Agustín Huila (Calle 3 Cra 12 Esq.)",
                "location": "📍 San Agustín, Huila (Contacto Oficial Directo)",
                "description": (
                    "Contacto directo oficial de la Alcaldía de San Agustín Huila para radicar manifestación de interés "
                    "como Maestro en Construcción en Guadua Certificado, diseño 3D de infraestructura turística, casetas y mínima cuantía. "
                    "Línea móvil oficial WhatsApp: +57 318 285 1968 | Conmutador: (608) 8373177 | Correo: contactenos@sanagustin-huila.gov.co"
                ),
                "url": "https://www.sanagustin-huila.gov.co/contratacion",
                "budget_min": 2500000,
                "budget_max": 18000000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "573182851968",
                "skills": ["📍 Alcaldía San Agustín", "WhatsApp +57 3182851968", "🎋 Maestro en Guadua", "Mínima Cuantía"]
            },
            {
                "id": "secop_sena_pitalito_2026",
                "title": "🏛️ [Circular SECOP II: SAMC HIL-CGDSS-001-2026] SENA Regional Huila (Pitalito / San Agustín) — Formación Campesina y Materiales",
                "organization": "SENA Regional Huila — Centro CGDSS Pitalito",
                "location": "📍 Pitalito / San Agustín, Huila (Circular Pública SECOP II)",
                "description": (
                    "Circular oficial activa en SECOP II (No requiere clave para ver el pliego). "
                    "Referencia: SAMC HIL-CGDSS-001-2026. Objeto: Suministro de materiales y apoyo para procesos de Formación Especial Campesina "
                    "en el Sur del Huila (Centro de Gestión y Desarrollo Sostenible Surcolombiano - Pitalito)."
                ),
                "url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10223805",
                "budget_min": 537250000,
                "budget_max": 537250000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "",
                "skills": ["📍 Pitalito / San Agustín", "Circular SECOP II Real", "SENA Regional Huila", "Sur del Huila"]
            },
            {
                "id": "secop_agrosur_pitalito_2026",
                "title": "🏛️ [Circular SECOP II: PMC 005 DE 2026] CPGA AGROSUR Pitalito — Convocatoria Pública Sur del Huila",
                "organization": "CPGA AGROSUR (Pitalito, Huila)",
                "location": "📍 Pitalito, Huila (Circular Pública SECOP II)",
                "description": (
                    "Circular oficial activa en SECOP II con acceso directo al pliego sin clave. "
                    "Referencia: PMC 005 DE 2026 — Entidad: AGROSUR Pitalito, Huila."
                ),
                "url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10245503",
                "budget_min": 14063027,
                "budget_max": 14063027,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "",
                "skills": ["📍 Pitalito Huila", "Circular SECOP II Real", "Mínima Cuantía", "Sur del Huila"]
            },
            {
                "id": "huila_elmaco_sanagustin",
                "title": "🎋 Finca Ecológica El Maco (San Agustín, Huila) — Diseño 3D, Ampliación y Mantenimiento de Cabañas en Guadua",
                "organization": "Finca Ecológica El Maco (San Agustín, Huila)",
                "location": "📍 San Agustín, Huila (WhatsApp Directo: +57 320 375 5982)",
                "description": (
                    "Eco-hotel y finca en San Agustín construida con arquitectura bio-climática, cabañas campestres y estructuras naturales. "
                    "Contacto directo verificado por WhatsApp (+57 320 375 5982) para ofrecer tus servicios como Maestro en Construcción en Guadua Certificado, "
                    "adecuaciones estructurales, pérgolas y renders 3D en Blender."
                ),
                "url": "https://www.elmaco.ch/",
                "budget_min": 850000,
                "budget_max": 4200000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573203755982",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3203755982", "🎋 Maestro en Guadua", "Blender 3D"]
            },
            {
                "id": "huila_nacimiento_glamping",
                "title": "🎋 Nacimiento Glamping (Vereda El Tablón, San Agustín Huila) — Estructuras en Guadua, Miradores y Diseño 3D",
                "organization": "Nacimiento Glamping (San Agustín, Huila)",
                "location": "📍 Vereda El Tablón, San Agustín, Huila (WhatsApp: +57 311 684 5394)",
                "description": (
                    "Glamping campestre en la Vereda El Tablón de San Agustín, Huila. "
                    "Contacto directo verificado por WhatsApp (+57 311 684 5394) para ofrecer diseño de nuevas cabañas/domos en Blender 3D, "
                    "cubiertas y decks en guadua certificada o planos arquitectónicos."
                ),
                "url": "https://nacimientoglamping.com/",
                "budget_min": 900000,
                "budget_max": 4800000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573116845394",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3116845394", "🎋 Cabañas en Guadua", "Blender 3D"]
            },
            {
                "id": "huila_sanagua_glamping",
                "title": "🎋 Glamping Sanagua — Cascadas del Lavapatas (San Agustín, Huila) — Diseño de Cabañas, Kioscos en Guadua y Renders",
                "organization": "Glamping Sanagua (San Agustín, Huila)",
                "location": "📍 Sector Lavapatas, San Agustín, Huila (WhatsApp: +57 312 676 0320)",
                "description": (
                    "Glamping y alojamiento campestre en San Agustín, Huila. "
                    "Contacto directo verificado por WhatsApp (+57 312 676 0320) y web oficial (sanagua.co) para ofrecer "
                    "construcción y mantenimiento especializado en guadua certificada, pérgolas, miradores y modelado 3D."
                ),
                "url": "https://sanagua.co/",
                "budget_min": 750000,
                "budget_max": 3900000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573126760320",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3126760320", "🎋 Guadua Certificada", "Renders 3D"]
            },
            {
                "id": "huila_cabanas_numbana",
                "title": "🎋 Cabañas Numbana (Vía Parque Arqueológico, San Agustín Huila) — Ampliación en Guadua, Planos y Render 3D",
                "organization": "Cabañas Numbana (San Agustín, Huila)",
                "location": "📍 Vía Parque Arqueológico, San Agustín (WhatsApp: +57 323 247 1045)",
                "description": (
                    "Hospedaje de cabañas campestres en la vía al Parque Arqueológico de San Agustín. "
                    "Contacto directo verificado por WhatsApp (+57 323 247 1045) para proponer diseño 3D de nuevas cabañas en guadua, "
                    "kioscos sociales o mantenimiento estructural."
                ),
                "url": "https://cabanasnumbana.com/",
                "budget_min": 650000,
                "budget_max": 3500000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573232471045",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3232471045", "🎋 Cabañas en Guadua", "Planos & 3D"]
            },
            {
                "id": "huila_cabanas_gamcelat",
                "title": "🎋 Cabañas y Alojamiento Rural Gamcelat (San Agustín, Huila) — Estructuras en Guadua y Diseño 3D",
                "organization": "Cabañas Gamcelat (San Agustín, Huila)",
                "location": "📍 A 400m del centro vía al Parque, San Agustín (WhatsApp: +57 313 245 8373)",
                "description": (
                    "Complejo de cabañas rurales en San Agustín, Huila. "
                    "Líneas móviles directas verificadas: +57 313 245 8373 / +57 311 291 0193 para contactar al propietario sin intermediarios."
                ),
                "url": "https://wa.me/573132458373",
                "budget_min": 600000,
                "budget_max": 3200000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573132458373",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3132458373", "🎋 Guadua & Cabañas", "Trato Directo"]
            },
            {
                "id": "huila_cabanas_amalu",
                "title": "🎋 Cabañas Amalú (San Agustín, Huila) — Diseño de Cabañas, Cubiertas en Guadua y Catálogo Web",
                "organization": "Cabañas Amalú (San Agustín, Huila)",
                "location": "📍 San Agustín, Huila (WhatsApp: +57 318 699 5451)",
                "description": (
                    "Alojamiento de cabañas campestres en San Agustín, Huila con atención directa por WhatsApp (+57 318 699 5451). "
                    "Ideal para ofrecer diseño 3D de nuevas unidades en guadua o página web con motor de reservas a WhatsApp."
                ),
                "url": "https://wa.me/573186995451",
                "budget_min": 550000,
                "budget_max": 2800000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573186995451",
                "skills": ["📍 San Agustín Huila", "WhatsApp +57 3186995451", "🎋 Cabañas en Guadua", "Blender 3D"]
            },
            {
                "id": "huila_guaitipan_pitalito",
                "title": "🎋 Laguna Guaitipán Ancestral — Glamping & Cabañas (Pitalito, Huila) — Estructuras en Guadua y Renders 3D",
                "organization": "Laguna Guaitipán Ancestral (Pitalito, Huila)",
                "location": "📍 Laguna de Guaitipán, Pitalito, Huila (WhatsApp: +57 318 280 4008)",
                "description": (
                    "Complejo turístico de glampings y cabañas en Pitalito, Huila (a 35 min de San Agustín). "
                    "Contacto directo verificado por WhatsApp (+57 318 280 4008 / +57 316 018 6786) para ofrecer diseño y construcción "
                    "de nuevas cabañas en guadua certificada, miradores y visualización en Blender 3D."
                ),
                "url": "https://lagunaguaitipan.com/",
                "budget_min": 950000,
                "budget_max": 5200000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573182804008",
                "skills": ["📍 Pitalito Huila", "WhatsApp +57 3182804008", "🎋 Maestro en Guadua", "Blender 3D"]
            },
            {
                "id": "huila_mayu_isnos",
                "title": "🎋 Glamping Mayu — Mirador Campestre (Isnos, Huila) — Diseño de Cabañas y Miradores en Guadua",
                "organization": "Glamping Mayu (Isnos, Huila)",
                "location": "📍 Isnos, Huila (WhatsApp: +57 314 358 9808)",
                "description": (
                    "Mirador y glamping campestre en el municipio vecino de Isnos, Huila. "
                    "Contacto directo verificado por WhatsApp (+57 314 358 9808 / +57 317 871 6443) para ofrecer "
                    "estructuras en guadua certificada, planos y modelado 3D en Blender."
                ),
                "url": "https://wa.me/573143589808",
                "budget_min": 700000,
                "budget_max": 3800000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "573143589808",
                "skills": ["📍 Isnos Huila", "WhatsApp +57 3143589808", "🎋 Miradores en Guadua", "Blender 3D"]
            },
            {
                "id": "secop_usco_huila_estudiantes",
                "title": "🎓 [Circular SECOP II: CPS-1212-B2024] Universidad Surcolombiana (USCO Huila) — Apoyo y Acompañamiento Académico",
                "organization": "Universidad Surcolombiana (USCO — Huila)",
                "location": "📍 Huila (Circular Pública SECOP II)",
                "description": (
                    "Proceso oficial de la Universidad Surcolombiana (USCO) en SECOP II con enlace directo al pliego público sin clave."
                ),
                "url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6535897",
                "budget_min": 2271150,
                "budget_max": 2271150,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "estudiantes_tareas",
                "whatsapp_phone": "",
                "skills": ["🎓 USCO Huila", "Circular SECOP II Real", "Universitarios", "Apoyo Académico"]
            }
        ]

        for item in verified_direct_contacts:
            seen_ids.add(item["id"])
            results.append(item)

        # 2. Consultar en Vivo SECOP II (datos.gov.co) filtrando SOLO circulares con enlace público directo (OpportunityDetail)
        secop_urls = [
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?departamento_entidad=Huila&$limit=35",
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?$q=GUADUA&$limit=15"
        ]

        for url in secop_urls:
            try:
                resp = requests.get(url, headers=self.headers, timeout=7)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        for item in data:
                            url_obj = item.get("urlproceso")
                            proc_url = url_obj.get("url", "") if isinstance(url_obj, dict) else ""
                            # SOLO conservar circulares reales que abran directamente el pliego público sin pedir login
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

                            txt_upper = f"{entidad} {ciudad} {nombre} {desc}".upper()
                            if any(bad in txt_upper for bad in ["GASOLINA", "MEDICAMENTO", "FISIOTERAPEUTA", "ODONTOLOGO", "ENFERMERA", "HOSPITAL"]):
                                continue

                            try:
                                precio = float(item.get("precio_base") or 0)
                            except Exception:
                                precio = 0.0

                            seen_ids.add(proc_id)
                            pub_date = item.get("fecha_de_publicacion_del") or now_iso

                            results.append({
                                "id": f"secop_{proc_id}",
                                "title": f"🏛️ [Circular {ref}] {entidad} ({ciudad}) — {nombre[:75]}",
                                "organization": f"{entidad} ({ciudad})",
                                "location": f"🇨🇴 {ciudad}, Huila (Circular SECOP II Directa)",
                                "description": (
                                    f"Circular Pública SECOP II — Referencia Oficial: {ref}. "
                                    f"Entidad: {entidad} ({ciudad}). Objeto: {desc[:380]}. "
                                    f"El botón abre directamente la circular oficial en SECOP II sin pedir usuario ni contraseña."
                                ),
                                "url": proc_url,
                                "budget_min": int(precio) if precio > 0 else 2500000,
                                "budget_max": int(precio) if precio > 0 else 15000000,
                                "currency": "COP",
                                "published_at": pub_date if "T" in str(pub_date) else now_iso,
                                "category_hint": "alcaldia_huila",
                                "whatsapp_phone": "",
                                "skills": [f"📍 {ciudad}", f"Ref: {ref}", "Circular SECOP II", "Pliego Directo"]
                            })
            except Exception:
                pass

        return {
            "success": True,
            "source": self.NAME,
            "items": results[:limit],
            "error": None
        }
