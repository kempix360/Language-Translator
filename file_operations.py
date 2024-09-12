import tkinter as tk
from tkinter import filedialog, messagebox


def load_file(input_text):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)
        messagebox.showinfo("File Loaded", "Text file loaded successfully.")


def save_translated_file(translated_text):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        messagebox.showinfo("File Saved", f"Translated file saved at {save_path}.")
