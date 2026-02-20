import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")  # Tkinterに埋め込むため
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


REQUIRED_COLS = {"date", "category", "amount"}


def main():
    root = tk.Tk()
    root.title("Sales Graph Tool (Minimum)")
    root.geometry("1000x700")

    # 状態
    selected_file = tk.StringVar(value="（未選択）")
    message = tk.StringVar(value="CSVを選択してください。")
    last_figure = {"fig": None}  # 保存Stepで使う予定（今は保持だけ）

    # ===== UI =====
    title = ttk.Label(root, text="売上CSV → カテゴリ別売上グラフ → PNG保存（最小版）")
    title.pack(pady=10)

    # 入力エリア
    input_frame = ttk.LabelFrame(root, text="入力")
    input_frame.pack(fill="x", padx=10, pady=10)

    def on_select_csv():
        path = filedialog.askopenfilename(
            title="売上CSVを選択",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return  # キャンセル
        selected_file.set(path)
        message.set("CSVを選択しました。次は「グラフ作成」を押してください。")

    btn_select = ttk.Button(input_frame, text="CSVを選択", command=on_select_csv)
    btn_select.pack(side="left", padx=10, pady=10)

    path_label = ttk.Label(input_frame, textvariable=selected_file)
    path_label.pack(side="left", padx=10)

    btn_make = ttk.Button(input_frame, text="グラフ作成")
    btn_make.pack(side="right", padx=10, pady=10)

    # グラフ表示エリア
    graph_frame = ttk.LabelFrame(root, text="グラフ（カテゴリ別売上合計）")
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas_holder = {"canvas": None}  # 既存キャンバスの破棄用

    def show_figure(fig: Figure):
        # 既に表示しているグラフがあれば破棄して差し替える
        if canvas_holder["canvas"] is not None:
            canvas_holder["canvas"].get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas_holder["canvas"] = canvas

    def make_graph():
        path = selected_file.get()
        if not path or path == "（未選択）":
            message.set("CSVを選択してください。")
            return

        # CSV読み込み
        try:
            df = pd.read_csv(path)
        except Exception:
            message.set("読み込みに失敗しました。CSV形式と列名を確認してください。")
            return

        # 必須列チェック
        cols = set(df.columns)
        if not REQUIRED_COLS.issubset(cols):
            message.set("必須列が不足しています（date, category, amount）")
            return

        # 集計（カテゴリ別売上合計）
        try:
            grouped = (
                df.groupby("category", as_index=False)["amount"]
                .sum()
                .sort_values("amount", ascending=False)
            )
        except Exception:
            message.set("集計に失敗しました。amount列が数値か確認してください。")
            return

        # グラフ作成
        fig = Figure(figsize=(8, 4.5))
        ax = fig.add_subplot(111)

        ax.bar(grouped["category"], grouped["amount"])
        ax.set_title("Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        # ラベルが長い時に見切れにくくする
        fig.tight_layout()

        show_figure(fig)
        last_figure["fig"] = fig
        message.set("グラフを作成しました。次はPNG保存を追加します。")

    btn_make.config(command=make_graph)

    # メッセージエリア
    msg_frame = ttk.LabelFrame(root, text="メッセージ")
    msg_frame.pack(fill="x", padx=10, pady=10)

    msg_label = ttk.Label(msg_frame, textvariable=message)
    msg_label.pack(anchor="w", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()