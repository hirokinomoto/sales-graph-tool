# src/app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


APP_TITLE = "Sales Graph Tool (Minimum)"
REQUIRED_COLS = {"date", "category", "amount"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x620")

        self.csv_path = tk.StringVar(value="(未選択)")
        self.msg = tk.StringVar(value="CSVを選択してください。")

        self.df = None
        self.figure = None
        self.canvas = None

        self._build_ui()

    def _build_ui(self):
        # ===== Title =====
        title = ttk.Label(
            self,
            text="売上CSV → カテゴリ別売上グラフ（最小版）",
            font=("Meiryo UI", 12, "bold"),
            anchor="center",
        )
        title.pack(fill="x", pady=(10, 6))

        # ===== Input =====
        frame_in = ttk.LabelFrame(self, text="入力")
        frame_in.pack(fill="x", padx=12, pady=8)

        btn_csv = ttk.Button(frame_in, text="CSVを選択", command=self.on_select_csv)
        btn_csv.pack(side="left", padx=8, pady=10)

        lbl_path = ttk.Label(frame_in, textvariable=self.csv_path)
        lbl_path.pack(side="left", padx=8, pady=10)

        btn_plot = ttk.Button(frame_in, text="グラフ作成", command=self.on_make_graph)
        btn_plot.pack(side="right", padx=8, pady=10)

        # ===== Graph Area =====
        frame_graph = ttk.LabelFrame(self, text="グラフ（カテゴリ別売上 合計）")
        frame_graph.pack(fill="both", expand=True, padx=12, pady=8)

        self.graph_container = ttk.Frame(frame_graph)
        self.graph_container.pack(fill="both", expand=True, padx=8, pady=8)

        # ===== Message =====
        frame_msg = ttk.LabelFrame(self, text="メッセージ")
        frame_msg.pack(fill="x", padx=12, pady=(0, 12))

        lbl_msg = ttk.Label(frame_msg, textvariable=self.msg)
        lbl_msg.pack(fill="x", padx=8, pady=8)

    def on_select_csv(self):
        path = filedialog.askopenfilename(
            title="売上CSVを選択",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        self.csv_path.set(path)
        self.msg.set("CSVを選択しました。次は「グラフ作成」を押してください。")

    def on_make_graph(self):
        path = self.csv_path.get()
        if not path or path == "(未選択)":
            self.msg.set("CSVが未選択です。「CSVを選択」を押してください。")
            return

        try:
            df = pd.read_csv(path)
        except Exception as e:
            self.msg.set("CSVの読み込みに失敗しました。")
            messagebox.showerror("CSV読み込みエラー", str(e))
            return

        # --- minimal validation ---
        missing = REQUIRED_COLS - set(df.columns)
        if missing:
            self.msg.set(f"必須列が不足しています: {', '.join(sorted(missing))}")
            return

        # amount must be numeric
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        if df["amount"].isna().any():
            self.msg.set("amount列に数値以外が含まれています。CSVを確認してください。")
            return

        # aggregate
        grouped = df.groupby("category", as_index=True)["amount"].sum().sort_values(ascending=False)

        # draw
        self._render_bar_chart(grouped)
        self.msg.set("グラフを作成しました。")

    def _render_bar_chart(self, series):
        # clear previous canvas
        for w in self.graph_container.winfo_children():
            w.destroy()

        fig = Figure(figsize=(7.5, 4.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(series.index.astype(str), series.values)
        ax.set_title("Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")
        ax.tick_params(axis="x", rotation=0)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.figure = fig
        self.canvas = canvas


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()