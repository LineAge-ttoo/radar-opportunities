import sqlite3, json
import sys; sys.path.append(r'C:\Radar'); from scripts.analyzers.proposal_generator import TechnicalProposalGenerator
import sys; sys.path.append(r'C:\Radar'); from scripts.analyzers.blueprint_generator import BlueprintGenerator

conn = sqlite3.connect(r'C:\Radar\data\opportunities\radar.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM opportunities WHERE proposal_json IS NULL AND decision IN ('PRIORIDAD', 'INVESTIGAR', 'CONSTRUIR_Y_VENDER');")
rows = cur.fetchall()
print(f"Backfilling proposals for {len(rows)} opportunities...")

for r in rows:
    opp = dict(r)
    opp['skills'] = json.loads(opp.get('skills_json') or '[]')
    pitch = TechnicalProposalGenerator.generate_pitch(opp)
    blueprint = BlueprintGenerator.generate_blueprint(opp) if opp.get('decision') == 'CONSTRUIR_Y_VENDER' else None
    
    cur.execute("""
    UPDATE opportunities 
    SET proposal_json = ?, blueprint_json = ? 
    WHERE opportunity_id = ?;
    """, (
        json.dumps(pitch, ensure_ascii=False),
        json.dumps(blueprint, ensure_ascii=False) if blueprint else None,
        opp['opportunity_id']
    ))

conn.commit()
conn.close()
print("Backfill completed successfully.")

