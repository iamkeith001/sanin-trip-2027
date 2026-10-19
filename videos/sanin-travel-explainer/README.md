# 冬日，沿著山陰慢行

2027 山陰・海之京都・山陽八天七夜旅程介紹。六位旅伴，2027/1/11–1/18。

## 播放

- `renders/冬日山陰八天七夜_動態解說版.mp4`：新版正式影片，1920×1080、30fps，約 3 分 8 秒。
- `旅程介紹.html`：本機播放頁，可暫停、拖曳、切換速度、跳至各天與全螢幕。請保留同目錄的 renders、assets、boards 資料夾。
- `captions.srt`：繁體中文字幕；MP4 內也已燒入字幕。
- `boards/旅程總覽_動態解說版.jpg`：新版正式成片各幕總覽。
- `renders/冬日山陰八天七夜.mp4`：第一版保留供比較。

## 資料與編輯

- `SOURCES.md`：官方查核來源、既有行程與未確認項目的界線。
- `assets/images/web/CREDITS.md`：五張 Wikimedia Commons 景點照片的作者與授權。
- `STORYBOARD.md`、`SCRIPT.md`：分鏡與旁白稿。
- `timeline.js`、`scenes.json`、`compositions/frames/`：可繼續修改的原始動畫。
- `index.html`：HyperFrames 主 composition；以 HyperFrames Studio 開啟。直接用瀏覽器開此檔不會自行載入子 composition，日常播放請開「旅程介紹.html」。
- `QA.md`：視覺、字幕、音量與播放檢查紀錄。

## 本機編輯預覽

```sh
npm run dev
```

## 內容狀態

原始旅遊文件維持原狀，本片產出集中在此子資料夾。Day 3 為推薦方案，Day 5 砂丘為條件式短遊；2027 冬季班次、餐廳訂位及寄物容量仍須再核。照片非本次旅行拍攝，不保證積雪。

## 採用技能

主要使用個人 claude-skills 的 motion-explainer-images、motion-design、review-loop，並採用 HyperFrames／faceless-explainer 的組裝與輸出流程。配樂和轉場聲為本專案程式合成原創素材；中文旁白為台灣女聲 TTS。

## 動態解說改版

每一天新增進度列與有因果的動作：全程實際移動與住宿夜數連動、六人八件行李分流、轉乘午餐停點、天候替代路線、先寄物再登高、砂丘條件閘門、吉備津長廊短走、美術館上午與 15:00 界線，以及機場報到緩衝。旁白、配樂、字幕、照片授權與約 3 分 8 秒長度維持一致。

HyperFrames CLI 已由 0.8.171 更新至 0.8.174。動畫使用可重現的 GSAP paused timeline，節拍依既有旁白子句同步。

## 版本控制

本次 commit 包含已檢查的 V2 MP4、播放頁、動畫原始檔、必要圖片／字型／聲音素材，以及精簡成片檢查圖。node_modules、草稿、工作快取與第一版大型影片保留在本機，不進版控。
