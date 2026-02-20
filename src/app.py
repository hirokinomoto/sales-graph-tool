import tkinter as tk
from tkinter import ttk, filedialog


def main():
    root = tk.Tk()
    root.title("Sales Graph Tool (Minimum)")
    root.geometry("900x600")

    # 状態
    selected_file = tk.StringVar(value="（未選択）")
    message = tk.StringVar(value="CSVを選択してください。")

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
        message.set("CSVを選択しました。次はグラフ作成を追加します。")

    btn_select = ttk.Button(input_frame, text="CSVを選択", command=on_select_csv)
    btn_select.pack(side="left", padx=10, pady=10)

    path_label = ttk.Label(input_frame, textvariable=selected_file)
    path_label.pack(side="left", padx=10)

    # メッセージエリア
    msg_frame = ttk.LabelFrame(root, text="メッセージ")
    msg_frame.pack(fill="x", padx=10, pady=10)

    msg_label = ttk.Label(msg_frame, textvariable=message)
    msg_label.pack(anchor="w", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()