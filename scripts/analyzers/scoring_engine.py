import json
import re
import os
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_SCORING_CONFIG = os.path.join(BASE_DIR, 'config', 'scoring', 'scoring_rules.json')

class ScoringEngine:
    def __init__(self, config_path=DEFAULT_SCORING_CONFIG):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8-sig') as f:
                cfg = json.load(f)
                self.skills_rules = cfg.get('skills', [])
                self.signals = cfg.get('opportunity_signals', {})
                self.weights = cfg.get('weights', {})
        else:
            self.skills_rules = []
            self.signals = {'positive': [], 'negative': []}
            self.weights = {'fit': 0.35, 'money': 0.20, 'trust': 0.15, 'reusability': 0.15, 'competition_inverse': 0.15}

        self.compiled_rules = []
        for s in self.skills_rules:
            kw = s['keyword'].strip()
            if kw.lower() == '3d':
                pattern = r'\b3d\b|\bthree\.?js\b|\bwebgl\b'
            elif kw.lower() == 'ai':
                pattern = r'\bai\b|\bartificial intelligence\b|\bllm\b|\bagents?\b|\bopenai\b|\banthropic\b|\blangchain\b'
            elif kw.lower() == 'ui/ux':
                pattern = r'\bui/ux\b|\bui design\b|\bux design\b|\bfigma\b'
            elif kw.lower() in ['bot', 'bots']:
                pattern = r'\bbots?\b|\btelegram\b|\bdiscord\b'
            elif kw.lower() in ['api', 'apis']:
                pattern = r'\bapis?\b|\bwebhook\b|\bgraphql\b|\brest\b'
            elif kw.lower() == 'node':
                pattern = r'\bnode(\.js)?\b|\bnodejs\b'
            else:
                pattern = r'\b' + re.escape(kw) + r'\b'

            self.compiled_rules.append({
                'keyword': kw,
                'weight': s.get('weight', 15),
                'category': s.get('category', 'general'),
                'regex': re.compile(pattern, re.IGNORECASE)
            })

    @staticmethod
    def compute_age_and_freshness(published_at_str):
        """Returns (age_hours, freshness_bonus, freshness_label)"""
        now = datetime.now(timezone.utc)
        try:
            s = str(published_at_str or '').replace('Z', '+00:00')
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            diff_sec = max(0.0, (now - dt).total_seconds())
            age_hours = round(diff_sec / 3600.0, 1)
        except Exception:
            age_hours = 48.0

        if age_hours <= 6:
            return age_hours, 18.0, f"🔥 Hace {max(1, int(age_hours))}h"
        elif age_hours <= 24:
            return age_hours, 15.0, "🔥 Publicado Hoy"
        elif age_hours <= 72:
            days = max(1, int(age_hours // 24))
            return age_hours, 10.0, f"⚡ Hace {days}d"
        elif age_hours <= 168:
            days = int(age_hours // 24)
            return age_hours, 5.0, f"🟢 Hace {days}d"
        elif age_hours <= 720:
            days = int(age_hours // 24)
            return age_hours, 0.0, f"Hace {days}d"
        else:
            days = int(age_hours // 24)
            return age_hours, -25.0, f"Antigua ({days}d)"

    def analyze(self, opp):
        tags_list = [str(t) for t in opp.get('observed_data', {}).get('tags', [])]
        tags_str = ' '.join(tags_list)
        title = opp.get('title', '')
        desc = opp.get('description', '')
        text = f"{title} {desc} {opp.get('category', '')} {tags_str}"
        lower_text = text.lower()
        lower_title = title.lower()

        # 1. Detect skills & compute fit_score
        detected_skills = []
        raw_fit = 0
        categories_hit = set()

        for s in self.compiled_rules:
            if s['regex'].search(text):
                detected_skills.append(s['keyword'])
                # Extra boost if keyword is right in the title!
                if s['regex'].search(title):
                    raw_fit += s['weight'] * 1.35
                else:
                    raw_fit += s['weight']
                categories_hit.add(s.get('category', 'general'))

        if len(categories_hit) > 1:
            raw_fit += 10

        # Penalize non-tech HR / Legal / Recruiting / Sales / Accounting roles
        non_tech_title_terms = [
            'people & talent', 'human resources', 'hr manager', 'recruiter', 'talent acquisition',
            'account executive', 'tax manager', 'accountant', 'payroll', 'legal counsel', 'nurse',
            'customer support representative', 'collections specialist'
        ]
        if any(nt in lower_title for nt in non_tech_title_terms) or 'non tech' in tags_str.lower():
            raw_fit -= 45

        fit_score = min(100.0, max(0.0, round(float(raw_fit), 1)))

        # 2. Money score
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        opp_type = opp.get('opportunity_type', '')

        if p_min or p_max:
            val = p_max or p_min
            if val >= 5000:
                money_score = 92.0
            elif val >= 1000:
                money_score = 84.0
            elif val >= 200:
                money_score = 75.0
            else:
                money_score = 60.0
        elif opp_type in ['bounty', 'contract', 'freelance']:
            money_score = 65.0
        else:
            money_score = 40.0

        # Penalize US-only / restrictive work authorization if stated
        us_only_signals = ['work legally within the united states', 'us citizens only', 'must reside in the us', 'u.s. citizens only']
        is_us_restricted = any(sig in lower_text for sig in us_only_signals)
        if is_us_restricted:
            fit_score = max(0.0, fit_score - 20.0)
            opp.setdefault('observed_data', {})['stated_location'] = 'US Only (Restringido)'

        for neg in self.signals.get('negative', []):
            if neg['keyword'].lower() in lower_text:
                money_score = max(0.0, money_score - neg['penalty'])
                fit_score = max(0.0, fit_score - 30.0)

        # 3. Trust score
        trust_score = 75.0
        if opp.get('source') in ['Remotive', 'Arbeitnow', 'RemoteOK', 'WeWorkRemotely']:
            trust_score = 85.0
        elif opp.get('source') in ['GitHub Bounties', 'HackerNews']:
            trust_score = 82.0
        if opp.get('organization') and opp.get('organization') not in ['Unknown', 'Confidential', '']:
            trust_score += 8.0
        if 'unpaid' in lower_text or 'crypto token' in lower_text:
            trust_score -= 45.0
        trust_score = min(100.0, max(10.0, trust_score))

        # 4. Reusability & Scalability score
        reusable_keywords = ['automation', 'n8n', 'bot', 'scraping', 'template', 'pipeline', 'workflow', 'tool', 'script', 'agent', 'webhook']
        reusable_matches = [k for k in reusable_keywords if re.search(r'\b' + re.escape(k) + r'\b', lower_text)]
        reusability_score = min(100.0, 30.0 + len(reusable_matches) * 15.0)

        scalability_score = 30.0
        if any(re.search(r'\b' + re.escape(w) + r'\b', lower_text) for w in ['saas', 'product', 'plugin', 'addon', 'template', 'asset', 'package', 'workflow', 'bot', 'agent']):
            scalability_score = 78.0
        if opp_type == 'bounty':
            scalability_score = 60.0

        # 5. Competition score
        if any(s in detected_skills for s in ['n8n', 'roblox', 'blender', 'unity', 'bot', 'scraping']):
            competition_score = 35.0
            est_comp_str = 'BAJA'
        elif any(s in detected_skills for s in ['ai', 'python', 'typescript']):
            competition_score = 60.0
            est_comp_str = 'MEDIA'
        else:
            competition_score = 80.0
            est_comp_str = 'ALTA'

        # 6. Freshness / Recency calculation
        age_hours, freshness_bonus, freshness_label = self.compute_age_and_freshness(opp.get('published_at'))

        # 7. Overall score formula + Freshness Bonus
        comp_inverse = 100.0 - competition_score
        w = self.weights
        base_score = (
            (fit_score * w.get('fit', 0.35)) +
            (money_score * w.get('money', 0.20)) +
            (trust_score * w.get('trust', 0.15)) +
            (reusability_score * w.get('reusability', 0.15)) +
            (comp_inverse * w.get('competition_inverse', 0.15))
        )
        # Apply freshness bonus only if there is at least some technical fit
        if fit_score >= 25.0:
            overall_score = round(min(99.0, max(5.0, base_score + (freshness_bonus * 0.6))), 1)
        else:
            overall_score = round(max(5.0, base_score - 10.0), 1)

        # 8. Estimated Data
        if opp_type == 'bounty':
            est_hours = '4 a 16 horas'
            est_diff = 'MEDIA'
            econ_pot = 'INMEDIATO (Pago por PR)'
        elif opp_type in ['contract', 'freelance']:
            est_hours = '15 a 60 horas'
            est_diff = 'MEDIA'
            econ_pot = 'ALTO (Contrato Directo)'
        elif opp_type == 'full_time':
            est_hours = 'Remoto Continuo'
            est_diff = 'MEDIA_ALTA'
            econ_pot = 'ALTO (Ingreso Recurrente)'
        else:
            est_hours = '20 a 60 horas'
            est_diff = 'MEDIA'
            econ_pot = 'MEDIO_ALTO'

        has_automation_fit = any(k in detected_skills for k in ['n8n', 'automation', 'bot', 'workflow', 'scraping', 'ai'])

        estimated_data = {
            'estimated_hours': est_hours,
            'estimated_difficulty': est_diff,
            'economic_potential': econ_pot,
            'competition_level': est_comp_str,
            'automation_potential': 'SI' if has_automation_fit else ('PARCIAL' if 'python' in detected_skills else 'NO'),
            'age_hours': age_hours,
            'freshness_label': freshness_label,
            'estimation_method': 'RADAR Engine v2 (Fit + Freshness + Monetization)'
        }

        # 9. Decision & Next Action
        if age_hours > 1080:  # Older than 45 days -> discard stale offers
            decision = 'DESCARTAR'
            reasoning = f"Oferta antigua ({freshness_label}). Descartada para priorizar oportunidades frescas."
            next_action = 'Ignorar por antigüedad.'
        elif reusability_score >= 70.0 and scalability_score >= 70.0 and fit_score >= 55.0:
            decision = 'CONSTRUIR_Y_VENDER'
            reasoning = f"[{freshness_label}] Oportunidad ideal para empaquetar ({', '.join(detected_skills[:4])}) y vender como solución/plantilla repetible."
            next_action = 'Construir MVP/plantilla reutilizable y enviar pitch al cliente y negocios similares.'
        elif overall_score >= 70.0 and fit_score >= 45.0:
            decision = 'PRIORIDAD'
            reasoning = f"[{freshness_label}] Alta afinidad técnica ({', '.join(detected_skills[:4])}) con excelente potencial de cierre e ingresos."
            next_action = 'Copiar el Sniper Pitch generado, abrir la oferta original y postular hoy mismo.'
        elif overall_score >= 52.0 and fit_score >= 25.0:
            decision = 'INVESTIGAR'
            reasoning = f"[{freshness_label}] Encaje técnico sólido ({', '.join(detected_skills[:3])}). Vale la pena revisar alcance y enviar propuesta."
            next_action = 'Revisar detalles en el enlace original y enviar propuesta técnica.'
        elif overall_score >= 38.0:
            decision = 'OBSERVAR'
            reasoning = f"[{freshness_label}] Coincidencia parcial o alta competencia."
            next_action = 'Mantener en observación.'
        else:
            decision = 'DESCARTAR'
            reasoning = 'Baja afinidad con nuestro stack principal o restricción geográfica.'
            next_action = 'Archivar.'

        # Deduplicate skills cleanly
        unique_skills = []
        seen_sk = set()
        for sk in detected_skills:
            if sk.lower() not in seen_sk:
                seen_sk.add(sk.lower())
                unique_skills.append(sk)

        opp['skills'] = unique_skills
        opp['fit_score'] = fit_score
        opp['money_score'] = money_score
        opp['difficulty_score'] = 50.0 if est_diff == 'MEDIA' else 70.0
        opp['trust_score'] = trust_score
        opp['reusability_score'] = reusability_score
        opp['scalability_score'] = scalability_score
        opp['competition_score'] = competition_score
        opp['overall_score'] = overall_score
        opp['decision'] = decision
        opp['reasoning'] = reasoning
        opp['next_action'] = next_action
        opp['estimated_data'] = estimated_data

        return opp
