import sys
from PySide6 import QtWidgets

from financefixer.domain.models.loan import Loan
from financefixer.ui.loanAppViewBase import LoanAppViewBase
from financefixer.ui.pySideUi.loanAppWidget import LoanAppWidget


class LoanAppView(LoanAppViewBase):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])

        self.widget = LoanAppWidget()
        self.widget.resize(800, 600)

    def execute(self):
        self.widget.show()
        sys.exit(self.app.exec())

    def bind_add_loan(self, callback):
        super().bind_add_loan(callback)
        self.widget.add_loan_button.clicked.connect(self.handle_add_loan)

    def handle_add_loan(self):
        if self.add_loan_callback:
            name = self.widget.name_input.text()
            principal = int(
                self.widget.principal_input.value() * 100
            )  # Convert to cents
            interest = self.widget.interest_input.value()
            min_payment = int(
                self.widget.min_payment_input.value() * 100
            )  # Convert to cents
            loan = Loan(
                name=name,
                principal_cents=principal,
                annual_rate=interest,
                min_payment_cents=min_payment,
            )
            self.add_loan_callback(loan)
        else:
            raise RuntimeError("Add loan callback not set")

    def bind_get_loan(self, callback):
        super().bind_get_loan(callback)
        self.widget.get_loan_button.clicked.connect(self.handle_get_loan)

    def handle_get_loan(self):
        if self.get_loan_callback:
            loan_id = self.widget.get_loan_id_input.value()
            self.get_loan_callback(loan_id)
        else:
            raise RuntimeError("Get loan callback not set")

    def refresh_loans(self):
        pass

    def handle_edit_loan(self, loan: Loan):
        pass

    def handle_delete_loan(self, loan_id: int):
        pass

    def show_message(self, message: str):
        QtWidgets.QMessageBox.information(self.widget, "Info", message)
