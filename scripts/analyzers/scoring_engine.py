import json
import re
import os
from datetime import datetime

DEFAULT_SCORING_CONFIG = r'C:\Radar\config\scoring\scoring_rules.json'

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

        # Precompile regex for precise boundary matching
        self.compiled_rules = []
        for s in self.skills_rules:
            kw = s['keyword'].strip()
            # Escape regex special chars except if it already has spaces/slashes
            if kw.lower() == '3d':
                pattern = r'\b3d\b'
            elif kw.lower() == 'ai':
                pattern = r'\bai\b|\bartificial intelligence\b|\bllm\b|\bagents?\b'
            elif kw.lower() == 'ui/ux':
                pattern = r'\bui/ux\b|\bui design\b|\bux design\b|\bfigma\b'
            elif kw.lower() in ['bot', 'bots']:
                pattern = r'\bbots?\b'
            elif kw.lower() in ['api', 'apis']:
                pattern = r'\bapis?\b'
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

    def analyze(self, opp):
        tags_str = ' '.join(opp.get('observed_data', {}).get('tags', []))
        text = f"{opp.get('title', '')} {opp.get('description', '')} {opp.get('category', '')} {tags_str}"

        # 1. Detect skills & compute fit_score
        detected_skills = []
        raw_fit = 0
        categories_hit = set()

        for s in self.compiled_rules:
            if s['regex'].search(text):
                detected_skills.append(s['keyword'])
                raw_fit += s['weight']
                categories_hit.add(s.get('category', 'general'))

        # Bonus if multi-discipline
        if len(categories_hit) > 1:
            raw_fit += 10

        fit_score = min(100.0, max(0.0, float(raw_fit)))

        # 2. Money score (observed facts only, honest calculation)
        p_min = opp.get('payment_min')
        p_max = opp.get('payment_max')
        opp_type = opp.get('opportunity_type', '')

        if p_min or p_max:
            val = p_max or p_min
            if val >= 5000:
                money_score = 90.0
            elif val >= 1000:
                money_score = 80.0
            elif val >= 200:
                money_score = 70.0
            else:
                money_score = 50.0
        elif opp_type in ['bounty', 'contract', 'freelance']:
            money_score = 55.0
        else:
            money_score = 30.0

        # Penalize bad signals
        lower_text = text.lower()
        for neg in self.signals.get('negative', []):
            if neg['keyword'].lower() in lower_text:
                money_score = max(0.0, money_score - neg['penalty'])
                fit_score = max(0.0, fit_score - 30.0)

        # 3. Trust score
        trust_score = 70.0
        if opp.get('source') in ['Remotive', 'Arbeitnow']:
            trust_score = 85.0
        if opp.get('organization') and opp.get('organization') not in ['Unknown', 'Confidential', '']:
            trust_score += 10.0
        if 'unpaid' in lower_text or 'crypto token' in lower_text:
            trust_score -= 40.0
        trust_score = min(100.0, max(10.0, trust_score))

        # 4. Reusability & Scalability score
        reusable_keywords = ['automation', 'n8n', 'bot', 'scraping', 'template', 'pipeline', 'workflow', 'tool', 'script']
        reusable_matches = [k for k in reusable_keywords if re.search(r'\b' + re.escape(k) + r'\b', lower_text)]
        reusability_score = min(100.0, 30.0 + len(reusable_matches) * 15.0)

        scalability_score = 30.0
        if any(re.search(r'\b' + re.escape(w) + r'\b', lower_text) for w in ['saas', 'product', 'plugin', 'addon', 'template', 'asset', 'package', 'workflow', 'bot']):
            scalability_score = 75.0
        if opp_type == 'bounty':
            scalability_score = 50.0

        # 5. Competition score
        if any(s in detected_skills for s in ['n8n', 'roblox', 'blender', 'unity', 'bot']):
            competition_score = 40.0
            est_comp_str = 'BAJA'
        elif any(s in detected_skills for s in ['ai', 'python', 'scraping']):
            competition_score = 65.0
            est_comp_str = 'MEDIA'
        else:
            competition_score = 85.0
            est_comp_str = 'ALTA'

        # 6. Overall score formula
        comp_inverse = 100.0 - competition_score
        w = self.weights
        overall_score = round(
            (fit_score * w.get('fit', 0.35)) +
            (money_score * w.get('money', 0.20)) +
            (trust_score * w.get('trust', 0.15)) +
            (reusability_score * w.get('reusability', 0.15)) +
            (comp_inverse * w.get('competition_inverse', 0.15)),
            1
        )

        # 7. Estimated Data
        if opp_type == 'bounty':
            est_hours = '4 a 20 horas'
            est_diff = 'MEDIA'
            econ_pot = 'MEDIO'
        elif opp_type in ['contract', 'freelance']:
            est_hours = '20 a 80 horas'
            est_diff = 'MEDIA_ALTA'
            econ_pot = 'ALTO'
        elif opp_type == 'full_time':
            est_hours = 'Dedicación continua (>160h/mes)'
            est_diff = 'ALTA'
            econ_pot = 'ALTO'
        else:
            est_hours = 'Por definir según alcance'
            est_diff = 'MEDIA'
            econ_pot = 'MEDIO'

        has_automation_fit = any(k in detected_skills for k in ['n8n', 'automation', 'bot', 'workflow', 'scraping'])

        estimated_data = {
            'estimated_hours': est_hours,
            'estimated_difficulty': est_diff,
            'economic_potential': econ_pot,
            'competition_level': est_comp_str,
            'automation_potential': 'SI' if has_automation_fit else ('PARCIAL' if 'python' in detected_skills else 'NO'),
            'estimation_method': 'Heurística técnica de RADAR Engine v1'
        }

        # 8. Decision & Next Action
        if reusability_score >= 70.0 and scalability_score >= 70.0 and fit_score >= 50.0:
            decision = 'CONSTRUIR_Y_VENDER'
            reasoning = f"Fuerte señal de automatización/producto reutilizable ({', '.join(detected_skills[:3])}). Puede empaquetarse y replicarse."
            next_action = 'Analizar requerimientos y empaquetar una solución/plantilla vendible.'
        elif overall_score >= 72.0:
            decision = 'PRIORIDAD'
            reasoning = f"Alta afinidad técnica ({', '.join(detected_skills[:3])}) con buen balance de viabilidad y pago."
            next_action = 'Inspeccionar URL original, verificar requisitos y preparar propuesta técnica personalizada.'
        elif overall_score >= 50.0:
            decision = 'INVESTIGAR'
            reasoning = f"Afinidad prometedora ({', '.join(detected_skills[:2])}). Requiere clarificar términos de contratación o pago."
            next_action = 'Evaluar viabilidad remota o alcance para proponer solución directa.'
        elif overall_score >= 35.0:
            decision = 'OBSERVAR'
            reasoning = 'Coincidencia parcial o demanda estándar con alta competencia. Mantener en radar pasivo.'
            next_action = 'No priorizar acción inmediata.'
        else:
            decision = 'DESCARTAR'
            reasoning = 'Baja afinidad técnica o señales desfavorables.'
            next_action = 'Archivar sin acción.'

        # Update opp dictionary
        opp['skills'] = list(set(detected_skills))
        opp['fit_score'] = fit_score
        opp['money_score'] = money_score
        opp['difficulty_score'] = 50.0 if est_diff == 'MEDIA' else (75.0 if est_diff == 'MEDIA_ALTA' else 30.0)
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
