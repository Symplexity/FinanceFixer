from financefixer.domain.models.loan import Loan
from financefixer.application.loanApplication import LoanActions


class LoanAppPresenter:
    def __init__(self, view, loan_actions: LoanActions):
        self.view = view
        self.loan_actions = loan_actions

        self.view.bind_add_loan(self.on_add_loan)
        self.view.bind_edit_loan(self.on_get_loan)
        self.view.bind_delete_loan(self.on_delete_loan)

        self.refresh_loans()

    def start(self):
        self.view.execute()

    def on_add_loan(self, loan: Loan):
        try:
            loan = self.loan_actions.add_loan(loan)
            self.refresh_loans()
            self.view.show_message(
                f"Loan '{loan.name}' (id: {loan.id}) added successfully."
            )
        except Exception as e:
            self.view.show_message(f"Error adding loan: {str(e)}")

    def on_get_loan(self, loan_id: int):
        try:
            loan = self.loan_actions.get_loan_by_id(loan_id)
            self.view.show_message(f"Loan '{loan.name}' (id: {loan.id}) retrieved.")
        except Exception as e:
            self.view.show_message(f"Error retrieving loan: {str(e)}")

    def on_delete_loan(self, loan_ids: list[int]):
        try:
            for loan_id in loan_ids:
                self.loan_actions.delete_loan(loan_id)
            self.refresh_loans()
            self.view.show_message(
                f"Deleted loans with IDs: {', '.join(map(str, loan_ids))}"
            )
        except Exception as e:
            self.view.show_message(f"Error deleting loans: {str(e)}")

    def refresh_loans(self):
        try:
            loans = self.loan_actions.get_all_loans()
            self.view.refresh_loans(loans)
        except Exception as e:
            self.view.show_message(f"Error refreshing loans: {str(e)}")
