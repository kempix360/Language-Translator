import tkinter as tk
from tkinter import ttk, messagebox, font
from translator import translate_text
from file_operations import load_file, save_translated_file


def setup_gui(root):
    # Configure grid layout
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # Set overall style
    style = ttk.Style()
    style.configure("TLabel", font=("Calibri", 12), padding=5)
    style.configure("TCombobox", font=("Calibri", 12))
    style.configure("TButton", font=("Calibri", 12, "bold"), foreground="blue", background="#007bff", padding=10)

    # Input text field
    input_label = ttk.Label(root, text="Enter text to translate:")
    input_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

    global input_text
    input_text = tk.Text(root, height=25, width=50, wrap=tk.WORD, font=("Calibri", 12), bg="#f4f4f4", bd=1,
                         relief="solid", padx=5, pady=5)
    input_text.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")

    # Output text field
    output_label = ttk.Label(root, text="Translated text:")
    output_label.grid(row=0, column=1, padx=25, pady=10, sticky="w")

    global output_text
    output_text = tk.Text(root, height=25, width=50, wrap=tk.WORD, font=("Calibri", 12), bg="#f4f4f4", bd=1,
                          relief="solid", padx=5, pady=5)
    output_text.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")


    # Language selection dropdowns
    src_lang_label = ttk.Label(root, text="Source Language:")
    src_lang_label.grid(row=2, column=0, padx=25, pady=5, sticky="w")

    global src_lang
    src_lang = ttk.Combobox(root, values=["English", "Spanish", "French", "German", "Chinese", "Japanese"])
    src_lang.grid(row=3, column=0, padx=30, pady=5, sticky="w")
    src_lang.set("English")

    dest_lang_label = ttk.Label(root, text="Destination Language:")
    dest_lang_label.grid(row=2, column=1, padx=25, pady=5, sticky="w")

    global dest_lang
    dest_lang = ttk.Combobox(root, values=["English", "Spanish", "French", "German", "Chinese", "Japanese"])
    dest_lang.grid(row=3, column=1, padx=30, pady=5, sticky="w")
    dest_lang.set("Spanish")

    # Buttons
    translate_button = ttk.Button(root, text="Translate", style="TButton", command=perform_translation)
    translate_button.grid(row=6, column=0, pady=30)

    load_button = ttk.Button(root, text="Load txt File", style="TButton", command=lambda: load_file(input_text))
    load_button.grid(row=6, column=1, pady=30)


def perform_translation():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return
    src = src_lang.get()
    dest = dest_lang.get()
    translated_text = translate_text(text, src, dest)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translated_text)
