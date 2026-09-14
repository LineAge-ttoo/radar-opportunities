import json
import sqlite3
import uuid
from datetime import datetime

WORKFLOW_FILE = r'C:\Radar\n8n\workflows\RADAR_02_DEMAND_DETECTION.json'
N8N_DB_FILE = r'C:\Radar\n8n\instance\.n8n\database.sqlite'

with open(WORKFLOW_FILE, 'r', encoding='utf-8-sig') as f:
    wf = json.load(f)

workflow_id = "RADAR02DEMAND01"
version_id = str(uuid.uuid4())
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

conn = sqlite3.connect(N8N_DB_FILE)
cur = conn.cursor()

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
    wf['name'],
    0,
    json.dumps(wf['nodes'], ensure_ascii=False),
    json.dumps(wf['connections'], ensure_ascii=False),
    json.dumps(wf['settings'], ensure_ascii=False),
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
    "RADAR Demand Detection Engine v1 - Detección de problemas repetidos",
    None,
    '[]',
    None
))

cur.execute("""
INSERT OR IGNORE INTO shared_workflow (workflowId, projectId, role, createdAt, updatedAt)
VALUES (?, ?, 'workflow:owner', ?, ?)
""", (workflow_id, project_id, now_str, now_str))

conn.commit()
conn.close()
print("RADAR_02 registered successfully in n8n database.")

