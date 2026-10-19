import re
from datetime import datetime, timezone

class ScoringEngine:
    # Practical skills the user actually wants to do (NO Systems Engineering degree required)
    PRACTICAL_SKILLS = [
        ('planos', r'\b(planos?|autocad|dwg|cad|arquitect\w*|remodelaci\w*|interiores|layout|mobiliario|cocinas)\b', 32, 'planos_3d'),
        ('3d / render', r'\b(3d|renders?|modelado|blender|sketchup|stl|obj|animaci\w*|roblox|unity)\b', 30, 'planos_3d'),
        ('whatsapp / bot', r'\b(whatsapp|bots?|chatbot|manychat|respuestas?\s+autom\w*|atenci[oó]n\s+al\s+cliente)\b', 34, 'automatizacion'),
        ('automatización', r'\b(automatizaci\w*|automatizar|automation|n8n|make|zapier|power\s+automate|flujos?|webhook)\b', 32, 'automatizacion'),
        ('ia práctica', r'\b(ia|inteligencia\s+artificial|ai\s+agent|agente|chatgpt|openai|prompt)\b', 24, 'automatizacion'),
        ('web / catálogo', r'\b(p[aá]ginas?\s+web|landing\s+page|cat[aá]logos?|wordpress|elementor|wix|shopify|tienda|men[uú]|reservas?)\b', 28, 'web_diseno'),
        ('diseño / vector', r'\b(dise[ñn]o|infograf\w*|vector\w*|ilustraci\w*|logo|flyer|dtf|canva|figma|ui/ux|visual)\b', 25, 'web_diseno'),
        ('tareas / datos', r'\b(excel|google\s+sheets|datos|data\s+collection|listados|mercado\s+libre|edici[oó]n|reels|guiones)\b', 22, 'tareas_rapidas')
    ]

    # Strict blocklist of corporate engineering, legal, accounting, or complex jobs the user does NOT want
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
            age_hours = 2.0

        if age_hours <= 2:
            return age_hours, 20.0, f"🔥 Hace {max(5, int(age_hours * 60))} min"
        elif age_hours <= 24:
            return age_hours, 16.0, f"🔥 Hoy ({max(1, int(age_hours))}h)"
        elif age_hours <= 72:
            days = max(1, int(age_hours // 24))
            return age_hours, 10.0, f"⚡ Hace {days}d"
        else:
            days = max(1, int(age_hours // 24))
            return age_hours, 0.0, f"Hace {days}d"

    def analyze(self, opp):
        title = opp.get('title', '')
        desc = opp.get('description', '')
        source = opp.get('source', '')
        loc = opp.get('location', '')
        tags = ' '.join([str(t) for t in opp.get('observed_data', {}).get('tags', [])])
        full_text = f"{title} {desc} {tags}"

        # 1. Immediately discard blocked corporate engineering / legal / accounting jobs
        if self.BLOCKED_PATTERNS.search(title) or (
            self.BLOCKED_PATTERNS.search(desc[:300]) and opp.get('opportunity_type') != 'cliente_directo_colombia'
        ):
            opp['decision'] = 'DESCARTAR'
            opp['overall_score'] = 5.0
            opp['skills'] = []
            opp['reasoning'] = 'Descartado: Requiere perfil corporativo/ingeniería pesada o área ajena (contabilidad/legal).'
            opp['next_action'] = 'Ignorar.'
            opp['estimated_data'] = {'age_hours': 999, 'freshness_label': 'Descartado'}
            return opp

        # 2. Match practical doable skills
        detected_skills = list(opp.get('skills') or [])
        raw_fit = 0.0
        matched_cats = set()

        for label, pattern, weight, cat in self.PRACTICAL_SKILLS:
            if re.search(pattern, full_text, re.IGNORECASE):
                if label not in detected_skills:
                    detected_skills.append(label)
                if re.search(pattern, title, re.IGNORECASE):
                    raw_fit += weight * 1.35
                else:
                    raw_fit += weight
                matched_cats.add(cat)

        # If no practical skill matched at all, discard it so the user never sees useless jobs
        if not detected_skills and opp.get('opportunity_type') != 'cliente_directo_colombia':
            opp['decision'] = 'DESCARTAR'
            opp['overall_score'] = 10.0
            opp['skills'] = []
            opp['reasoning'] = 'Descartado: No corresponde a automatizaciones, planos, 3D, web ni tareas prácticas.'
            opp['next_action'] = 'Ignorar.'
            opp['estimated_data'] = {'age_hours': 999, 'freshness_label': 'Descartado'}
            return opp

        # 3. Colombia Priority Bonus (+22 points for Colombian clients!)
        is_colombia = (
            'colombia' in source.lower()
            or 'colombia' in loc.lower()
            or 'colombia' in full_text.lower()
            or opp.get('currency') == 'COP'
        )
        if is_colombia:
            raw_fit += 25.0
            if '🇨🇴 Colombia' not in detected_skills:
                detected_skills.insert(0, '🇨🇴 Colombia')

        fit_score = min(100.0, max(20.0, round(raw_fit, 1)))

        # 4. Freshness & Money Score
        age_hours, fresh_bonus, fresh_label = self.compute_age_and_freshness(opp.get('published_at'))
        money_score = 88.0 if (opp.get('payment_min') or opp.get('payment_max')) else 70.0
        reusability_score = 90.0 if ('automatizacion' in matched_cats or 'planos_3d' in matched_cats or is_colombia) else 65.0

        overall_score = round(min(99.0, (fit_score * 0.50) + (money_score * 0.20) + (reusability_score * 0.15) + fresh_bonus), 1)

        # 5. Decision Classification
        if opp.get('opportunity_type') == 'cliente_directo_colombia':
            decision = 'CONSTRUIR_Y_VENDER' if 'whatsapp' in ' '.join(detected_skills).lower() else 'PRIORIDAD'
            reasoning = f"🇨🇴 Cliente real en {source} sin contratos legales. Puedes ofrecerle servicio directo hoy mismo y cobrar en pesos (Nequi / Bancolombia)."
            next_action = "Abrir su Instagram/Facebook o WhatsApp directo y enviarle el mensaje corto listo."
            est_hours = "1 a 3 días (Entrega rápida)"
            est_comp = "MUY BAJA (Contacto directo)"
        elif is_colombia and fit_score >= 55.0:
            decision = 'PRIORIDAD'
            reasoning = f"🇨🇴 [{fresh_label}] Proyecto publicado desde Colombia ({', '.join(detected_skills[:3])}). Sin contratos legales complejos."
            next_action = "Copiar la propuesta corta en español y enviarla de inmediato antes que otros."
            est_hours = "1 a 4 días"
            est_comp = "BAJA"
        elif overall_score >= 74.0:
            decision = 'PRIORIDAD'
            reasoning = f"[{fresh_label}] Tarea práctica realizable ({', '.join(detected_skills[:3])}) con pago directo por entregable."
            next_action = "Enviar propuesta corta ofreciendo muestra rápida en 24-48h."
            est_hours = "1 a 3 días"
            est_comp = "BAJA - MEDIA"
        else:
            decision = 'INVESTIGAR'
            reasoning = f"[{fresh_label}] Tarea práctica ({', '.join(detected_skills[:3])}) compatible con tus habilidades."
            next_action = "Revisar descripción y cotizar si el alcance es rápido."
            est_hours = "2 a 5 días"
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
            'estimated_difficulty': 'FÁCIL - MEDIA (Sin Ingeniería)',
            'competition_level': est_comp,
            'is_colombia': is_colombia
        }
        return opp
