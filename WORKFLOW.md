
# 作業ルール（毎回これを見る）

このリポジトリは「自宅PC／訓練校PC」で同じ作業をする前提。
迷子防止のため、作業前〜終了までの流れをここにまとめる。

---

## 作業前にすること（毎回）

### 1) 正しいフォルダを開いているか

- VSCodeで `sales-graph-tool` を開いている（別フォルダを開いてない）

### 2) 最新の状態にする（PCを切り替えるなら必須）

ターミナルで：

- `git pull`

### 3) ターミナルは PowerShell 7 を使う（方針）

このリポジトリでは **PowerShell 7（x64）** に手順を統一する。

VSCodeで PowerShell 7 を開く：

- メニュー：`Terminal` → `New Terminal`
- 右上の `▼`（プロファイル）→ `PowerShell` / `PowerShell 7` を選ぶ

既定にする（おすすめ）：

- `Ctrl + Shift + P` → `Terminal: Select Default Profile` → `PowerShell` / `PowerShell 7`

> 見分け方：プロンプトが `PS C:\...>` なら PowerShell。

### 4) 仮想環境（.venv）に入る（必須）

このプロジェクトは `.venv` を使う。

リポジトリ直下（例：`C:\dev\sales-graph-tool`）で：

```powershell
.\.venv\Scripts\Activate.ps1
```

成功すると、プロンプトの先頭に `(.venv)` が付く。

#### .venv が無い場合（初回だけ）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5) VSCodeのPythonが .venv になっているか

- 右下のPython（Interpreter）が `.venv` を指していること
- 違うとき：
  - `Ctrl + Shift + P` → `Python: Select Interpreter` → `.venv` を選ぶ

---

## 作業中のお約束（事故を防ぐ）

### 1) 1回の作業は小さく

- 目安：1コミット＝1変更（例：CSV選択だけ、グラフ作成だけ、README更新だけ）

### 2) 動作確認してからコミット

- 保存 → 実行 → 期待どおり → コミット

### 3) エラーは“全文”を残す

- スクショより、ターミナルのエラーメッセージ全文が最速で解決できる

### 4) 生成物は原則Gitに入れない

- 出力ファイル（必要になった場合）は `output/` に置き、Git管理しない（必要なら `.gitignore` で除外）

### 5) 仕様変更は先にドキュメント

- 仕様が変わるなら `SPEC.md` を先に更新してからコード
- READMEは発表用の要約（概要・図・実行手順の入口）

---

## 作業終了時にすること（毎回）

### 1) 変更状況チェック

- `git status`

### 2) コミット

- メッセージは「何をしたか」が分かる短文
  - 例：`Add CSV picker` / `Draw bar chart` / `Update docs`

### 3) 同期（Push）※PC切り替えのため最重要

- `git push`
  （VSCodeの「変更の同期」でもOK）

### 4) 次回やることを1行メモ（任意）

おすすめの置き場所（どちらかに統一）：

- READMEの末尾に `Next: ...` を1行追加
- もしくは、この `WORKFLOW.md` の末尾に `Next: ...` を1行追加

---

## 仮想環境の出入り（覚えるのはこれだけ）

### 入る（PowerShell）

```powershell
.\.venv\Scripts\Activate.ps1
```

### 抜ける（共通）

```powershell
deactivate
```
