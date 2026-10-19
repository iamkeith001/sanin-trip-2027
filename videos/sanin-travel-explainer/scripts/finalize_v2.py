from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json
P=Path(__file__).resolve().parents[1]
V=P/'renders/冬日山陰八天七夜_動態解說版.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)]));(P/'final-v2-media.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
T=json.loads((P/'timeline.js').read_text().split('=',1)[1].strip().rstrip(';'))['scenes']
O=P/'boards/final-v2-stills';O.mkdir(exist_ok=True)
canvas=Image.new('RGB',(1920,1560),'#F4F0E7');draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype(str(P/'assets/fonts/GenSekiGothic2TW-B.otf'),23)
labels=['冬日山陰','全程路線與住宿','Day 1 先寄行李','Day 2 轉乘與晚餐','Day 3 看天候慢遊','Day 4 天橋立登高','Day 5 砂丘條件分支','Day 6 長廊短走','Day 7 先看美術館','Day 8 機場緩衝','旅行的三個安排','一起出發']
for i,(name,s) in enumerate(T.items()):
 t=s['start']+s['duration']-.6
 f=O/f'{i+1:02}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(V),'-frames:v','1',str(f)],check=True)
 im=Image.open(f).convert('RGB').resize((640,360));x=i%3*640;y=i//3*390
 canvas.paste(im,(x,y));draw.text((x+15,y+364),labels[i],font=font,fill='#17394A')
canvas.save(P/'boards/旅程總覽_動態解說版.jpg',quality=92)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(V),'-frames:v','1',str(O/'poster.png')],check=True)
p=P/'旅程介紹.html';p.write_text(p.read_text().replace('boards/v2-snapshots/frame-00-at-0s.png','boards/final-v2-stills/poster.png'))
print('media metadata, 12 stills, overview and poster ready')
