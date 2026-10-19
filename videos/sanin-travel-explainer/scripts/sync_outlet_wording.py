"""Sync the regenerated Day 7 clause metadata without changing any scene window."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
M=json.loads((P/'audio_meta.json').read_text());v=next(v for v in M['voices'] if v['frame']==9)
tp=P/'timeline.js';T=json.loads(tp.read_text().split('=',1)[1].strip().rstrip(';'));s=T['scenes']['day-seven'];start=s['start']
s['clauses']=[{'at':w['start'],'end':w['end'],'text':w['text']} for w in v['words']];s['items']=[v['words'][i]['start'] for i in [1,2,3,4]]
tp.write_text('window.TL = '+json.dumps(T,ensure_ascii=False,indent=2)+';\n')
p=P/'caption_groups.json';G=json.loads(p.read_text());groups=[g for g in G['groups'] if g['frame']==9];assert len(groups)==len(v['words'])==8
for g,w in zip(groups,v['words']):
 g.update(start=round(start+w['start'],3),end=round(start+w['end']+.12,3),text=w['text'])
 assert len(g['words'])==1
 g['words'][0].update(text=w['text'],start=round(start+w['start'],3),end=round(start+w['end'],3))
p.write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n')
p=P/'compositions/captions.html';text=p.read_text();text,n=re.subn(r'var GROUPS = \[.*?\];',lambda m:'var GROUPS = '+json.dumps(G['groups'],ensure_ascii=False,separators=(',',':'))+';',text,count=1,flags=re.S);assert n==1;p.write_text(text)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
lines=[];offset=0
for voice in M['voices']:
 for w in voice['words']:lines.append(f"{len(lines)+1}\n{stamp(offset+w['start'])} --> {stamp(offset+w['end'])}\n{w['text']}\n")
 offset+=voice['duration_s']
(P/'captions.srt').write_text('\n'.join(lines))
p=P/'STORYBOARD.md';p.write_text(p.read_text().replace('午後 Outlet','午後 outlet 購物').replace('、Outlet 與回館','、outlet 購物與回館'))
print('Day 7 captions + animation cues synced; 94 cues; duration remains',offset)
