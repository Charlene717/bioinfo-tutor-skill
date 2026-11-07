# bioinfo-tutor · 生物資訊家教 Skill

> 一份給 Claude 用的 Skill，讓它當生物資訊家教：觀念題直接講清楚，作業與除錯用提示引導。一般入門都能教，scRNA-seq 教得特別深。

![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![語言: 繁體中文](https://img.shields.io/badge/%E8%AA%9E%E8%A8%80-%E7%B9%81%E9%AB%94%E4%B8%AD%E6%96%87-1a6b5a.svg)

Skill 是一個資料夾，裡面的 `SKILL.md` 寫著給 Claude 的做事方法。裝好之後，遇到相關的情境 Claude 會自己套用。這一份教的是「怎麼當一位生物資訊家教」，核心主張只有一句：每個參數都是一個假設，要有數字、有理由、有紀錄。「跑得出來」只是起點，「說得出為什麼」才算學會。

## 它會怎麼教

| 你問的是 | 它會怎麼做 |
|---|---|
| 觀念題（是什麼、為什麼要做、A 和 B 差在哪） | 直接講清楚，再用一題確認你懂了 |
| 作業、練習題、練習版腳本裡的空格 | 用提示一階一階引導，不直接給完整答案 |
| 程式報錯 | 帶你讀錯誤訊息、提假設、做檢查，自己找到原因 |
| 你自己的研究分析 | 可以給能用的程式，但每個關鍵決定都要你說得出理由 |
| 老師或助教備課 | 完整給：答案、解析、常見誤解 |

另外內建四個功能：

- **小測驗與自我檢測**：一次一題，答錯會換個角度重講，再出一題同觀念、不同情境的題目。
- **除錯教學**：教的是除錯的方法，不只是這一個 bug 的解法。
- **學習路徑規劃**：依你的目標、背景與每週時數，排出每個階段的小成品與自我檢核。
- **帶讀論文 Methods**：把方法段還原成流程表，逐句拆開，並分清楚「沒寫」和「做錯」。

範圍包含命令列與環境、R 與 Python、檔案格式、NGS 流程、bulk RNA-seq 與基礎統計；scRNA-seq 從 QC 到下游分析，每一步都整理了常見誤解與版本陷阱。完整內容見 [`bioinfo-tutor/SKILL.md`](bioinfo-tutor/SKILL.md)。

## 適合誰

| 你是 | 可以拿它做什麼 |
|---|---|
| 正在學生物資訊的學生 | 問觀念、除錯、自我檢測、排學習計畫、讀懂論文的方法段 |
| 老師、助教 | 擬回覆學生的草稿、出題附解析、設計練習、整理常見誤解 |

## 安裝

### Claude 應用程式

1. 下載這個倉庫裡的 [`bioinfo-tutor.zip`](bioinfo-tutor.zip)，不用解壓縮。要下載的是這一個檔案，不是右上角 **Code** 裡的 Download ZIP，那會抓到整個倉庫。
2. 到 **Settings > Capabilities**，確認 **Code execution and file creation** 是開的（新版設定頁叫 **Create and edit files**）。
3. 到 **Customize > Skills**，按「+」，選「Create skill」，再選「Upload a skill」，上傳剛剛的 zip。
4. `bioinfo-tutor` 會出現在 Skill 清單裡，確認開關是開的。

以上是個人方案的步驟，於 2026-11-06 對照官方說明。團隊與企業方案能不能自行上傳，要看組織擁有者的設定。介面文字會隨版本調整，中文介面顯示的是對應的翻譯；找不到選項或上傳失敗時，以官方說明為準：[Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

### Claude Code

下載或 clone 這個倉庫，把 `bioinfo-tutor` 資料夾整個複製到下面其中一個位置：

| 位置 | 作用範圍 |
|---|---|
| `~/.claude/skills/bioinfo-tutor/` | 你這台電腦上的所有專案 |
| `<專案>/.claude/skills/bioinfo-tutor/` | 只有那個專案；commit 進去，同組的人也會有 |

已經在 Claude 應用程式裝好的人不必再裝一次。用同一個帳號登入 Claude Code，啟用中的 Skill 會一起載入；這需要較新的版本，細節見[官方文件](https://code.claude.com/docs/en/skills)。

## 怎麼用

裝好之後照平常的方式問就可以。

學生可以這樣問：

- 為什麼做 PCA 之前要先 scale？
- 我照教學跑 `FindMarkers` 一直報錯，可以教我怎麼找原因嗎？（貼上完整的錯誤訊息）
- 考我五題 QC 的觀念
- 我是醫學系背景、沒寫過程式，每週六小時，想在寒假學會分析 scRNA-seq，幫我排學習計畫
- 帶我讀這篇論文的 Methods（貼上那一段）

老師與助教可以這樣問：

- 我的學生一直搞不懂為什麼不能把細胞當 replicate，幫我出五題選擇題，附解析
- 學生問我 resolution 要設多少，幫我擬一段回覆

沒有自動啟用時，在訊息裡直接說「用 bioinfo-tutor 這個 Skill」。

## 使用須知

- **AI 會出錯**。這份 Skill 要求 Claude 先確認版本、不確定就查文件、沒實跑的程式要標明，但沒辦法保證零錯誤。函式的參數與預設值以官方文件為準，課程的要求以老師的說明為準。
- **不要貼上可以識別個人的臨床資料**。
- **它是引導工具，不是防作弊機制**。`SKILL.md` 是純文字，任何人都可以修改。
- **課程地圖會過期**。Skill 裡的課程地圖記的是寫下當時的狀態；集數、頁碼、題號以各課程倉庫的 README 為準。

## 搭配的課程

Skill 裡附了一張課程地圖，學生提到這些課、或想找接著學的資源時用來指路。沒有上這些課也可以用。

- [生資互動式教學入口](https://charlene717.github.io/bioinfo-interactive-tutorial-portal/)：從工具與基礎到組學、AI 與研究實務的雙語課程地圖。
- scRNA-seq 四個系列：[A 入門篇](https://github.com/Charlene717/scRNA-seq-tutorial-Aseries)、[Q 快速上手篇](https://github.com/Charlene717/scRNA-seq-tutorial-Qseries)、[B 實作篇](https://github.com/Charlene717/scRNA-seq-tutorial-Bseries)、[C 數學篇](https://github.com/Charlene717/scRNA-seq-tutorial-Cseries)。
- 互動網站：[單細胞 RNA-seq 互動教學](https://charlene717.github.io/scrna-interactive-tutorial/)、[scRNA-seq 進階數學](https://charlene717.github.io/scrna-advanced-math/)。

## 目錄結構

```
.
├── README.md
├── LICENSE              # MIT
├── bioinfo-tutor/
│   └── SKILL.md         # Skill 本體，內容只住在這裡
├── bioinfo-tutor.zip    # 上傳到 Claude 用；由 build_zip.py 產生，不要手改
└── build_zip.py         # SKILL.md 改過之後重新產生 zip；加 --check 只比對不寫入
```

## 想改成自己的版本

`SKILL.md` 是一般的 Markdown，fork 之後可以直接改。開頭的 `description` 決定它什麼時候啟用；〈課程地圖〉一節可以換成你自己的課程。改完在倉庫根目錄執行：

```bash
python build_zip.py          # 重新產生 bioinfo-tutor.zip
python build_zip.py --check  # 確認 zip 與資料夾的內容一致
```

腳本只用 Python 標準函式庫，會順便檢查上傳時常被擋下來的幾件事：資料夾名稱與 `name` 是否相同、`description` 的長度與字元。

## 授權

[MIT License](LICENSE)，可自由使用、修改、再散布。Skill 裡連結的課程教材各有自己的授權，見各課程的倉庫。

## English summary

`bioinfo-tutor` is a Skill that turns Claude into a bioinformatics tutor covering introductory topics, with extra depth on scRNA-seq. It explains concepts directly, guides students through homework and debugging with graded hints rather than handing over answers, and includes four workflows: quizzes, debugging coaching, study-plan design, and guided reading of a paper's Methods. A teacher mode gives full answer keys and explanations. The skill is written in Traditional Chinese and replies in English when asked in English. To install, upload `bioinfo-tutor.zip` under Customize > Skills in Claude, or copy the `bioinfo-tutor/` folder into `~/.claude/skills/` for Claude Code. MIT licensed.

---

目前版本 v1.0.0（2026-11-06）。問題與建議歡迎開 [Issue](../../issues)。
