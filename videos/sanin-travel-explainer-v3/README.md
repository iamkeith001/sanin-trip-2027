# 冬日山陰八天七夜 v3（動態解說片）

依 2026-11-01 逐日查核後的行程重做的解說片。v2 留在 `../sanin-travel-explainer/` 當紀錄，未改動。

- **成片**：`renders/冬日山陰八天七夜_v3.mp4`，1920×1080、約 2 分 48 秒、12 幕、繁中字幕。
- **旁白**：Microsoft Edge `zh-TW-HsiaoChenNeural`，語速 +8%（同 v2）。腳本見 `SCRIPT.md`。
- **圖片**：16 張皆為 AI 生成示意圖（draw 技能，gpt-image-2.5-flare，low，1536×1024），水彩與寫實風混用，不是實景照片（依使用者要求，畫面上不加標示）。prompt 見 `scripts/gen_prompts.json`。
- **配樂與音效**：沿用 v2 的 music bed（裁到片長並淡出）與章節提示音。
- **第 2 幕路線圖**：沿用 v2 的路線圖動畫（旁白相同），只更新查核日期。

## 重建

```bash
/usr/bin/python3 scripts/gen_images.py          # 只補生缺少的圖（需 ~/.openai.env）
/usr/bin/python3 assets/voice/helpers/run_tts.py  # 依 SCRIPT.md 產生旁白
/usr/bin/python3 ~/.claude/skills/motion-explainer-images/scripts/voice_meta.py --project . --pad 0.6 --last-pad 1.8
/usr/bin/python3 scripts/build_v3.py             # timeline、12 幕、字幕、index
/usr/bin/python3 ~/.claude/skills/motion-explainer-images/scripts/subset_fonts.py --project .   # 一定放最後
npx hyperframes check && npx hyperframes render --quality high --output "renders/冬日山陰八天七夜_v3.mp4"
```

`build_v3.py` 會把各幕字型改回完整字型，所以改完內容要重跑 `subset_fonts.py`。完整字型 `assets/fonts/GenSekiGothic2TW-B.otf` 不進版控，用技能的 `fetch_fonts.sh` 取回。

## 內容依據與界線

- 行程、時刻、票價依 `../../itinerary.md` 等文件（2026-11-01 查核，含 2027 當日班表）。
- Day 3 慢遊仍是推薦案、待旅伴拍板；Day 5 砂丘為條件式；晚餐多數未訂位。影片不代表已訂或保證。
