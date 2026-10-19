from pathlib import Path
import json,subprocess,sys
P=Path(__file__).resolve().parents[1]
T=json.loads((P/'timeline.js').read_text().split('=',1)[1].strip().rstrip(';'))['scenes']
times=[round(s['start']+max(c['at']+.1,c['end']-.15),3) for s in T.values() for c in s['clauses']]
S=str(Path.home()/'.claude/skills/review-loop/scripts/sheet.py')
mode=sys.argv[1]
vid=P/'renders'/('draft-v2.mp4' if mode=='draft' else '冬日山陰八天七夜_動態解說版.mp4')
subprocess.run([sys.executable,S,'--video',str(vid),'--at',','.join(map(str,times)),'--out',str(P/'boards'/f'{mode}-v2-review'),'--name','clauses'],check=True)
