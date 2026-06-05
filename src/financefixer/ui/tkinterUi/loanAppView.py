import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from financefixer.domain.models.loan import Loan
from financefixer.ui.loanAppViewBase import LoanAppViewBase
from financefixer.ui.tkinterUi.components.loanAppComponents import (
    LoanDisplayFrame,
    LoanInputFrame,
)


class LoanAppView(LoanAppViewBase):
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        ## Loan Input
        self.loan_input_frame = LoanInputFrame(
            self.frame, text="Loan Details", padding=10
        )
        self.loan_input_frame.pack(fill=tk.X, pady=5)
        self.loan_input_frame.bind_add_loan(self.on_add_loan)

        ## Loan Display
        self.loan_display_frame = LoanDisplayFrame(
            self.frame, text="Added Loans", padding=10
        )
        self.loan_display_frame.pack(fill=tk.X, expand=True, pady=5)
        self.loan_display_frame.bind_delete_loan(self.on_delete_loan)
        self.loan_display_frame.bind_edit_loan(self.on_edit_loan)

    def execute(self):
        self.root.mainloop()

    def show_message(self, message: str):
        showinfo("Info", message)

    def bind_add_loan(self, callback):
        super().bind_add_loan(callback)

    def on_add_loan(self):
        if not self.add_loan_callback:
            raise ValueError("Add loan callback not set")
        loan = self.loan_input_frame.get_inputs()
        self.add_loan_callback(loan)

    def refresh_loans(self, loans: list[Loan]):
        self.loan_display_frame.refresh_loans(loans)

    def bind_delete_loan(self, callback):
        super().bind_delete_loan(callback)

    def on_delete_loan(self):
        if not self.delete_loan_callback:
            raise ValueError("Delete loan callback not set")
        selected_loan_ids = self.loan_display_frame.get_selected()
        if not selected_loan_ids:
            self.show_message("No loans selected for deletion")
            return
        self.delete_loan_callback(selected_loan_ids)

    def on_get_loan(self):
        pass

    def on_edit_loan(self, loan: Loan):
        pass

    def bind_edit_loan(self, callback):
        super().bind_edit_loan(callback)
