"""Build the five photo-led, seek-safe itinerary compositions."""
import json
from html import escape as h
from pathlib import Path

P = Path(__file__).resolve().parents[1]
SCENES = json.loads((P / 'scenes.json').read_text())
CREDITS = {
 'kinosaki':'Photo: 663highland · CC BY 2.5 · Wikimedia Commons',
 'amanohashidate':'Photo: brian25_tw · CC BY-SA 2.0 · Wikimedia Commons',
 'tottori':'Photo: Suicasmo · CC BY-SA 4.0 · Wikimedia Commons',
 'kibitsu':'Photo: Reggaeman · CC BY-SA 3.0 · Wikimedia Commons',
 'kurashiki':'Photo: David Monniaux · CC BY-SA 3.0 · Wikimedia Commons',
}
for n in range(5, 10):
 s=SCENES[n-1]; cid=s['id']; image=s['image']
 rows=''.join(f'<div class="row" id="{cid}-row-{i}"><span class="when">{h(a)}</span><span class="what">{h(b)}</span></div>' for i,(a,b) in enumerate(s['items']))
 page=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"></head><body><template>
<link rel="stylesheet" href="../../assets/base.css">
<style>
@font-face{{font-family:GenSekiGothic;src:url('../../assets/fonts/GenSekiGothic2TW-B.otf') format('opentype');font-weight:700}}
#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}
.photo-frame{{left:900px;top:348px;width:934px;height:470px}}
.photo-frame img{{object-position:center}}
.credit{{left:900px;top:829px;width:934px}}
.tagbox{{position:absolute;left:86px;top:351px;width:755px}}
.leadbox{{position:absolute;left:86px;top:426px;width:755px}}
.rows{{position:absolute;left:86px;top:555px;width:755px}}
.row{{padding:15px 0;gap:18px}}
.row .when{{min-width:151px;font-size:27px}}
.row .what{{font-size:29px}}
.source{{bottom:119px}}
</style>
<div id="root" data-composition-id="{cid}" data-duration="16" data-width="1920" data-height="1080">
<div class="scene">
 <p class="eyebrow">{h(s['eyebrow'])}</p><p class="date">{h(s['date'])}</p><div class="rule"></div>
 <p class="day">{h(s['day'])}</p><h1 class="heading" id="{cid}-heading">{h(s['title'])}</h1>
 <div class="tagbox" id="{cid}-tag"><p class="tag">{h(s['tag'])}</p></div>
 <div class="leadbox" id="{cid}-lead"><p class="lead">{h(s['lead'])}</p></div>
 <div class="rows">{rows}</div>
 <figure class="photo-frame" id="{cid}-photo"><img id="{cid}-image" src="../../assets/images/treated/{image}.jpg" alt="{h(s['title'])}，景點參考照片"></figure>
 <p class="credit">{h(CREDITS[image])}</p>
 <p class="footnote">{h(s['note'])}</p><p class="source">{h(s.get('source',''))}</p><p class="page-number">{n:02d} / 12</p>
</div></div>
<script>
(()=>{{
 const C=window.TL.scenes['{cid}'];const D=C.duration;const tl=gsap.timeline({{paused:true}});
 tl.fromTo('#{cid}-heading',{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.8,ease:'power3.out'}},C.title);
 tl.fromTo('#{cid}-tag',{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.7,ease:'power3.out'}},C.enter+0.5);
 tl.fromTo('#{cid}-lead',{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.7,ease:'power3.out'}},C.enter+0.7);
 tl.fromTo('#{cid}-photo',{{x:30,opacity:0}},{{x:0,opacity:1,duration:0.9,ease:'power3.out'}},C.enter+0.2);
 tl.fromTo('#{cid}-image',{{scale:1.03}},{{scale:1.0,duration:D-1,ease:'none'}},C.enter);
 {''.join(f"tl.fromTo('#{cid}-row-{i}',{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.7,ease:'power3.out'}},C.items[{i}]);" for i in range(3))}
 window.__timelines['{cid}']=tl;
}})();
</script></template></body></html>'''
 (P/f'compositions/frames/{n:02d}-{cid}.html').write_text(page)
 print(f'Built {n:02d}-{cid}.html')
