from pathlib import Path
P=Path(__file__).resolve().parents[1]
f=P/'compositions/frames/01-opening.html';s=f.read_text()
s=s.replace('top:640px;width:890px','top:600px;width:890px').replace('top:790px;width:850px;height:35px','top:790px;width:850px;height:35px')
a=s.index('  <svg data-hf-id="hf-oz62"');b=s.index('  <p data-hf-id="hf-0sra"',a)
s=s[:a]+'''  <div id="op-stories" style="position:absolute;left:86px;top:710px;width:890px;height:126px;display:flex;gap:28px">
   <div id="op-yokai" class="op-story"><svg viewBox="0 0 92 66"><path d="M20 56V17H72V56M17 17H75M26 9H66M35 33H57M35 42H57"/><circle cx="46" cy="22" r="4"/></svg><span>妖怪街</span></div>
   <div id="op-onsen" class="op-story"><svg viewBox="0 0 92 66"><path d="M11 37Q11 61 46 61Q81 61 81 37M11 37Q46 49 81 37"/><g id="op-steam"><path d="M29 31C17 20 39 17 28 6M47 31C35 20 57 17 46 6M65 31C53 20 75 17 64 6"/></g></svg><span>城崎溫泉</span></div>
   <div id="op-canal" class="op-story"><svg viewBox="0 0 92 66"><path d="M7 37Q46 2 85 37M7 37H85M20 37V50M72 37V50"/><g id="op-water"><path d="M5 55Q19 47 33 55T61 55T89 55M5 63Q19 55 33 63T61 63T89 63"/></g></svg><span>白壁運河</span></div>
  </div>
''' +s[b:]
s=s.replace('</style>','.op-story{width:278px;display:flex;align-items:center;gap:14px;border-top:2px solid var(--line);padding-top:15px;font-size:32px}.op-story svg{width:84px;height:74px;fill:none;stroke:var(--ink);stroke-width:3;stroke-linecap:round}#op-yokai svg,#op-onsen svg,#op-canal svg{overflow:visible}</style>',1)
a=s.index("const line=document.getElementById('opening-route-line')");b=s.index("window.__timelines['01-opening']",a)
s=s[:a]+'''tl.fromTo('#opening-photo img',{scale:1.015},{scale:1.085,duration:D,ease:'none'},0);
tl.fromTo('.opening-numbers .opening-stat',{opacity:0,y:24},{opacity:1,y:0,duration:.8,stagger:.22,ease:'expo.out'},T.clauses[3].at);
['#op-yokai','#op-onsen','#op-canal'].forEach((sel,i)=>tl.fromTo(sel,{opacity:.18,y:12},{opacity:1,y:0,duration:.7,ease:'expo.out'},T.clauses[Math.min(i+1,2)].at+i*.24));
tl.fromTo('#op-steam',{y:5,opacity:.3},{y:-4,opacity:1,duration:1.2,ease:'power2.inOut',repeat:1,yoyo:true},T.clauses[2].at);
tl.fromTo('#op-water',{x:-4},{x:4,duration:2.3,ease:'power2.inOut',repeat:1,yoyo:true},T.clauses[2].at+.5);
''' +s[b:];f.write_text(s)
# Causal summary: a process, not checkmarks that could imply confirmations.
f=P/'compositions/frames/11-practical.html'
f.write_text('''<template>
<link rel="stylesheet" href="../../assets/base.css">
<style>
@font-face{font-family:GenSekiGothic;src:url('../../assets/fonts/GenSekiGothic2TW-B.otf');font-weight:700;font-display:block}
#root{position:absolute;inset:0;width:100%;height:100%}
.pr2-row{position:absolute;left:100px;width:1735px;height:155px;border-top:2px solid var(--line);display:flex;align-items:center;gap:32px}.pr2-num{font-size:56px;color:var(--accent);width:100px}.pr2-cell{width:440px;font-size:38px;line-height:1.5}.pr2-small{display:block;font-size:26px;color:var(--muted)}.pr2-arrow{width:100px;height:50px;overflow:visible;color:var(--accent)}.pr2-result{font-size:37px;width:470px}.pr2-route{fill:none;stroke:var(--line);stroke-width:4}.pr2-token{fill:var(--accent)}.pr2-note{position:absolute;left:233px;top:839px;font-size:29px;color:var(--muted)}
</style>
<div id="root" data-composition-id="11-practical" data-duration="16.78" data-width="1920" data-height="1080"><div class="scene">
<div class="eyebrow">BEFORE WE GO</div><div class="date">行前再確認</div><div class="rule"></div><div class="day">TRAVEL LOGIC</div><h1 id="pr2-title" class="heading">三個安排，換來旅途的餘裕</h1>
<div id="pr2-luggage" class="pr2-row" style="top:350px"><span class="pr2-num">01</span><div class="pr2-cell">八件大行李<span class="pr2-small">Day 1 先交寄川口屋</span></div><svg class="pr2-arrow" viewBox="0 0 100 50"><path id="pr2-p1" class="pr2-route" d="M0 25H95L80 10M95 25L80 40"/><rect id="pr2-bag" class="pr2-token" x="0" y="10" width="24" height="30" rx="3"/></svg><div id="pr2-r1" class="pr2-result">隔天輕裝轉乘<span class="pr2-small">後續寄送仍待決定</span></div></div>
<div id="pr2-meal" class="pr2-row" style="top:510px"><span class="pr2-num">02</span><div class="pr2-cell">含餐的住宿<span class="pr2-small">城崎、文珠荘依訂房用餐</span></div><svg class="pr2-arrow" viewBox="0 0 100 50"><path id="pr2-p2" class="pr2-route" d="M0 25H95L80 10M95 25L80 40"/><circle id="pr2-meal-token" class="pr2-token" cx="0" cy="25" r="10"/></svg><div id="pr2-r2" class="pr2-result">保留回館與用餐時間<span class="pr2-small">其餘餐廳多數尚未訂位</span></div></div>
<div id="pr2-winter" class="pr2-row" style="top:670px"><span class="pr2-num">03</span><div class="pr2-cell">冬季交通與天候<span class="pr2-small">出發前核對班次、六人座位</span></div><svg class="pr2-arrow" viewBox="0 0 100 50"><path id="pr2-p3" class="pr2-route" d="M0 25H95L80 10M95 25L80 40"/><circle id="pr2-winter-token" class="pr2-token" cx="0" cy="25" r="10"/></svg><div id="pr2-r3" class="pr2-result">風雪大，就減少景點<span class="pr2-small">把休息與返程緩衝留下來</span></div></div>
<p id="pr2-note" class="pr2-note">先處理限制，再決定景點的多寡。</p>
<p class="footnote">已訂住宿與候選餐廳，分開看待。</p><p class="source">依專案行程、交通與訂房文件整理 · 官方資訊查核 2026-10-19</p><div class="page-number">11 / 12</div>
</div></div>
<script>
(()=>{const T=window.TL.scenes.practical;const c=T.clauses;const tl=gsap.timeline({paused:true});
tl.fromTo('#pr2-title',{opacity:0,y:20},{opacity:1,y:0,duration:.8,ease:'expo.out'},T.title);
const rows=['luggage','meal','winter'],ats=[c[1].at,c[3].at,c[5].at],res=[c[1].at+1,c[3].at+1,c[7].at];
rows.forEach((n,i)=>{tl.fromTo('#pr2-'+n,{opacity:.15,y:18},{opacity:1,y:0,duration:.75,ease:'expo.out'},ats[i]);tl.fromTo('#pr2-r'+(i+1),{opacity:0,x:-15},{opacity:1,x:0,duration:.7,ease:'expo.out'},res[i]);});
['#pr2-bag','#pr2-meal-token','#pr2-winter-token'].forEach((s,i)=>tl.fromTo(s,{x:0},{x:77,duration:.95,ease:'power2.inOut'},ats[i]+.2));
tl.fromTo('#pr2-note',{opacity:0,y:8},{opacity:1,y:0,duration:.6,ease:'expo.out'},c[7].at);
window.__timelines['11-practical']=tl;})();
</script></template>
''')
# Closing: highlights are tied to the named experiences, then a protected-time result.
f=P/'compositions/frames/12-closing.html';s=f.read_text()
s=s.replace('top:490px;font-size:35px','top:490px;font-size:35px')
a=s.index(' <p data-hf-id="hf-ddci"');b=s.index(' <p data-hf-id="hf-uur2"',a)
s=s[:a]+''' <div class="cl2-flow" style="position:absolute;left:1050px;top:492px;width:784px;height:134px;display:flex;gap:20px">
 <div id="cl2-1" class="cl2-stop">境港<span>妖怪街</span></div><div class="cl2-arrow">→</div><div id="cl2-2" class="cl2-stop">城崎<span>溫泉連住</span></div><div class="cl2-arrow">→</div><div id="cl2-3" class="cl2-stop">倉敷<span>白壁運河</span></div>
 </div>
 <div id="cl2-room" style="position:absolute;left:1050px;top:675px;width:784px;height:72px;border-top:3px solid var(--line);padding-top:20px;font-size:34px"><span id="cl2-scenery">想看的風景</span><span id="cl2-plus" style="margin:0 24px;color:var(--accent)">＋</span><span id="cl2-buffer">冬天的餘裕</span></div>
 <p class="closing-invite" style="top:761px;border:0;padding-top:0;font-size:35px">準備，一起出發。</p>
''' +s[b:]
s=s.replace('</style>','.cl2-stop{width:212px;font-size:35px;line-height:1.5;border-bottom:3px solid var(--line);padding-bottom:12px}.cl2-stop span{display:block;font-size:27px;color:var(--muted)}.cl2-arrow{font-size:32px;color:var(--muted);padding-top:25px}</style>',1)
s=s.replace("tl.fromTo('.closing-lead',{y:24,opacity:0},{y:0,opacity:1,duration:.85,ease:'expo.out'},T.items[0]);","""['#cl2-1','#cl2-2','#cl2-3'].forEach((sel,i)=>{tl.fromTo(sel,{opacity:.2,y:14},{opacity:1,y:0,duration:.75,ease:'expo.out'},T.clauses[i].at);tl.fromTo(sel,{borderBottomColor:'var(--line)'},{borderBottomColor:'var(--accent)',duration:.5},T.clauses[i].at+.2);});
tl.fromTo('#cl2-scenery',{opacity:0,y:12},{opacity:1,y:0,duration:.7,ease:'expo.out'},T.clauses[3].at);
tl.fromTo('#cl2-plus,#cl2-buffer',{opacity:0,y:12},{opacity:1,y:0,duration:.7,ease:'expo.out'},T.clauses[4].at);""")
s=s.replace("T.items[2]);","T.clauses[6].at);")
f.write_text(s)
