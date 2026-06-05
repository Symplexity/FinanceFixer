import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from financefixer.ui.loanAppViewBase import LoanAppViewBase
from financefixer.ui.tkinterUi.components.loanAppComponents import (
    LoanDisplayFrame,
    LoanInputFrame,
)
from financefixer.utils.eventBus import EventBus, Events


class LoanAppView(LoanAppViewBase):
    def __init__(self, root, bus: EventBus):
        self.root = root
        self.event_bus = bus

        self.event_bus.subscribe(Events.SHOW_MESSAGE, self.show_message)

        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        loan_tab = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)

        self.notebook.add(loan_tab, text="Loans")
        self.notebook.add(tab2, text="Tab 2")

        ## Loan Input
        self.loan_input_frame = LoanInputFrame(
            self.event_bus, loan_tab, text="Loan Details", padding=10
        )
        self.loan_input_frame.pack(fill=tk.X, pady=5)

        ## Loan Display
        self.loan_display_frame = LoanDisplayFrame(
            self.event_bus, loan_tab, text="Added Loans", padding=10
        )
        self.loan_display_frame.pack(fill=tk.X, expand=True, pady=5)

    def execute(self):
        self.root.mainloop()

    def show_message(self, message: str):
        showinfo("Info", message)
