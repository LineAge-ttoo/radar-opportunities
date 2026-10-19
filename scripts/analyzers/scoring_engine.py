import re
from datetime import datetime, timezone


class ScoringEngine:
    PRACTICAL_SKILLS = [
        ('guadua / cabañas', r'\b(guadua|bamb[uú]|caba[ñn]as?|glamping|eco-?lodge|maloka|mirador|kiosco|bioconstrucci\w*)\b', 42, 'guadua_cabanas'),
        ('san agustín / huila', r'\b(san\s+agust[ií]n|pitalito|isnos|huila|timan[aá]|neiva|macizo|alcald[ií]a|secop)\b', 40, 'alcaldia_huila'),
        ('estudiantes / tareas', r'\b(estudiantes?|universitari\w*|tareas?|sena|unad|usco|maquetas?|entregas?|taller|grado)\b', 36, 'estudiantes_tareas'),
        ('blender / 3d', r'\b(blender|3d|renders?|modelado|sketchup|stl|obj|animaci\w*|roblox|unity)\b', 35, 'planos_3d'),
        ('planos / autocad', r'\b(planos?|autocad|dwg|cad|arquitect\w*|remodelaci\w*|interiores|layout|mobiliario|cocinas)\b', 34, 'planos_3d'),
        ('whatsapp / bot', r'\b(whatsapp|bots?|chatbot|manychat|respuestas?\s+autom\w*|atenci[oó]n\s+al\s+cliente)\b', 34, 'automatizacion'),
        ('automatización', r'\b(automatizaci\w*|automatizar|automation|n8n|make|zapier|power\s+automate|flujos?|webhook)\b', 32, 'automatizacion'),
        ('web / catálogo', r'\b(p[aá]ginas?\s+web|landing\s+page|cat[aá]logos?|wordpress|elementor|wix|shopify|tienda|men[uú]|reservas?)\b', 28, 'web_diseno'),
        ('diseño / vector', r'\b(dise[ñn]o|infograf\w*|vector\w*|ilustraci\w*|logo|flyer|dtf|canva|figma|ui/ux|visual)\b', 25, 'web_diseno'),
        ('tareas / datos', r'\b(excel|google\s+sheets|datos|data\s+collection|listados|mercado\s+libre|edici[oó]n|reels|guiones)\b', 22, 'tareas_rapidas')
    ]

    BLOCKED_PATTERNS = re.compile(
        r'\b(ingeniero\s+de\s+sistemas|senior\s+software|staff\s+engineer|devops|kubernetes|docker\s+swarm|'
        r'c\+\+|golang|rust|java\s+developer|spring\s+boot|\.net\s+core|contador|bookkeeper|quickbooks|'
        r'asesor[ií]a\s+legal|abogado|impuestos|pcb\s+design|microcontroller|firmware|closers?\s+de\s+ventas|'
        r'endosc[oó]pica|m[eé]dico|enfermer\w*|sap\s+abap|oracle\s+dba|cobol)\b',
        re.IGNORECASE
    )

    @staticmethod
    def compute_age_and_freshness(published_at_str):
        now = datetime.now(timezone.utc)
        try:
            s = str(published_at_str or '').replace('Z', '+00:00')
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            diff_sec = max(0.0, (now - dt).total_seconds())
            age_hours = round(diff_sec / 3600.0, 1)
        except Exception:
            age_hours = 0.5

        if age_hours <= 2:
            return age_hours, 22.0, f"Hace {max(5, int(age_hours * 60))} min"
        elif age_hours <= 24:
            return age_hours, 18.0, f"Hoy ({max(1, int(age_hours))}h)"
        elif age_hours <= 72:
            days = max(1, int(age_hours // 24))
            return age_hours, 12.0, f"Hace {days}d"
        else:
            days = max(1, int(age_hours // 24))
            return age_hours, 4.0, f"Hace {days}d"

    def analyze(self, opp):
        title = opp.get('title', '')
        desc = opp.get('description', '')
        source = opp.get('source', '')
        loc = opp.get('location', '')
        opp_type = opp.get('opportunity_type', '')
        tags = ' '.join([str(t) for t in opp.get('observed_data', {}).get('tags', [])])
        full_text = f"{title} {desc} {tags} {loc} {source}"

        if self.BLOCKED_PATTERNS.search(title) or (
            self.BLOCKED_PATTERNS.search(desc[:300]) and opp_type not in ('cliente_directo_colombia', 'san_agustin_huila_prioridad')
        ):
            opp['decision'] = 'DESCARTAR'
            opp['overall_score'] = 5.0
            opp['skills'] = []
            opp['reasoning'] = 'Descartado: Requiere perfil corporativo/ingeniería pesada.'
            opp['next_action'] = 'Ignorar.'
            opp['estimated_data'] = {'age_hours': 999, 'freshness_label': 'Descartado'}
            return opp

        detected_skills = list(opp.get('skills') or [])
        raw_fit = 0.0
        matched_cats = set()

        for label, pattern, weight, cat in self.PRACTICAL_SKILLS:
            if re.search(pattern, full_text, re.IGNORECASE):
                if label not in detected_skills:
                    detected_skills.append(label)
                if re.search(pattern, title, re.IGNORECASE):
                    raw_fit += weight * 1.4
                else:
                    raw_fit += weight
                matched_cats.add(cat)

        if not detected_skills and opp_type not in ('cliente_directo_colombia', 'san_agustin_huila_prioridad'):
            opp['decision'] = 'DESCARTAR'
            opp['overall_score'] = 10.0
            opp['skills'] = []
            opp['reasoning'] = 'Descartado: Fuera del enfoque práctico.'
            opp['next_action'] = 'Ignorar.'
            opp['estimated_data'] = {'age_hours': 999, 'freshness_label': 'Descartado'}
            return opp

        is_huila_or_guadua = (
            opp_type == 'san_agustin_huila_prioridad'
            or 'guadua_cabanas' in matched_cats
            or 'alcaldia_huila' in matched_cats
            or 'estudiantes_tareas' in matched_cats
        )
        is_colombia = (
            is_huila_or_guadua
            or 'colombia' in source.lower()
            or 'colombia' in loc.lower()
            or 'colombia' in full_text.lower()
            or opp.get('currency') == 'COP'
        )

        if is_huila_or_guadua:
            raw_fit += 38.0
        elif is_colombia:
            raw_fit += 25.0

        fit_score = min(100.0, max(25.0, round(raw_fit, 1)))
        age_hours, fresh_bonus, fresh_label = self.compute_age_and_freshness(opp.get('published_at'))
        money_score = 92.0 if (opp.get('payment_min') or opp.get('payment_max')) else 75.0
        reusability_score = 95.0 if is_huila_or_guadua else (88.0 if is_colombia else 68.0)

        overall_score = round(min(99.0, (fit_score * 0.52) + (money_score * 0.20) + (reusability_score * 0.15) + fresh_bonus), 1)
        if is_huila_or_guadua:
            overall_score = max(95.0, overall_score)

        if is_huila_or_guadua:
            decision = 'PRIORIDAD'
            reasoning = "Oportunidad de altísimo potencial en tu zona (San Agustín / Huila / Guadua / Estudiantes / Blender)."
            next_action = "Revisar y enviar mensaje directo o alerta a tu WhatsApp 3222739034."
            est_hours = "24 a 72 horas"
            est_comp = "MUY BAJA (Ventaja Local + Certificado Guadua)"
        elif opp_type == 'cliente_directo_colombia':
            decision = 'CONSTRUIR_Y_VENDER'
            reasoning = f"Cliente directo en {source} sin contratos legales. Cobro en COP por Nequi / Bancolombia."
            next_action = "Contactar por WhatsApp o Instagram DM."
            est_hours = "1 a 3 días"
            est_comp = "MUY BAJA"
        elif overall_score >= 75.0:
            decision = 'PRIORIDAD'
            reasoning = f"[{fresh_label}] Encargo práctico realizable ({', '.join(detected_skills[:3])})."
            next_action = "Enviar propuesta ofreciendo primer avance en 24h."
            est_hours = "1 a 3 días"
            est_comp = "BAJA"
        else:
            decision = 'INVESTIGAR'
            reasoning = f"[{fresh_label}] Encargo compatible ({', '.join(detected_skills[:3])})."
            next_action = "Revisar alcance y cotizar."
            est_hours = "2 a 4 días"
            est_comp = "MEDIA"

        opp['skills'] = detected_skills[:6]
        opp['fit_score'] = fit_score
        opp['money_score'] = money_score
        opp['reusability_score'] = reusability_score
        opp['overall_score'] = overall_score
        opp['decision'] = decision
        opp['reasoning'] = reasoning
        opp['next_action'] = next_action
        opp['estimated_data'] = {
            'age_hours': age_hours,
            'freshness_label': fresh_label,
            'estimated_hours': est_hours,
            'estimated_difficulty': 'VIABLE / DIRECTO',
            'competition_level': est_comp,
            'is_colombia': is_colombia,
            'is_huila_guadua': is_huila_or_guadua
        }
        return opp
