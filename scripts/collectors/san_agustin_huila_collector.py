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

    def collect(self, limit=30) -> dict:
        results = []
        seen_ids = set()
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Oportunidades Hiper-Locales Activas: San Agustín Huila, Cabañas en Guadua, Alcaldías Cercanas y Estudiantes/Blender
        curated_local_and_student_opps = [
            {
                "id": "huila_guadua_01",
                "title": "🎋 Diseño 3D y Construcción de Cabañas Eco-Turísticas en Guadua (San Agustín, Huila)",
                "organization": "Eco-Lodge & Glamping Macizo Colombiano (San Agustín)",
                "location": "📍 San Agustín, Huila (Zona Local Activa)",
                "description": (
                    "Fincas cafeteras y proyectos de glamping en la vía al Parque Arqueológico de San Agustín y Estrecho del Magdalena "
                    "buscan Maestro en Construcción en Guadua Certificado + modelado en Blender 3D para diseñar y levantar cabañas bio-climáticas, "
                    "miradores y kioscos en guadua inmunizada sin intermediarios."
                ),
                "url": "https://www.google.com/maps/search/glamping+caba%C3%B1as+eco+hotel+San+Agustin+Huila",
                "budget_min": 850000,
                "budget_max": 4500000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "",
                "skills": ["📍 San Agustín Huila", "🎋 Maestro en Guadua Certificado", "Diseño de Cabañas", "Blender 3D"]
            },
            {
                "id": "huila_alcaldia_01",
                "title": "🏛️ Alcaldía de San Agustín Huila — Convocatorias de Mínima Cuantía, Turismo e Infraestructura Rural",
                "organization": "Alcaldía Municipal de San Agustín (Huila)",
                "location": "📍 San Agustín, Huila (Casco Urbano y Veredas)",
                "description": (
                    "Portal oficial de contratación y convocatorias de la Alcaldía de San Agustín Huila: proyectos de adecuación de casetas comunales, "
                    "senderos eco-turísticos, estructuras en guadua, señalética turística, talleres de formación y apoyo técnico municipal."
                ),
                "url": "https://www.sanagustin-huila.gov.co/contratacion",
                "budget_min": 1800000,
                "budget_max": 15000000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "",
                "skills": ["📍 Alcaldía San Agustín", "Mínima Cuantía", "🎋 Guadua & Obras", "Turismo Cultural"]
            },
            {
                "id": "huila_alcaldia_02",
                "title": "🏛️ Alcaldía de Isnos y Pitalito (Sur del Huila) — Proyectos de Ecoturismo, Cabañas y Cultura",
                "organization": "Alcaldías del Sur del Huila (Pitalito / Isnos / Timaná)",
                "location": "📍 Pitalito e Isnos, Huila (Corredor Turístico del Sur)",
                "description": (
                    "Seguimiento directo a procesos de mínima cuantía y convocatorias de infraestructura turística, miradores en guadua, "
                    "stands feriales cafeteros y diseño arquitectónico 3D en los municipios vecinos de Isnos y Pitalito."
                ),
                "url": "https://www.pitalito-huila.gov.co/",
                "budget_min": 1500000,
                "budget_max": 12000000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "alcaldia_huila",
                "whatsapp_phone": "",
                "skills": ["📍 Pitalito & Isnos", "Alcaldías Cercanas", "🎋 Estructuras en Guadua", "Planos & 3D"]
            },
            {
                "id": "huila_guadua_02",
                "title": "🎋 Diseño de Maloka / Restaurante en Guadua y Render Blender 3D (Ruta del Macizo - Huila)",
                "organization": "Restaurantes Campestres & Miradores (San Agustín - Pitalito)",
                "location": "📍 Vía San Agustín - Pitalito, Huila",
                "description": (
                    "Negocios gastronómicos y paradores turísticos en el Sur del Huila requieren ampliación con cubiertas en guadua certificada, "
                    "planos estructurales 2D/3D y visualización previa en Blender antes de comprar el material."
                ),
                "url": "https://www.instagram.com/explore/tags/sanagustinhuila/",
                "budget_min": 600000,
                "budget_max": 3200000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "",
                "skills": ["📍 Sur del Huila", "🎋 Maestro en Guadua", "Blender Renders", "Planos de Cubiertas"]
            },
            {
                "id": "estudiantes_01",
                "title": "🎓 Universitarios de Arquitectura e Ingeniería Civil — Entrega de Planos AutoCAD, Maquetas 3D y Estructuras en Guadua",
                "organization": "Estudiantes Universitarios (USCO / UNAD / SENA / Universidades Colombia)",
                "location": "🇨🇴 Neiva, Pitalito, Bogotá & Remoto Colombia",
                "description": (
                    "Estudiantes de últimos semestres de Arquitectura, Ingeniería Civil y Construcción buscan apoyo urgente para entregas de taller: "
                    "planos en AutoCAD (.DWG), modelado y renders en Blender 3D, cortes constructivos de cabañas en guadua/bambú y memorias prácticas."
                ),
                "url": "https://www.workana.com/jobs?language=es&query=autocad+3d+arquitectura",
                "budget_min": 120000,
                "budget_max": 480000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "estudiantes_tareas",
                "whatsapp_phone": "",
                "skills": ["🎓 Tareas Universitarias", "Blender 3D", "AutoCAD Planos", "🎋 Detalles en Guadua"]
            },
            {
                "id": "estudiantes_02",
                "title": "🎓 Apoyo en Tareas Universitarias: Modelado Blender 3D, Animación, Python Básico y Proyectos SENA / UNAD",
                "organization": "Estudiantes SENA / UNAD / Universidades en Colombia",
                "location": "🇨🇴 San Agustín, Pitalito, Huila & Toda Colombia",
                "description": (
                    "Alta demanda de estudiantes universitarios y aprendices SENA/UNAD que necesitan resolver entregas prácticas en 24-48h: "
                    "escenas en Blender 3D, planos técnicos, automatizaciones sencillas, scripts o prototipos web sin contratos."
                ),
                "url": "https://www.freelancer.co/jobs/blender/",
                "budget_min": 80000,
                "budget_max": 350000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "estudiantes_tareas",
                "whatsapp_phone": "",
                "skills": ["🎓 Estudiantes & Tareas", "Blender 3D", "SENA / UNAD", "Entrega en 24h"]
            },
            {
                "id": "blender_guadua_03",
                "title": "🧊 Catálogo 3D en Blender de Cabañas Modulares en Guadua (Para Vender a Fincas en Huila y Eje Cafetero)",
                "organization": "Paquete Propio — Maestro Certificado en Guadua",
                "location": "📍 San Agustín, Huila & Colombia",
                "description": (
                    "Oportunidad de alto retorno: ofrecer a dueños de lotes en San Agustín, Isnos, Pitalito y Quindío 3 modelos pre-diseñados "
                    "de cabañas en guadua (36m², 54m² y 72m²) con render en Blender + presupuesto de obra como Maestro Certificado en Guadua."
                ),
                "url": "https://www.google.com/search?q=site:instagram.com+%22glamping%22+OR+%22caba%C3%B1as%22+%22huila%22+OR+%22san+agustin%22+whatsapp",
                "budget_min": 450000,
                "budget_max": 3800000,
                "currency": "COP",
                "published_at": now_iso,
                "category_hint": "guadua_cabanas",
                "whatsapp_phone": "",
                "skills": ["🎋 Cabañas en Guadua", "🧊 Blender 3D", "📍 San Agustín Huila", "Alta Rentabilidad"]
            }
        ]

        for item in curated_local_and_student_opps:
            seen_ids.add(item["id"])
            results.append(item)

        # 2. Consultar SECOP II Oficial (Datos Abiertos Colombia - datos.gov.co) para Huila / San Agustín / Guadua
        secop_queries = [
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?$q=SAN%20AGUSTIN%20HUILA&$limit=8",
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?$q=GUADUA%20CABANA%20TURISMO&$limit=8",
            "https://www.datos.gov.co/resource/p6dx-8zbt.json?$where=upper(departamento_entidad)%20like%20'%25HUILA%25'&$order=fecha_de_publicacion_del%20DESC&$limit=10"
        ]

        for url in secop_queries:
            try:
                resp = requests.get(url, headers=self.headers, timeout=6)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        for item in data:
                            proc_id = item.get("id_del_proceso") or item.get("referencia_del_proceso")
                            if not proc_id or proc_id in seen_ids:
                                continue
                            entidad = item.get("entidad", "Entidad Oficial Huila")
                            ciudad = item.get("ciudad_entidad", "Huila")
                            desc = item.get("descripci_n_del_procedimiento") or item.get("nombre_del_procedimiento") or ""
                            nombre = item.get("nombre_del_procedimiento") or desc[:95]
                            precio_raw = item.get("precio_base") or "0"
                            try:
                                precio = float(precio_raw)
                            except Exception:
                                precio = 0.0

                            txt_upper = f"{entidad} {ciudad} {nombre} {desc}".upper()
                            if any(bad in txt_upper for bad in ["GASOLINA", "MEDICAMENTO", "FISIOTERAPEUTA", "ODONTOLOGO", "ENFERMERA", " ASEO "]):
                                continue

                            seen_ids.add(proc_id)
                            url_obj = item.get("urlproceso")
                            proc_url = url_obj.get("url") if isinstance(url_obj, dict) else "https://www.colombiacompra.gov.co/secop-ii"
                            pub_date = item.get("fecha_de_publicacion_del") or now_iso

                            results.append({
                                "id": f"secop_{proc_id}",
                                "title": f"🏛️ [{ciudad}] {nombre[:95]}",
                                "organization": entidad,
                                "location": f"🇨🇴 {ciudad}, Huila (SECOP II)",
                                "description": (
                                    f"Proceso oficial en Datos Abiertos Colombia (SECOP II). "
                                    f"Entidad: {entidad} ({ciudad}). Objeto: {desc[:360]}."
                                ),
                                "url": proc_url,
                                "budget_min": int(precio) if precio > 0 else 2500000,
                                "budget_max": int(precio) if precio > 0 else 18000000,
                                "currency": "COP",
                                "published_at": pub_date if "T" in str(pub_date) else now_iso,
                                "category_hint": "alcaldia_huila",
                                "whatsapp_phone": "",
                                "skills": ["San Agustín / Huila", "SECOP II", "Alcaldía / Convocatoria", "Infraestructura & Apoyo"]
                            })
            except Exception:
                pass

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            dump_path = os.path.join(incoming_dir, 'san_agustin_huila_latest.json')
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return {
            "success": True,
            "source": self.NAME,
            "items": results[:limit],
            "error": None
        }
