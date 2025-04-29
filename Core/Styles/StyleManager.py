# Styles/StyleManager.py

import tkinter as tk
from tkinter import ttk

class StyleManager:
    @staticmethod
    def apply_styles(root: tk.Tk):
        """
        Apply a modern and clean style to the Tkinter app.
        """
        root.configure(bg="#f7f7f7")
        style = ttk.Style(root)

        style.theme_use('default')

        # Setting font globally with separate parameters
        root.option_add("*Font", ("Segoe UI", 11))  # <-- CORRECT

        # Combobox
        style.configure('TCombobox',
                        fieldbackground='#ffffff',
                        background='#ffffff',
                        foreground='#333333',
                        padding=5,
                        relief="flat")

        # Button
        style.configure('TButton',
                        background='#4a90e2',
                        foreground='#ffffff',
                        font=('Segoe UI', 11),
                        padding=6,
                        relief="flat")
        style.map('TButton',
                  background=[('active', '#357ABD'), ('pressed', '#2E5EAA')])

        # Label
        style.configure('TLabel',
                        background="#f7f7f7",
                        foreground="#333333",
                        font=('Segoe UI', 11))

        # Entry
        style.configure('TEntry',
                        fieldbackground='#ffffff',
                        foreground='#333333',
                        padding=4,
                        relief="flat")

        # Frame
        style.configure('TFrame',
                        background="#f7f7f7")
