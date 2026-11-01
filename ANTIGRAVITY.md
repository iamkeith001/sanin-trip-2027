# 日本山陰・海之京都・山陽旅伴行程決策冊

## 專案目的

這是 2027 年冬季 8 天旅行的私人規劃專案。`trip_discussion.html` 是讓旅伴逐日比較交通、景點、住宿與節奏，並保存討論成果的互動頁面。

## 內容來源與更新原則

- `README.md`、`itinerary.md`、`transportation.md`、`spots.md`、`budget.md` 與 Word 企劃書是行程內容來源；改動前先核對彼此是否一致。
- 不假設全程單一交通方式：每一天的交通由當日討論方案決定；Day 2 為 JR 鐵道安排。
- 候選景點、住宿、交通或營運資訊不得寫成已預訂、已確認或可行；需要保留待查證狀態。
- 外部營運時間、冬季道路與交通時刻表屬時效資訊，正式定案前要查證。

## 網頁與資產

- 主要頁面：`trip_discussion.html`。
- 主視覺放在 `assets/`；新增或替換影像要保留替代文字、預留文字安全區，並在頁面中實際引用後驗證。
- 保持日別導覽、方案卡、討論成果總覽與本機保存功能可用；改動互動程式後至少做語法檢查與重複 ID 檢查。
- 樣式用預先產生的 `assets/tailwind.min.css`（tailwindcss 3.4.17），不再從 CDN 即時產生。HTML 新增 Tailwind class 後要重建：`npx -y tailwindcss@3.4.17 -i input.css -o assets/tailwind.min.css --content trip_discussion.html --minify`（input.css 內容為 `@tailwind base; @tailwind components; @tailwind utilities;`）。
- 每天開頭的「今日重點」卡是手機上的主要閱讀入口；時刻或停止點改動時要同步更新這張卡。插圖用 JPEG（寬 1200 px 左右），不放大型 PNG。

## 隱私與版本管理

- 這是私人旅遊文件；不得加入憑證、付款資料、護照資料或不必要的個人資訊。
- 無明確授權，不建立遠端、不推送、不分享。
