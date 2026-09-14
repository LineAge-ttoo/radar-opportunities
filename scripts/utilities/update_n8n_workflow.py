import json
import sqlite3
import uuid
from datetime import datetime

WORKFLOW_FILE = r'C:\Radar\n8n\workflows\RADAR_01_DISCOVERY.json'
N8N_DB_FILE = r'C:\Radar\n8n\instance\.n8n\database.sqlite'

js_code = r"""const payload = $input.first().json;
const jobs = Array.isArray(payload.jobs) ? payload.jobs : [];

const skillsRules = [
  { keyword: 'n8n', weight: 25, regex: /\bn8n\b/i },
  { keyword: 'automation', weight: 20, regex: /\bautomations?\b/i },
  { keyword: 'workflow', weight: 14, regex: /\bworkflows?\b/i },
  { keyword: 'bot', weight: 16, regex: /\bbots?\b/i },
  { keyword: 'scraping', weight: 18, regex: /\bscraping|crawler\b/i },
  { keyword: 'ai', weight: 14, regex: /\bai\b|artificial intelligence|llm|agent/i },
  { keyword: 'python', weight: 18, regex: /\bpython\b/i },
  { keyword: 'javascript', weight: 16, regex: /\bjavascript\b/i },
  { keyword: 'typescript', weight: 16, regex: /\btypescript\b/i },
  { keyword: 'unity', weight: 22, regex: /\bunity\b/i },
  { keyword: 'roblox', weight: 22, regex: /\broblox\b/i },
  { keyword: 'blender', weight: 22, regex: /\bblender\b/i },
  { keyword: '3d', weight: 16, regex: /\b3d\b/i },
  { keyword: 'ui/ux', weight: 15, regex: /\bui\/ux\b|ui design|ux design|figma/i },
  { keyword: 'api', weight: 15, regex: /\bapis?\b/i }
];

function cleanHtml(raw) {
  if (!raw) return '';
  return String(raw)
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
}

function parseSalary(salaryStr) {
  if (!salaryStr) return { min: null, max: null, currency: null };
  const s = String(salaryStr).trim();
  let currency = null;
  if (s.includes('$') || s.toUpperCase().includes('USD')) currency = 'USD';
  else if (s.includes('€') || s.toUpperCase().includes('EUR')) currency = 'EUR';
  else if (s.includes('£') || s.toUpperCase().includes('GBP')) currency = 'GBP';

  const matches = s.match(/(\d+[\d,]*(?:\.\d+)?)\s*(k|K)?/g);
  if (!matches) return { min: null, max: null, currency };

  const nums = [];
  for (const m of matches) {
    const isK = /k$/i.test(m);
    const clean = m.replace(/[kK,]/g, '').trim();
    let val = parseFloat(clean);
    if (!isNaN(val)) {
      if (isK) val *= 1000;
      nums.push(val);
    }
  }
  if (nums.length === 0) return { min: null, max: null, currency };
  return {
    min: Math.min(...nums),
    max: Math.max(...nums),
    currency
  };
}

const results = [];

for (const job of jobs) {
  const cleanDesc = cleanHtml(job.description || '');
  const title = String(job.title || '').trim();
  const fullText = (title + ' ' + (job.category || '') + ' ' + (job.job_type || '') + ' ' + cleanDesc).toLowerCase();

  const detectedSkills = [];
  let rawFit = 0;
  for (const s of skillsRules) {
    if (s.regex.test(fullText)) {
      detectedSkills.push(s.keyword);
      rawFit += s.weight;
    }
  }

  if (detectedSkills.length === 0) continue;

  const fitScore = Math.min(100, Math.max(0, rawFit));
  const salaryParsed = parseSalary(job.salary);

  let moneyScore = 30;
  if (salaryParsed.min || salaryParsed.max) {
    const val = salaryParsed.max || salaryParsed.min;
    if (val >= 5000) moneyScore = 90;
    else if (val >= 1000) moneyScore = 80;
    else moneyScore = 60;
  } else if (['contract', 'freelance'].includes(String(job.job_type || '').toLowerCase())) {
    moneyScore = 55;
  }

  const trustScore = 85;
  const reusableKws = ['automation', 'n8n', 'bot', 'scraping', 'template', 'workflow', 'script'];
  const hasReusable = reusableKws.some(k => fullText.includes(k));
  const reusabilityScore = hasReusable ? 85 : 35;
  const scalabilityScore = (fullText.includes('product') || fullText.includes('saas') || hasReusable) ? 80 : 35;

  let compScore = 70;
  let compLevel = 'MEDIA';
  if (detectedSkills.some(k => ['n8n', 'unity', 'roblox', 'blender', 'bot'].includes(k))) {
    compScore = 40;
    compLevel = 'BAJA';
  }

  const overallScore = Math.round(
    (fitScore * 0.35) +
    (moneyScore * 0.20) +
    (trustScore * 0.15) +
    (reusabilityScore * 0.15) +
    ((100 - compScore) * 0.15)
  );

  let decision = 'OBSERVAR';
  let reasoning = '';
  let nextAction = '';

  if (reusabilityScore >= 70 && scalabilityScore >= 70 && fitScore >= 50) {
    decision = 'CONSTRUIR_Y_VENDER';
    reasoning = 'Oportunidad con componente de automatizacion y producto reutilizable (' + detectedSkills.slice(0, 3).join(', ') + ').';
    nextAction = 'Disenar micro-herramienta o plantilla de automatizacion empaquetada.';
  } else if (overallScore >= 72) {
    decision = 'PRIORIDAD';
    reasoning = 'Alta afinidad tecnica (' + detectedSkills.slice(0, 3).join(', ') + ') con propuesta viable y buena compensacion.';
    nextAction = 'Revisar URL original y preparar propuesta tecnica enfocada en resultados.';
  } else if (overallScore >= 50) {
    decision = 'INVESTIGAR';
    reasoning = 'Afinidad prometedora (' + detectedSkills.slice(0, 2).join(', ') + '). Validar condiciones y alcance.';
    nextAction = 'Evaluar terminos especificos y requerimientos tecnicos en la oferta.';
  } else {
    decision = 'OBSERVAR';
    reasoning = 'Coincidencia parcial en tecnologia general. Mantener en monitoreo.';
    nextAction = 'No priorizar accion inmediata.';
  }

  results.push({
    opportunity_id: 'remotive_' + (job.id || Math.random().toString(36).substr(2, 9)),
    source: 'Remotive',
    source_url: job.url || '',
    discovered_at: new Date().toISOString(),
    published_at: job.publication_date || null,
    title: title,
    organization: String(job.company_name || '').trim(),
    category: job.category || 'Software Development',
    opportunity_type: job.job_type || 'contract',
    payment_min: salaryParsed.min,
    payment_max: salaryParsed.max,
    currency: salaryParsed.currency,
    location: job.candidate_required_location || 'Worldwide',
    remote: true,
    skills: [...new Set(detectedSkills)],
    observed_data: {
      stated_salary: job.salary || null,
      stated_location: job.candidate_required_location || null,
      stated_job_type: job.job_type || null,
      tags: job.tags || []
    },
    estimated_data: {
      estimated_hours: job.job_type === 'full_time' ? 'Dedicacion continua (>160h/mes)' : '20 a 80 horas',
      estimated_difficulty: fitScore > 70 ? 'MEDIA' : 'ALTA',
      economic_potential: moneyScore > 70 ? 'ALTO' : 'MEDIO',
      competition_level: compLevel,
      automation_potential: hasReusable ? 'SI' : 'PARCIAL'
    },
    fit_score: fitScore,
    money_score: moneyScore,
    difficulty_score: 50,
    trust_score: trustScore,
    reusability_score: reusabilityScore,
    scalability_score: scalabilityScore,
    competition_score: compScore,
    overall_score: overallScore,
    decision: decision,
    reasoning: reasoning,
    next_action: nextAction
  });
}

results.sort((a, b) => b.overall_score - a.overall_score);

return results.map(r => ({ json: r }));
"""

workflow_obj = {
    "name": "RADAR_01_DISCOVERY",
    "nodes": [
        {
            "parameters": {},
            "id": "0f128c56-b043-4b54-b157-001000000001",
            "name": "ESCANEAR AHORA",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [0, 0]
        },
        {
            "parameters": {
                "url": "https://remotive.com/api/remote-jobs",
                "options": {
                    "timeout": 30000
                }
            },
            "id": "0f128c56-b043-4b54-b157-001000000002",
            "name": "DESCARGAR REMOTIVE",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [260, 0]
        },
        {
            "parameters": {
                "jsCode": js_code
            },
            "id": "0f128c56-b043-4b54-b157-001000000003",
            "name": "MOTOR RADAR NORMALIZADOR Y SCORING",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [540, 0]
        }
    ],
    "connections": {
        "ESCANEAR AHORA": {
            "main": [
                [
                    {
                        "node": "DESCARGAR REMOTIVE",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "DESCARGAR REMOTIVE": {
            "main": [
                [
                    {
                        "node": "MOTOR RADAR NORMALIZADOR Y SCORING",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "pinData": {},
    "settings": {
        "executionOrder": "v1"
    },
    "active": False,
    "tags": []
}

# 1. Write file
with open(WORKFLOW_FILE, 'w', encoding='utf-8') as f:
    json.dump(workflow_obj, f, ensure_ascii=False, indent=2)
print("Updated workflow saved to:", WORKFLOW_FILE)

# 2. Insert or update in n8n database
workflow_id = "RADAR01DISCOV01"
version_id = str(uuid.uuid4())
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

conn = sqlite3.connect(N8N_DB_FILE)
cur = conn.cursor()

# Check project ID
cur.execute("SELECT id FROM project WHERE type = 'personal';")
row = cur.fetchone()
project_id = row[0] if row else "rzdr6xOJBIeOqyRw"

cur.execute("""
INSERT INTO workflow_entity (
    id, name, active, nodes, connections, settings, staticData, pinData,
    versionId, triggerCount, meta, parentFolderId, createdAt, updatedAt,
    isArchived, versionCounter, description, activeVersionId, nodeGroups, sourceWorkflowId
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    name = excluded.name,
    nodes = excluded.nodes,
    connections = excluded.connections,
    settings = excluded.settings,
    versionId = excluded.versionId,
    updatedAt = excluded.updatedAt
""", (
    workflow_id,
    workflow_obj['name'],
    0,
    json.dumps(workflow_obj['nodes'], ensure_ascii=False),
    json.dumps(workflow_obj['connections'], ensure_ascii=False),
    json.dumps(workflow_obj['settings'], ensure_ascii=False),
    None,
    '{}',
    version_id,
    0,
    '{}',
    None,
    now_str,
    now_str,
    0,
    1,
    "RADAR Discovery Engine v1 - Escaneo de oportunidades remotas",
    None,
    '[]',
    None
))

# Ensure shared_workflow entry
cur.execute("""
INSERT OR IGNORE INTO shared_workflow (workflowId, projectId, role, createdAt, updatedAt)
VALUES (?, ?, 'workflow:owner', ?, ?)
""", (workflow_id, project_id, now_str, now_str))

conn.commit()
conn.close()
print("Workflow successfully registered into n8n SQLite database with ID:", workflow_id)
