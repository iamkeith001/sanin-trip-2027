from pathlib import Path
import re
P=Path(__file__).resolve().parents[1]
for n,f in enumerate(sorted((P/'compositions/frames').glob('*.html'))[2:10],1):
 s=f.read_text()
 if 'class="dayrail"' in s:continue
 css='.dayrail{position:absolute;left:1050px;top:153px;width:784px;height:42px;display:flex;gap:18px;align-items:center;font-size:24px;line-height:1;z-index:5}.dayrail span{width:80px;border-bottom:3px solid var(--line);padding:0 0 9px;color:var(--muted)}.dayrail span.past{border-color:var(--ink)}.dayrail span.today{color:var(--accent);border-color:var(--accent)}'
 s=s.replace('</style>',css+'</style>',1)
 rail='<div class="dayrail" aria-label="八日旅程進度">'+''.join(f'<span class="{"today" if i==n else "past" if i<n else "future"}">DAY {i}</span>' for i in range(1,9))+'</div>'
 pos=s.index('<div class="scene">') if '<div class="scene">' in s else -1
 if pos>=0:s=s[:pos+19]+rail+s[pos+19:]
 else:
  # data-hf-id may decorate the inner scene; inject after its opening tag.
  s=re.sub(r'(<div[^>]*id="root"[^>]*>)',lambda m:m[1]+rail,s,count=1)
 f.write_text(s)
