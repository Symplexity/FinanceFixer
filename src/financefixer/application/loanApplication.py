from financefixer.data.loanRepo import LoanRepo
from financefixer.domain.models.loan import Loan


class LoanActions:
    def __init__(self, loan_repo: LoanRepo):
        self.repo = loan_repo

    def add_loan(self, loan: Loan) -> Loan:
        return self.repo.insert_loan(loan)

    def get_loan_by_id(self, loan_id: int) -> Loan:
        return self.repo.get_loan(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return self.repo.get_all_loans()

    def update_loan(self, loan: Loan) -> bool:
        return self.repo.update_loan(loan)

    def delete_loan(self, loan_id: int) -> bool:
        return self.repo.delete_loan(loan_id)
