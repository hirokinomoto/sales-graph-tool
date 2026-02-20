
# sales-graph-tool

売上CSVを読み込み、カテゴリ別売上合計を棒グラフで表示する最小ツール（Tkinter + pandas + matplotlib）です。

## できること（最小）

- CSVを選択して読み込む
- `category` ごとに `amount` を合計
- 棒グラフを画面表示する（プレビュー）

> ※ファイル出力（PNG保存など）は今回の最小版では扱いません。

---

## 必要なもの

- Windows
- Python（.venv 利用）
- 依存パッケージ：`pandas`, `matplotlib`（requirements.txt）

---

## セットアップ（初回だけ）

リポジトリ直下で：

```bat
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 実行方法

リポジトリ直下で（.venvに入ってから）：

```bat
python src\app.py
```

## CSV形式

- 文字コード：UTF-8
- ヘッダあり
- 必須列：`date`, `category`, `amount`
- 任意列：あっても無視されます（例：`quantity`）

例：

```csv
date,category,amount,quantity
2026-01-01,Food,12800,34
2026-01-01,Drink,3200,18
```

## よくあるエラー

### 必須列が不足しています（date, category, amount）

CSVの列名（ヘッダ）が `date`, `category`, `amount` になっているか確認してください。

### 読み込みに失敗しました。CSV形式と列名を確認してください

CSVが壊れている、文字コードが違う、区切り文字がカンマ以外などが原因の可能性があります。
