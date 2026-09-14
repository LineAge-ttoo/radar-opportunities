import json
import os
from datetime import datetime

class RadarPresenter:
    def __init__(self, export_dir=r'C:\Radar\exports'):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def generate_markdown(self, scan_meta, opportunities):
        md_lines = []
        md_lines.append("# RADAR SCAN REPORT")
        md_lines.append(f"**Fecha / Hora:** {scan_meta['started_at']}")
        sources_str = ", ".join(scan_meta.get('sources_consulted', []))
        md_lines.append(f"**Fuentes Consultadas:** {sources_str}")
        md_lines.append(f"**Hallazgos Totales:** {scan_meta['total_found']}")
        md_lines.append(f"- **PRIORIDAD:** {scan_meta['prioridad_count']}")
        md_lines.append(f"- **CONSTRUIR Y VENDER:** {scan_meta['construir_vender_count']}")
        md_lines.append(f"- **INVESTIGAR:** {scan_meta['investigar_count']}")
        md_lines.append(f"- **OBSERVAR:** {scan_meta['observar_count']}")
        md_lines.append(f"- **DESCARTAR:** {scan_meta['descartar_count']}")
        md_lines.append("\n---\n")

        # Group opportunities
        grouped = {
            'CONSTRUIR_Y_VENDER': [],
            'PRIORIDAD': [],
            'INVESTIGAR': [],
            'OBSERVAR': []
        }

        for opp in opportunities:
            dec = opp.get('decision', 'OBSERVAR')
            if dec in grouped:
                grouped[dec].append(opp)

        order = ['CONSTRUIR_Y_VENDER', 'PRIORIDAD', 'INVESTIGAR', 'OBSERVAR']
        for group_name in order:
            items = grouped[group_name]
            if not items:
                continue
            md_lines.append(f"## SECCIÓN: {group_name} ({len(items)} oportunidades)\n")
            for idx, opp in enumerate(items, 1):
                p_min = opp.get('payment_min')
                p_max = opp.get('payment_max')
                curr = opp.get('currency') or ''
                if p_min or p_max:
                    pago_str = f"{curr} {p_min or ''} - {p_max or ''}".strip()
                elif opp.get('observed_data', {}).get('stated_salary'):
                    pago_str = opp['observed_data']['stated_salary']
                else:
                    pago_str = "No publicado / Por negociar"

                est = opp.get('estimated_data', {})
                obs = opp.get('observed_data', {})
                skills_str = ", ".join(opp.get('skills', [])) or "General"

                md_lines.append(f"### {idx}. {opp.get('title', 'Sin título')} | {opp.get('organization', 'Empresa')} [{opp.get('overall_score', 0)} pts]")
                md_lines.append(f"- **Fuente:** {opp.get('source', '')}")
                md_lines.append(f"- **Pago:** {pago_str}")
                md_lines.append(f"- **Score:** {opp.get('overall_score', 0)} / 100 (Fit: {opp.get('fit_score', 0)}, Reusabilidad: {opp.get('reusability_score', 0)})")
                md_lines.append(f"- **Dificultad:** {est.get('estimated_difficulty', 'N/A')}")
                md_lines.append(f"- **Tiempo estimado:** {est.get('estimated_hours', 'N/A')}")
                md_lines.append(f"- **Compatibilidad (Skills):** {skills_str}")
                md_lines.append(f"- **Por qué apareció:** {opp.get('reasoning', '')}")
                md_lines.append(f"- **Qué sabemos (Datos Observados):** Tipo={obs.get('stated_job_type', 'N/A')}, Ubicación={obs.get('stated_location', 'N/A')}, Remoto={'Sí' if opp.get('remote') else 'No'}")
                md_lines.append(f"- **Qué estamos estimando:** Competencia={est.get('competition_level', 'N/A')}, Potencial Económico={est.get('economic_potential', 'N/A')}, Automatizable={est.get('automation_potential', 'N/A')}")
                md_lines.append(f"- **Qué haríamos (Siguiente Acción):** {opp.get('next_action', '')}")
                md_lines.append(f"- **Enlace original:** [{opp.get('source_url', 'Link')}]({opp.get('source_url', '')})\n")

        md_content = "\n".join(md_lines)
        md_file = os.path.join(self.export_dir, 'RADAR_SCAN_LATEST.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return md_file

    def generate_html(self, scan_meta, opportunities):
        html_cards = []
        for opp in opportunities:
            dec = opp.get('decision', 'OBSERVAR')
            if dec == 'DESCARTAR':
                continue

            color_class = {
                'CONSTRUIR_Y_VENDER': 'badge-build',
                'PRIORIDAD': 'badge-priority',
                'INVESTIGAR': 'badge-investigate',
                'OBSERVAR': 'badge-observe'
            }.get(dec, 'badge-observe')

            p_min = opp.get('payment_min')
            p_max = opp.get('payment_max')
            curr = opp.get('currency') or ''
            if p_min or p_max:
                pago_str = f"{curr} {p_min or ''} - {p_max or ''}".strip()
            elif opp.get('observed_data', {}).get('stated_salary'):
                pago_str = opp['observed_data']['stated_salary']
            else:
                pago_str = "No publicado"

            est = opp.get('estimated_data', {})
            obs = opp.get('observed_data', {})
            skills_badges = "".join([f"<span class='skill-pill'>{s}</span>" for s in opp.get('skills', [])])

            card = f"""
            <div class="card card-{dec.lower()}">
                <div class="card-header">
                    <span class="badge {color_class}">{dec.replace('_', ' ')}</span>
                    <span class="score-pill">Score: {opp.get('overall_score', 0)}</span>
                </div>
                <h3 class="card-title">{opp.get('title', 'Sin título')}</h3>
                <div class="card-meta">
                    <strong>{opp.get('organization', 'Empresa')}</strong> | 
                    <span>{opp.get('source', '')}</span> | 
                    <span>{obs.get('stated_location', 'Remoto')}</span>
                </div>
                <div class="pago-box">
                    <strong>Pago:</strong> {pago_str}
                </div>
                <div class="skills-box">
                    {skills_badges}
                </div>
                <div class="analysis-box">
                    <p><strong>Por qué apareció:</strong> {opp.get('reasoning', '')}</p>
                    <p><strong>Qué sabemos:</strong> Tipo={obs.get('stated_job_type', 'N/A')}, Remoto={'Sí' if opp.get('remote') else 'No'}</p>
                    <p><strong>Qué estimamos:</strong> Dificultad={est.get('estimated_difficulty', 'N/A')}, Tiempo={est.get('estimated_hours', 'N/A')}, Potencial={est.get('economic_potential', 'N/A')}</p>
                    <p class="next-action"><strong>Qué haríamos:</strong> {opp.get('next_action', '')}</p>
                </div>
                <a href="{opp.get('source_url', '#')}" target="_blank" rel="noopener noreferrer" class="btn-link">Ver Oportunidad Original ↗</a>
            </div>
            """
            html_cards.append(card)

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RADAR Intelligence Report</title>
    <style>
        :root {{
            --bg: #0d1117;
            --surface: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --text-bright: #f0f6fc;
            --priority: #238636;
            --build: #8957e5;
            --investigate: #1f6feb;
            --observe: #8b949e;
            --accent: #58a6ff;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 16px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: var(--text-bright);
            margin-top: 0;
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--text-bright);
        }}
        .stat-label {{
            font-size: 0.75rem;
            color: var(--text);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge-build {{ background: rgba(137, 87, 229, 0.2); color: #d2a8ff; border: 1px solid #8957e5; }}
        .badge-priority {{ background: rgba(35, 134, 54, 0.2); color: #7ee787; border: 1px solid #238636; }}
        .badge-investigate {{ background: rgba(31, 111, 235, 0.2); color: #79c0ff; border: 1px solid #1f6feb; }}
        .badge-observe {{ background: rgba(139, 148, 158, 0.2); color: #c9d1d9; border: 1px solid #8b949e; }}
        .score-pill {{
            font-size: 0.85rem;
            font-weight: bold;
            color: var(--text-bright);
            background: rgba(255, 255, 255, 0.08);
            padding: 4px 8px;
            border-radius: 6px;
        }}
        .card-title {{
            color: var(--text-bright);
            margin: 0 0 6px 0;
            font-size: 1.2rem;
        }}
        .card-meta {{
            font-size: 0.85rem;
            color: var(--text);
            margin-bottom: 10px;
        }}
        .pago-box {{
            background: rgba(255, 255, 255, 0.04);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            color: #7ee787;
            margin-bottom: 10px;
        }}
        .skills-box {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }}
        .skill-pill {{
            background: rgba(88, 166, 255, 0.15);
            color: #79c0ff;
            border: 1px solid rgba(88, 166, 255, 0.3);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.75rem;
        }}
        .analysis-box {{
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            padding: 10px;
            font-size: 0.85rem;
            line-height: 1.4;
            margin-bottom: 12px;
        }}
        .analysis-box p {{
            margin: 4px 0;
        }}
        .next-action {{
            color: #ffa657;
            font-weight: 500;
        }}
        .btn-link {{
            display: inline-block;
            background: #21262d;
            border: 1px solid var(--border);
            color: var(--accent);
            text-decoration: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .btn-link:hover {{
            background: #30363d;
            border-color: #8b949e;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>RADAR Intelligence Scan</h1>
            <div><strong>Ejecución:</strong> {scan_meta['started_at']}</div>
            <div><strong>Fuentes:</strong> {", ".join(scan_meta.get('sources_consulted', []))}</div>
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-value">{scan_meta['total_found']}</div><div class="stat-label">Total</div></div>
                <div class="stat-card"><div class="stat-value" style="color: #7ee787;">{scan_meta['prioridad_count']}</div><div class="stat-label">Prioridad</div></div>
                <div class="stat-card"><div class="stat-value" style="color: #d2a8ff;">{scan_meta['construir_vender_count']}</div><div class="stat-label">Construir y Vender</div></div>
                <div class="stat-card"><div class="stat-value" style="color: #79c0ff;">{scan_meta['investigar_count']}</div><div class="stat-label">Investigar</div></div>
                <div class="stat-card"><div class="stat-value" style="color: #8b949e;">{scan_meta['observar_count']}</div><div class="stat-label">Observar</div></div>
            </div>
        </header>

        <main>
            {"".join(html_cards)}
        </main>
    </div>
</body>
</html>
"""
        html_file = os.path.join(self.export_dir, 'RADAR_SCAN_LATEST.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return html_file
