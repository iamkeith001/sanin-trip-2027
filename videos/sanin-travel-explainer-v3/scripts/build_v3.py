"""Build the v3 itinerary explainer from audio_meta.json.

Writes timeline.js, compositions/frames/*.html, compositions/captions.html, index.html,
caption_groups.json, captions.srt and the trimmed music bed. Re-run after any narration or
content change. Facts follow ../../itinerary.md as reviewed on 2026-11-01.
"""
import json, re, shutil, subprocess
from html import escape as h
from pathlib import Path

P = Path(__file__).resolve().parents[1]
V2 = P.parent / 'sanin-travel-explainer'
META = json.loads((P / 'audio_meta.json').read_text())
VOICES = {v['frame']: v for v in META['voices']}
FONT_URL = "../../assets/fonts/GenSekiGothic2TW-B.otf"

RAIL_DAYS = 8
def rail(today):
    spans = ''.join(
        f'<span class="{"today" if d == today else "past" if d < today else "future"}">DAY {d}</span>'
        for d in range(1, RAIL_DAYS + 1))
    return f'<div class="dayrail" aria-label="八日旅程進度">{spans}</div>'

# rows: (time, text, clause index that reveals it)
DAYS = {
 3: dict(id='day-one', day=1, eyebrow='SAKAIMINATO', date='01.11 MON', title='境港，先寄行李再逛妖怪街',
         tag='已訂：御宿野乃 境港', main='03a-sakaiminato-street', main_kind='p', inset='03b-luggage-desk', inset_at=4,
         rows=[('12:00', '抵達米子機場（IT724）', 0), ('13:40', '機場 7-Eleven 買午餐', 1),
               ('14:11', 'JR 境線 → 14:26 境港', 2), ('14:30', '御宿野乃寄八件到川口屋', 4),
               ('15:35', '水木茂紀念館（16:00 前入館）', 5), ('19:30', '餐後散步點燈的妖怪街', 7)],
         note='停止點｜趕不上 14:11 先打給飯店', note_at=6),
 4: dict(id='day-two', day=2, eyebrow="SAN'IN COAST LINE", date='01.12 TUE', title='輕裝轉乘，抵達城崎',
         tag='已訂：川口屋（含早晚餐）', main='04a-coast-express', main_kind='p', inset='04b-kinosaki-dusk', inset_at=5,
         rows=[('08:05', '境線刷 IC 卡 → 08:56 米子', 1), ('09:00', '米子站領 e5489 特急票', 2),
               ('12:56', '鳥取轉濱風 4 號', 3), ('14:11', '抵達城崎溫泉', 4),
               ('16:00', '外湯一座（一之湯）', 6), ('18:00', '川口屋晚餐', 7)],
         note='每人 ¥6,470（淡季）・12/12 10:00 開賣', note_at=7),
 5: dict(id='day-three', day=3, eyebrow='KINOSAKI ONSEN', date='01.13 WED', title='在城崎，留一整天慢遊',
         tag='推薦方案・待旅伴拍板', main='05a-ropeway', main_kind='p', inset='05b-outdoor-bath', inset_at=4,
         rows=[('10:30', '纜車上山・11:10 下山', 1), ('12:00', '溫泉街海鮮午餐', 2),
               ('13:15', '回房午休約一小時', 3), ('14:30', '外湯一座（御所之湯）', 4),
               ('18:00', '旅館おまかせ会席', 5)],
         note='停止點｜11:10 才能上山就取消纜車', note_at=6),
 6: dict(id='day-four', day=4, eyebrow='AMANOHASHIDATE', date='01.14 THU', title='天橋立，從山上看海之京都',
         tag='已訂：文珠荘（含早晚餐）', main='06a-sandbar-view', main_kind='p', inset=None,
         rows=[('08:58', 'JR → 豐岡轉丹後鐵道', 1), ('11:05', '抵達天橋立，寄放行李', 2),
               ('11:40', '橋立大丸午餐', 4), ('13:00', 'View Land 展望台', 5),
               ('14:30', '智恩寺・松林短走', 7), ('15:30', '入住文珠荘', 8)],
         note='錯過 08:58 → 改 10:34 特急，11:54 到', note_at=8),
 7: dict(id='day-five', day=5, eyebrow='TOTTORI SAND DUNES', date='01.15 FRI', title='鳥取砂丘，是有條件的驚喜',
         tag='條件式：寄妥八件才去砂丘', main='07a-sand-dunes', main_kind='p', inset='07b-train-bento', inset_at=1,
         rows=[('09:34', '丹鐵 → 豐岡 → 城崎 → 鳥取', 0), ('11:56', '車上吃預備的午餐', 2),
               ('14:00', '抵鳥取，先寄妥八件', 3), ('14:40', '砂丘線 → 15:02 砂丘', 4),
               ('15:05', '砂丘短遊約 45 分', 5), ('16:20', '回程巴士 → 觀水庭', 7)],
         note='停止點｜14:30 未到站牌就取消砂丘', note_at=6),
 8: dict(id='day-six', day=6, eyebrow='OKAYAMA · KIBITSU', date='01.16 SAT', title='岡山，走一段吉備津長廊',
         tag='已訂：岡山格蘭比亞（連住 2 晚）', main='08a-shrine-corridor', main_kind='p', inset='08b-streetcar', inset_at=4,
         rows=[('10:02', '超級因幡 4 號 → 11:49 岡山', 0), ('12:25', '寄放八件・站前午餐', 1),
               ('13:52', '桃太郎線 → 吉備津', 2), ('14:25', '參拜，走一段長廊', 3),
               ('16:30', '表町買大統領中辛', 5)],
         note='停止點｜13:40 未到月台就取消吉備津', note_at=5),
 9: dict(id='day-seven', day=7, eyebrow='KURASHIKI', date='01.17 SUN', title='倉敷，把白壁與運河留到最後',
         tag='已選：倉敷散步＋Outlet', main='09a-kurashiki-canal', main_kind='w', inset='09b-museum-facade', inset_at=1,
         rows=[('08:26', 'JR → 08:43 倉敷', 0), ('09:30', '大原美術館（冬季 15:00 閉館）', 1),
               ('11:20', '白壁運河散步・午餐', 2), ('14:30', '三井 Outlet（16:45 集合）', 3),
               ('17:12', 'JR 回岡山・晚餐', 4), ('20:00', '回房整理八件行李', 5)],
         note='退稅品留著可開箱查驗', note_at=5),
 10: dict(id='day-eight', day=8, eyebrow='HOMEWARD BOUND', date='01.18 MON', title='返程，把機場緩衝留足',
         tag='已訂：IT215 15:25 起飛', main='10a-airport-bus', main_kind='w', inset=None,
         rows=[('07:30', '早餐，房內裝箱秤重', 0), ('10:40', '退房，到西口 21 號站牌', 1),
               ('11:10', '機場巴士 → 11:40 機場', 2), ('11:40', '先辦退稅確認', 3),
               ('12:55', '開櫃，託運八件', 4), ('15:25', 'IT215 → 17:30 桃園', 5)],
         note='報到 14:40 截止；飯店退房時間出發前確認', note_at=5),
}
IMG_KIND = {'03b-luggage-desk': 'w', '04b-kinosaki-dusk': 'w', '05b-outdoor-bath': 'w', '07b-train-bento': 'w',
            '08b-streetcar': 'w', '09b-museum-facade': 'p'}

SCENE_IDS = {1: 'opening', 2: 'route', 11: 'practical', 12: 'closing', **{k: v['id'] for k, v in DAYS.items()}}
ORDER = sorted(SCENE_IDS)

# ---------- timeline ----------
starts, t = {}, 0.0
for f in ORDER:
    starts[f] = round(t, 3); t += VOICES[f]['duration_s']
TOTAL = round(t, 2)
TL = {'scenes': {}}
for f in ORDER:
    v = VOICES[f]; d = v['duration_s']
    cl = [{'at': w['start'], 'end': w['end'], 'text': w['text']} for w in v['words']]
    TL['scenes'][SCENE_IDS[f]] = {'start': starts[f], 'duration': d, 'enter': 0.05, 'title': 0.15,
                                  'items': [c['at'] for c in cl[1:]], 'exit': round(d - 0.4, 2), 'clauses': cl}
(P / 'timeline.js').write_text('window.TL = ' + json.dumps(TL, ensure_ascii=False, indent=2) + ';\n')

HEAD = f'''<template>
<link rel="stylesheet" href="../../assets/base.css">
<style>
@font-face{{font-family:GenSekiGothic;src:url('{FONT_URL}') format('opentype');font-weight:700}}
#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}
#root,#root *{{font-family:GenSekiGothic,sans-serif;font-weight:700}}
.dayrail{{position:absolute;left:1050px;top:153px;width:784px;height:42px;display:flex;gap:18px;align-items:center;font-size:24px;line-height:1;z-index:5}}
.dayrail span{{width:80px;border-bottom:3px solid var(--line);padding:0 0 9px;color:var(--muted)}}
.dayrail span.past{{border-color:var(--ink)}}
.dayrail span.today{{color:var(--accent);border-color:var(--accent)}}
'''

def clause_at(f, i):
    return f"C.clauses[{i}].at"

def day_frame(f, s):
    cid = f'{f:02d}-{s["id"]}'
    rows = ''.join(f'<div class="row" id="r{f}-{i}"><span class="when">{h(a)}</span><span class="what">{h(b)}</span></div>'
                   for i, (a, b, _) in enumerate(s['rows']))
    inset = ''
    if s['inset']:
        inset = (f'<figure class="inset" id="i{f}"><img id="ii{f}" src="../../assets/images/treated/{s["inset"]}.jpg" '
                 f'alt="{h(s["title"])}補充示意圖"></figure>')
    row_js = ''.join(
        f"tl.fromTo('#r{f}-{i}',{{y:22,opacity:0}},{{y:0,opacity:1,duration:.6,ease:'power3.out'}},Math.max(.7,{clause_at(f, c)}));"
        for i, (_, _, c) in enumerate(s['rows']))
    inset_js = ''
    if s['inset']:
        inset_js = (f"tl.fromTo('#i{f}',{{opacity:0,scale:.9,rotation:-3}},{{opacity:1,scale:1,rotation:-1.5,duration:.8,ease:'back.out(1.4)'}},{clause_at(f, s['inset_at'])});"
                    f"tl.fromTo('#ii{f}',{{scale:1.08}},{{scale:1,duration:D-{clause_at(f, s['inset_at'])},ease:'none'}},{clause_at(f, s['inset_at'])});")
    return HEAD + f'''.tagbox{{position:absolute;left:86px;top:342px}}
.rows{{position:absolute;left:86px;top:414px;width:748px}}
.scene .row{{padding:10px 0;gap:22px}}.scene .row .when{{min-width:112px;font-size:28px}}.scene .row .what{{font-size:30px}}
.note{{position:absolute;left:86px;top:878px;width:748px;font-size:25px;line-height:1.45;color:var(--accent)}}
.photo-frame{{left:880px;top:342px;width:954px;height:537px;border-radius:6px}}
.inset{{position:absolute;left:1470px;top:640px;width:384px;height:256px;margin:0;overflow:hidden;border:8px solid var(--bg);border-radius:6px;box-shadow:0 18px 40px rgba(23,57,74,.28);background:var(--ink)}}
.inset img{{width:100%;height:100%;object-fit:cover;display:block}}
</style>
<div id="root" data-composition-id="{cid}" data-duration="{VOICES[f]["duration_s"]}" data-width="1920" data-height="1080"><div class="scene">
{rail(s["day"])}
<p class="eyebrow">{h(s["eyebrow"])}</p><p class="date">{h(s["date"])}</p><div class="rule"></div>
<p class="day">DAY {s["day"]}</p><h1 class="heading" id="h{f}">{h(s["title"])}</h1>
<div class="tagbox" id="t{f}"><p class="tag">{h(s["tag"])}</p></div>
<div class="rows">{rows}</div>
<figure class="photo-frame" id="p{f}"><img id="pi{f}" src="../../assets/images/treated/{s["main"]}.jpg" alt="{h(s["title"])}示意圖"></figure>
{inset}
<p class="note" id="n{f}">{h(s["note"])}</p><p class="page-number">{f:02d} / 12</p>
</div></div><script>(()=>{{
const C=window.TL.scenes['{s["id"]}'];const D=C.duration;const tl=gsap.timeline({{paused:true}});
tl.fromTo('#h{f}',{{y:24,opacity:0}},{{y:0,opacity:1,duration:.8,ease:'power3.out'}},C.title);
tl.fromTo('#t{f}',{{y:16,opacity:0}},{{y:0,opacity:1,duration:.6,ease:'power3.out'}},C.enter+.45);
tl.fromTo('#p{f}',{{x:30,opacity:0}},{{x:0,opacity:1,duration:.9,ease:'power3.out'}},C.enter+.2);
tl.fromTo('#pi{f}',{{scale:1.08,xPercent:1.5}},{{scale:1,xPercent:0,duration:D,ease:'none'}},0);
{row_js}
{inset_js}
tl.fromTo('#n{f}',{{opacity:0}},{{opacity:1,duration:.6,ease:'power2.out'}},{clause_at(f, s["note_at"])});
tl.to({{}},{{duration:D}},0);
window.__timelines['{cid}']=tl;
}})();</script></template>
'''

def opening():
    f = 1
    return HEAD + f'''.bg{{position:absolute;inset:0;overflow:hidden;background:var(--ink)}}
.bg img{{width:100%;height:100%;object-fit:cover;display:block}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,40,52,.86) 0%,rgba(17,40,52,.62) 38%,rgba(17,40,52,.05) 68%)}}
.kick{{position:absolute;left:96px;top:150px;color:#F2D3A8;font-size:28px;letter-spacing:6px}}
.big{{position:absolute;left:92px;top:205px;color:#F4F0E7;font-size:132px;line-height:1.12}}
.stamps{{position:absolute;left:96px;top:540px;display:flex;gap:16px}}
.stamps span{{border:2px solid rgba(244,240,231,.7);color:#F4F0E7;font-size:32px;padding:8px 22px;border-radius:999px;background:rgba(17,40,52,.35)}}
.who{{position:absolute;left:96px;top:640px;color:#F4F0E7;font-size:40px}}
.who b{{color:#F2B9A4}}
.route{{position:absolute;left:96px;top:712px;color:#F4F0E7;font-size:40px;display:flex;gap:18px;align-items:baseline}}
.route i{{font-style:normal;color:#F2B9A4}}
.line{{position:absolute;left:96px;top:800px;color:#F4F0E7;font-size:34px}}
</style>
<div id="root" data-composition-id="01-opening" data-duration="{VOICES[f]["duration_s"]}" data-width="1920" data-height="1080"><div class="scene">
<div class="bg"><img id="bgi1" src="../../assets/images/treated/01-opening.jpg" alt="冬季山陰海岸列車水彩示意圖"></div><div class="shade"></div>
<p class="kick" id="k1">2027.01.11 — 01.18</p>
<h1 class="big" id="b1">冬日山陰<br>八天七夜</h1>
<div class="stamps"><span id="s1a">妖怪街</span><span id="s1b">溫泉</span><span id="s1c">白壁運河</span></div>
<p class="who" id="w1"><b>6</b> 人・<b>8</b> 天・冬日旅行</p>
<p class="route"><span id="ra1">米子進</span><i id="rb1">→</i><span id="rc1">岡山出</span></p>
<p class="line" id="l1">把風景和休息，一起排進行程</p>
</div></div><script>(()=>{{
const C=window.TL.scenes['opening'];const D=C.duration;const q=i=>C.clauses[i].at;const tl=gsap.timeline({{paused:true}});
const up=(s,a)=>tl.fromTo(s,{{y:24,opacity:0}},{{y:0,opacity:1,duration:.7,ease:'power3.out'}},a);
tl.fromTo('#bgi1',{{scale:1.1,xPercent:-2}},{{scale:1,xPercent:0,duration:D,ease:'none'}},0);
up('#k1',.2);up('#b1',.35);
up('#s1a',q(1));up('#s1b',q(2));up('#s1c',q(2)+.45);
up('#w1',q(3));up('#ra1',q(4));up('#rb1',q(5)-.15);up('#rc1',q(5));up('#l1',q(6));
tl.to({{}},{{duration:D}},0);
window.__timelines['01-opening']=tl;
}})();</script></template>
'''

def practical():
    f = 11
    cards = [('01', '12/12・12/16 10:00', '搶六人特急指定席', '日本時間（台灣 09:00）。Day 2 超級松風＋濱風、Day 6 超級因幡；e5489 事前受付 12/5、12/9 起', 1),
             ('02', '晚餐多數未訂位', 'Day 1、5、6、7 自行訂位', 'Day 2–4 旅館含晚餐；其他晚餐先訂六人座位', 3),
             ('03', '冬季班次與天候', '出發前再核對一次', 'JR 運行情報、外湯休館表、飯店退房時間；風雪大就減少景點', 4)]
    html = ''.join(f'<div class="card" id="c{i}"><p class="num">{n}</p><p class="big">{h(a)}</p><p class="sub">{h(b)}</p><p class="fine">{h(c)}</p></div>'
                   for i, (n, a, b, c, _) in enumerate(cards))
    js = ''.join(f"tl.fromTo('#c{i}',{{y:30,opacity:0}},{{y:0,opacity:1,duration:.7,ease:'power3.out'}},q({at}));"
                 for i, (*_, at) in enumerate(cards))
    return HEAD + f'''.cards{{position:absolute;left:86px;top:350px;width:1748px;display:grid;grid-template-columns:repeat(3,1fr);gap:34px}}
.card{{background:#FBF8F1;border:2px solid var(--line);border-top:6px solid var(--accent);border-radius:8px;padding:30px 32px;min-height:500px}}
.card .num{{color:var(--accent);font-size:34px;letter-spacing:3px}}
.card .big{{font-size:54px;line-height:1.3;margin-top:18px}}
.card .sub{{font-size:38px;line-height:1.4;margin-top:16px;color:var(--ink)}}
.card .fine{{margin-top:28px;font-size:30px;line-height:1.55}}
</style>
<div id="root" data-composition-id="11-practical" data-duration="{VOICES[f]["duration_s"]}" data-width="1920" data-height="1080"><div class="scene">
<p class="eyebrow">BEFORE WE GO</p><p class="date">2026.11.01 查核</p><div class="rule"></div>
<p class="day">出發前</p><h1 class="heading" id="h11">出發前的三件事</h1>
<div class="cards">{html}</div><p class="page-number">11 / 12</p>
</div></div><script>(()=>{{
const C=window.TL.scenes['practical'];const D=C.duration;const q=i=>C.clauses[i].at;const tl=gsap.timeline({{paused:true}});
tl.fromTo('#h11',{{y:24,opacity:0}},{{y:0,opacity:1,duration:.8,ease:'power3.out'}},C.title);
{js}
tl.to({{}},{{duration:D}},0);
window.__timelines['11-practical']=tl;
}})();</script></template>
'''

def closing():
    f = 12
    return HEAD + f'''.bg{{position:absolute;inset:0;overflow:hidden;background:var(--ink)}}
.bg img{{width:100%;height:100%;object-fit:cover;display:block}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,40,52,.86) 0%,rgba(17,40,52,.55) 42%,rgba(17,40,52,.05) 72%)}}
.stops{{position:absolute;left:96px;top:170px;display:flex;gap:14px;align-items:center;color:#F4F0E7;font-size:34px}}
.stops i{{font-style:normal;color:#F2B9A4}}
.l1,.l2{{position:absolute;left:92px;color:#F4F0E7;font-size:70px;line-height:1.25}}
.l1{{top:300px}}.l2{{top:400px}}
.l2 b{{color:#F2B9A4}}
.ours{{position:absolute;left:96px;top:575px;color:#F2D3A8;font-size:34px;letter-spacing:4px}}
.go{{position:absolute;left:96px;top:650px;color:#F4F0E7;background:var(--accent);font-size:56px;padding:12px 34px;border-radius:6px}}
</style>
<div id="root" data-composition-id="12-closing" data-duration="{VOICES[f]["duration_s"]}" data-width="1920" data-height="1080"><div class="scene">
<div class="bg"><img id="bgi12" src="../../assets/images/treated/12-closing.jpg" alt="六位旅人雪中同行水彩示意圖"></div><div class="shade"></div>
<p class="stops"><span id="st0">境港・妖怪街</span><i id="sa0">→</i><span id="st1">城崎・溫泉</span><i id="sa1">→</i><span id="st2">倉敷・運河</span></p>
<p class="l1" id="cl1">把想看的風景排進來</p>
<p class="l2" id="cl2">也把冬天需要的<b>餘裕</b>留下來</p>
<p class="ours" id="co">我們的八天七夜・2027.01.11 — 01.18</p>
<p class="go" id="cg">準備一起出發</p>
</div></div><script>(()=>{{
const C=window.TL.scenes['closing'];const D=C.duration;const q=i=>C.clauses[i].at;const tl=gsap.timeline({{paused:true}});
const up=(s,a)=>tl.fromTo(s,{{y:22,opacity:0}},{{y:0,opacity:1,duration:.7,ease:'power3.out'}},a);
tl.fromTo('#bgi12',{{scale:1.08,xPercent:2}},{{scale:1,xPercent:0,duration:D,ease:'none'}},0);
up('#st0',Math.max(.3,q(0)));up('#sa0',q(1)-.1);up('#st1',q(1));up('#sa1',q(2)-.1);up('#st2',q(2));
up('#cl1',q(3));up('#cl2',q(4));up('#co',q(5));
tl.fromTo('#cg',{{scale:.85,opacity:0}},{{scale:1,opacity:1,duration:.7,ease:'back.out(1.6)'}},q(6));
tl.to({{}},{{duration:D}},0);
window.__timelines['12-closing']=tl;
}})();</script></template>
'''

FR = P / 'compositions/frames'; FR.mkdir(parents=True, exist_ok=True)
for old in FR.glob('*.html'): old.unlink()
(FR / '01-opening.html').write_text(opening())
route = (V2 / 'compositions/frames/02-route.html').read_text()
route = route.replace("../../assets/fonts/GenSekiGothic2TW-B.subset.otf", FONT_URL)
route = route.replace('2026-10-11 複核', '2026-11-01 查核')
(FR / '02-route.html').write_text(route)
for f, s in DAYS.items():
    (FR / f'{f:02d}-{s["id"]}.html').write_text(day_frame(f, s))
(FR / '11-practical.html').write_text(practical())
(FR / '12-closing.html').write_text(closing())

# ---------- captions ----------
groups, n = [], 0
for f in ORDER:
    for w in VOICES[f]['words']:
        s0 = round(starts[f] + w['start'], 3); e0 = round(starts[f] + w['end'], 3)
        groups.append({'id': f'caption-group-{n}', 'frame': f, 'start': s0, 'end': round(e0 + .12, 3), 'text': w['text'],
                       'words': [{'id': f'caption-word-{n}-0', 'text': w['text'], 'start': s0, 'end': e0}]})
        n += 1
(P / 'caption_groups.json').write_text(json.dumps({'total_duration_s': TOTAL, 'width': 1920, 'height': 1080, 'groups': groups},
                                                   ensure_ascii=False, indent=2))
cap = (V2 / 'compositions/captions.html').read_text()
cap = re.sub(r'var GROUPS = \[.*?\];\n', lambda m: 'var GROUPS = ' + json.dumps(groups, ensure_ascii=False, separators=(',', ':')) + ';\n', cap, count=1, flags=re.S)
cap = re.sub(r'var DURATION = [\d.]+;', f'var DURATION = {TOTAL};', cap, count=1)
cap = cap.replace('GenSekiGothic2TW-B.subset.otf', 'GenSekiGothic2TW-B.otf')
(P / 'compositions/captions.html').write_text(cap)
def srt_t(x):
    ms = int(round(x * 1000)); return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'
(P / 'captions.srt').write_text(''.join(f'{i + 1}\n{srt_t(g["start"])} --> {srt_t(g["end"])}\n{g["text"]}\n\n' for i, g in enumerate(groups)))

# ---------- music bed trimmed with a fade so it ends with the film ----------
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V2 / 'assets/audio/music-bed.wav'), '-t', str(TOTAL),
                '-af', f'afade=t=in:d=1.5,afade=t=out:st={TOTAL - 4:.2f}:d=4', str(P / 'assets/audio/music-bed-v3.wav')], check=True)

# ---------- index ----------
parts = []
for k, f in enumerate(ORDER):
    cid = (FR / f'{f:02d}-{SCENE_IDS[f]}.html').stem
    dur = VOICES[f]['duration_s'] + (0 if f == ORDER[-1] else .5)
    parts.append(f'''      <div id="el-{cid}" class="scene clip" data-composition-id="{cid}" data-composition-src="compositions/frames/{cid}.html"
        data-start="{starts[f]}" data-duration="{round(dur, 3)}" data-track-index="{k % 2}"></div>
      <audio id="el-{cid}-voice" data-audio-group="narration" src="assets/voice/{f:02d}.wav"
        data-start="{starts[f]}" data-duration="{VOICES[f]["speech_s"]}" data-track-index="10" data-volume="1"></audio>
''')
chimes = ''.join(f'''      <audio id="el-sfx-{i}" src="assets/audio/chime.wav" data-start="{round(starts[f] + .1, 2)}" data-duration="1.6" data-track-index="{20 + i}" data-volume="0.25"></audio>
''' for i, f in enumerate([2, 3, 6, 8, 10, 12]))
trans = ''
for a, b in zip(ORDER, ORDER[1:]):
    ca = (FR / f'{a:02d}-{SCENE_IDS[a]}.html').stem; cb = (FR / f'{b:02d}-{SCENE_IDS[b]}.html').stem
    trans += (f'        tl.to("#el-{ca}", {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, {starts[b]});\n'
              f'        tl.fromTo("#el-{cb}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.inOut" }}, {starts[b]});\n')
carve = ('{&quot;enabled&quot;:true,&quot;sources&quot;:[&quot;narration&quot;],&quot;strength&quot;:0.35}')
chain = ('{&quot;version&quot;:1,&quot;nodes&quot;:[{&quot;type&quot;:&quot;peaking&quot;,&quot;id&quot;:&quot;n1&quot;,&quot;params&quot;:{&quot;frequency&quot;:400,&quot;gain&quot;:-3.8,&quot;q&quot;:1.52}},'
         '{&quot;type&quot;:&quot;peaking&quot;,&quot;id&quot;:&quot;n2&quot;,&quot;params&quot;:{&quot;frequency&quot;:1000,&quot;gain&quot;:-5.33,&quot;q&quot;:1.52}},'
         '{&quot;type&quot;:&quot;peaking&quot;,&quot;id&quot;:&quot;n3&quot;,&quot;params&quot;:{&quot;frequency&quot;:1600,&quot;gain&quot;:-7.6,&quot;q&quot;:1.52}}]}')
index = f'''<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #F4F0E7; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      #el-captions {{ background: transparent !important; }}
    </style>
    <link rel="stylesheet" href="assets/base.css"><script src="timeline.js"></script><script src="assets/motion-kit.js"></script>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{''.join(parts)}
      <!-- BGM: v2 music bed, trimmed and faded to this film's length -->
      <audio id="el-bgm" src="assets/audio/music-bed-v3.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="1"
        data-fx-carve="{carve}" data-fx-chain="{chain}"></audio>

      <!-- captions -->
      <div id="el-captions" data-track-kind="captions" class="scene clip" data-composition-id="captions"
        data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2"></div>

      <hf-audio-group id="narration" data-label="中文旁白" data-fx-chain="{{&quot;version&quot;: 1, &quot;nodes&quot;: [{{&quot;type&quot;: &quot;gain&quot;, &quot;id&quot;: &quot;narration-level&quot;, &quot;label&quot;: &quot;Narration +2 dB&quot;, &quot;params&quot;: {{&quot;gain&quot;: 2.0}}}}]}}"></hf-audio-group>
{chimes}    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
      (function () {{ var tl = window.__timelines["main"];
{trans}        tl.to({{}}, {{ duration: {TOTAL} }}, 0);
      }})();
    </script>
  </body>
</html>
'''
(P / 'index.html').write_text(index)
(P / 'scenes.json').write_text(json.dumps({str(k): v for k, v in DAYS.items()}, ensure_ascii=False, indent=1))
print(f'built 12 frames, {len(groups)} caption groups, total {TOTAL}s')
