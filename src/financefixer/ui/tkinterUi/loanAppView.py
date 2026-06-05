import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from financefixer.ui.tkinterUi.components.loanAppComponents import (
    LoanPanelDisplayFrame,
    LoanPanelHeaderFrame,
    LoanRepaymentSimulationFrame,
)
from financefixer.utils.eventBus import EventBus, Events


class LoanAppView:
    def __init__(self, parent, bus: EventBus):
        self.root = parent
        self.event_bus = bus

        self.event_bus.subscribe(Events.SHOW_MESSAGE, self.show_message)

        self.build()

    def build(self):
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # self.notebook = ttk.Notebook(self.frame)
        # self.notebook.pack(fill=tk.BOTH, expand=True)

        # loan_tab = ttk.Frame(self.notebook)
        # tab2 = ttk.Frame(self.notebook)

        # self.notebook.add(loan_tab, text="Loans")
        # self.notebook.add(tab2, text="Tab 2")

        ## Loan Input
        self.loan_input_frame = LoanPanelHeaderFrame(
            self.frame, self.event_bus, text="Loans", padding=10
        )
        self.loan_input_frame.pack(fill=tk.X)

        ## Loan Display
        self.loan_display_frame = LoanPanelDisplayFrame(
            self.frame, self.event_bus, padding=10
        )
        self.loan_display_frame.pack(fill=tk.X, expand=True, pady=5)

        # TODO: Loan Repayment Simulation (Options, Charts, Summary, Amortization, etc.)
        self.loan_repayment_sim_frame = LoanRepaymentSimulationFrame(
            self.frame, self.event_bus, padding=10
        )
        self.loan_repayment_sim_frame.pack(fill=tk.BOTH, expand=True)

    def execute(self):
        self.root.mainloop()

    def show_message(self, message: str):
        # showinfo("Info", message)
        print(f"Message: {message}")
