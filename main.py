import tkinter as tk
from gui import setup_gui

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Translator")
    root.geometry("600x700")
    root.state('zoomed')
    root.resizable(width=True, height=True)

    # Set up the GUI components
    setup_gui(root)

    # Start the application
    root.mainloop()
