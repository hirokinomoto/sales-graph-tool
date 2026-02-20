
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

### 3) 仮想環境（.venv）に入る（必須）

このプロジェクトは `.venv` を使う。

#### PowerShell（VSCodeのターミナルがPowerShellのとき）

- ルート（`C:\dev\sales-graph-tool`）で：
  - `.\.venv\Scripts\Activate.ps1`

#### コマンドプロンプト（cmd）のとき

- ルートで：
  - `.\.venv\Scripts\activate`

成功すると、プロンプトの先頭に `(.venv)` が付く。

### 4) VSCodeのPythonが .venv になっているか

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

- 仕様が変わるなら `SPEC.md` / `ssot/決定事項ログ.md` を先に更新してからコード

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

- `ssot/決定事項ログ.md` の末尾に「次：◯◯」と1行だけ残す

---

## 仮想環境の出入り（覚えるのはこれだけ）

### 入る（PowerShell）

- `.\.venv\Scripts\Activate.ps1`

### 入る（cmd）

- `.\.venv\Scripts\activate`

### 抜ける（共通）

- `deactivate`
