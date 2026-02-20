# src/app.py
# Sales Graph Tool (Minimum)
# CSV -> Category total bar graph -> Save PNG
#
# Requirements: pandas, matplotlib
# Run: python src\app.py

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, filedialog

import pandas as pd

import matplotlib
matplotlib.use("TkAgg")  # Tkinterで表示するため
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


REQUIRED_COLUMNS = ["date", "category", "amount"]


class SalesGraphApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Sales Graph Tool (Minimum)")
        self.geometry("980x720")

        # state
        self.csv_path: str | None = None
        self.df: pd.DataFrame | None = None
        self.fig: Figure | None = None
        self.canvas: FigureCanvasTkAgg | None = None
        self.graph_ready: bool = False

        # UI vars
        self.csv_path_var = tk.StringVar(value="(未選択)")
        self.msg_var = tk.StringVar(value="CSVを選択してください。")

        self._build_ui()

    # -------------------------
    # UI
    # -------------------------
    def _build_ui(self) -> None:
        title = ttk.Label(
            self,
            text="売上CSV → カテゴリ別売上グラフ → PNG保存（最小版）",
            font=("Meiryo UI", 12, "bold"),
        )
        title.pack(pady=(12, 8))

        # 入力エリア
        frm_input = ttk.LabelFrame(self, text="入力")
        frm_input.pack(fill="x", padx=12, pady=(0, 10))

        btn_select = ttk.Button(frm_input, text="CSVを選択", command=self.on_select_csv)
        btn_select.pack(side="left", padx=10, pady=10)

        lbl_path = ttk.Label(frm_input, textvariable=self.csv_path_var)
        lbl_path.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.btn_create_graph = ttk.Button(frm_input, text="グラフ作成", command=self.on_create_graph)
        self.btn_create_graph.pack(side="right", padx=10, pady=10)

        # グラフエリア
        frm_graph = ttk.LabelFrame(self, text="グラフ（カテゴリ別売上 合計）")
        frm_graph.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        # 右上にPNG保存ボタン
        top_right = ttk.Frame(frm_graph)
        top_right.pack(fill="x", padx=8, pady=(8, 0))
        self.btn_save_png = ttk.Button(top_right, text="PNG保存", command=self.on_save_png, state="disabled")
        self.btn_save_png.pack(side="right")

        # Matplotlibキャンバスを置く領域
        self.graph_container = ttk.Frame(frm_graph)
        self.graph_container.pack(fill="both", expand=True, padx=8, pady=8)

        # メッセージエリア
        frm_msg = ttk.LabelFrame(self, text="メッセージ")
        frm_msg.pack(fill="x", padx=12, pady=(0, 12))
        lbl_msg = ttk.Label(frm_msg, textvariable=self.msg_var)
        lbl_msg.pack(anchor="w", padx=10, pady=10)

    # -------------------------
    # Handlers
    # -------------------------
    def on_select_csv(self) -> None:
        path = filedialog.askopenfilename(
            title="売上CSVを選択",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            self.msg_var.set("CSV選択をキャンセルしました。")
            return

        self.csv_path = path
        self.csv_path_var.set(path)
        self.msg_var.set("CSVを選択しました。次は『グラフ作成』を押してください。")

        # CSVが変わったらグラフ状態をリセット
        self._reset_graph_state()

    def on_create_graph(self) -> None:
        if not self.csv_path:
            self.msg_var.set("先にCSVを選択してください。")
            return

        try:
            df = self._read_csv_safely(self.csv_path)
        except Exception as e:
            self.msg_var.set(f"CSVの読み込みに失敗しました: {e}")
            self._reset_graph_state()
            return

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            self.msg_var.set(f"必須列が不足しています: {', '.join(missing)}（必要: {', '.join(REQUIRED_COLUMNS)}）")
            self._reset_graph_state()
            return

        # amount を数値化（失敗したらNaN -> 0）
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        # category別に合計
        summary = df.groupby("category", as_index=False)["amount"].sum()

        # Figure作成
        fig = Figure(figsize=(8.8, 4.6), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(summary["category"], summary["amount"])
        ax.set_title("Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")
        fig.tight_layout()

        # 既存キャンバスがあれば破棄して差し替え
        self._destroy_canvas_if_exists()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        # state保存（← PNG保存が動かない原因をここで潰す）
        self.df = df
        self.fig = fig
        self.canvas = canvas
        self.graph_ready = True
        self.btn_save_png.config(state="normal")

        self.msg_var.set("グラフを作成しました。次は『PNG保存』を押せます。")

    def on_save_png(self) -> None:
        # ここが「正しい？」の答え：
        # グラフ未作成の時は保存できない＝正しい挙動にする
        if not self.graph_ready or self.fig is None:
            self.msg_var.set("まだグラフがありません。先に『グラフ作成』を押してください。")
            return

        default_name = "sales_by_category.png"
        path = filedialog.asksaveasfilename(
            title="PNGとして保存",
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            initialfile=default_name,
        )
        if not path:
            self.msg_var.set("保存をキャンセルしました。")
            return

        try:
            # 保存（Figureを保持しているので確実）
            self.fig.savefig(path, dpi=150, bbox_inches="tight")
        except Exception as e:
            self.msg_var.set(f"PNG保存に失敗しました: {e}")
            return

        self.msg_var.set(f"PNG保存しました: {os.path.basename(path)}")

    # -------------------------
    # Helpers
    # -------------------------
    def _reset_graph_state(self) -> None:
        self.df = None
        self.fig = None
        self.graph_ready = False
        self.btn_save_png.config(state="disabled")
        self._destroy_canvas_if_exists()

    def _destroy_canvas_if_exists(self) -> None:
        if self.canvas is not None:
            widget = self.canvas.get_tk_widget()
            widget.destroy()
            self.canvas = None

        # container内に残骸が残るケースも潰す
        for child in self.graph_container.winfo_children():
            child.destroy()

    def _read_csv_safely(self, path: str) -> pd.DataFrame:
        """
        Excel経由で保存されたCSVでも読めるように複数エンコードを試す。
        """
        last_err: Exception | None = None
        for enc in ("utf-8-sig", "utf-8", "cp932"):
            try:
                return pd.read_csv(path, encoding=enc)
            except Exception as e:
                last_err = e
        raise last_err or RuntimeError("CSV read failed")


def main() -> None:
    app = SalesGraphApp()
    app.mainloop()


if __name__ == "__main__":
    main()