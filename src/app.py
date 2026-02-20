import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title("Sales Graph Tool (Minimum)")
    root.geometry("900x600")

    title = ttk.Label(root, text="売上CSV → カテゴリ別売上グラフ → PNG保存（最小版）")
    title.pack(pady=10)

    msg = ttk.Label(root, text="起動確認OK。次はCSV選択ボタンを追加します。")
    msg.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()