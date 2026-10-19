from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
m=json.loads((P/'final-v2-media.json').read_text());v=next(s for s in m['streams'] if s['codec_type']=='video');a=next(s for s in m['streams'] if s['codec_type']=='audio')
sec=m['format']['duration'];sz=int(m['format']['size'])
log=(P/'final-v2-loudness.log').read_text();tail=log.rsplit('Summary:',1)[-1];lufs=re.search(r'I:\s+([-\d.]+) LUFS',tail);peak=re.search(r'Peak:\s+([-\d.]+) dBFS',tail)
p=P/'QA.md';s=p.read_text().split('\n## 動態解說改版（V2）')[0]
s+=f'''
## 動態解說改版（V2）

- 正式影片：renders/冬日山陰八天七夜_動態解說版.mp4。
- {sec} 秒，{v['width']}×{v['height']}，{v['r_frame_rate']} fps，{v['codec_name']}／{v['pix_fmt']}；{a['codec_name']}、{a['sample_rate']} Hz、{a['channels']} 聲道。
- 檔案：{sz:,} bytes（{sz/1048576:.1f} MiB）。
- 響度：{lufs[1] if lufs else '見 log'} LUFS；true peak {peak[1] if peak else '見 log'} dBFS。
- CLI 更新至 0.8.174；check-report-v2.json 全項無錯誤，唯一警告為主組裝檔長度建議。
- 全程列車真實移動方向、抵站高亮、七晚住宿連動；每天加入 DAY 1–8 導覽列。
- 六位旅伴與八件行李分流、轉乘午餐停留、單一外湯到回館更衣與 18:00 晚餐節點。
- 城崎與砂丘採替代分支，保留推薦／條件成立狀態；天橋立先寄物再登高。
- 吉備津以透視木構長廊延伸、全長／短走括號分開；倉敷 15:00 冬季閉館線與上午安排連動。
- 返程依序呈現早餐、退房、較早巴士、報到與 15:25 航班；不新增未確認的巴士時間。
- 修正數字起頭 DOM ID 導致動畫選擇器失效、寄送線 dash 衝突、照片署名與重點文字距離、返程行李標籤與結果重疊。
- 草稿與正式影片皆於 94 個旁白子句節點擷取並逐張查看 12 張 contact sheets；另看分支與移動物件的中途、抵達 proof snapshots。
- 正式成片總覽：boards/旅程總覽_動態解說版.jpg；完整逐句畫面：boards/final-v2-review/clauses-1.png～clauses-12.png。
- 原旁白、字幕、配樂與景點照片來源維持；V1 影片及 versions/v1 原始檔保留。播放頁已改用 V2 影片。
'''
p.write_text(s)
print(f'duration={sec}s; bytes={sz:,}; loudness={lufs[1] if lufs else None}; peak={peak[1] if peak else None}')
