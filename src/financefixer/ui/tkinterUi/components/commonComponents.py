import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from financefixer.ui.interfaces.interfaces import IUiComponent


class HeaderFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, text: str, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text

    def build(self):
        self.columnconfigure(0, weight=1)

        self.header_font = tkfont.nametofont(
            "TkHeadingFont"
        )  # Only available font during development is 'fixed', this may produce different results on other systems.
        # self.header_font.configure(size=14, weight="bold")

        # print(f"Default header font: {self.header_font.actual()}")
        # print(f"Font names: {tkfont.names()}")
        style = ttk.Style()
        style.configure("Header.TLabel", font=self.header_font)

        ttk.Label(self, text=self.text, style="Header.TLabel").grid(
            row=0, column=0, sticky="w"
        )
