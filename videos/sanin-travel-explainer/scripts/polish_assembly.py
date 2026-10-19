"""Offline assets, shared clock, and a calm Traditional Chinese caption band.
Run after assembly/theme/transition injection and before subsetting/check.
"""
from pathlib import Path
import re
P=Path(__file__).resolve().parents[1]
root=P/'index.html'
text=root.read_text().replace('https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js','assets/gsap.min.js')
text=text.replace('lang="en"','lang="zh-Hant"')
if 'src="timeline.js"' not in text:
 text=text.replace('</head>','<link rel="stylesheet" href="assets/base.css"><script src="timeline.js"></script>\n</head>')
text=text.replace('Newsreader','GenSekiGothic').replace('Hanken Grotesk','GenSekiGothic')
root.write_text(text)

cap=P/'compositions/captions.html';t=cap.read_text()
if 'caption-band-travel' not in t:
 t=t.replace('</template>','''<style id="caption-band-travel">
 #captions-root{width:100%;height:100%;font-family:GenSekiGothic,sans-serif}
 .caption-stage{top:970px!important;height:110px!important;background:#17394A}
 .caption-pill{max-width:94%!important;padding:5px 30px!important;background:transparent!important;background-image:none!important;border:0!important;box-shadow:none!important}
 .caption-line{font-family:GenSekiGothic,sans-serif!important;font-size:38px!important;font-weight:700!important;line-height:1.4!important;letter-spacing:0!important;gap:0 12px!important}
 .caption-word,.caption-word.is-active,.caption-word.is-spoken{color:#F4F0E7!important;background:transparent!important;box-shadow:none!important;font-style:normal!important}
 </style></template>''')
t=t.replace('https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js','assets/gsap.min.js').replace('Newsreader','GenSekiGothic').replace('Hanken Grotesk','GenSekiGothic')
cap.write_text(t)

for f in sorted((P/'compositions/frames').glob('*.html')):
 s=f.read_text()
 # The theme helper authors project-root font URLs; a subcomposition's own
 # file-relative assets keep static lint and compiled asset rebasing in agreement.
 s=re.sub(r'(?<![./])assets/fonts/', '../../assets/fonts/',s)
 f.write_text(s)
print('Offline playback, shared clock, and caption band ready.')
