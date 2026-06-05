from warnings import deprecated
from abc import ABC, abstractmethod

from financefixer.domain.models.loan import Loan


class LoanAppViewBase(ABC):
    def __init__(self, **kwargs):
        self.get_loan_callback = None
        self.add_loan_callback = None
        self.refresh_loans_callback = None
        self.delete_loan_callback = None
        self.edit_loan_callback = None

    ## Common UI methods
    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def show_message(self, message: str): ...

    ## LoanInputComponent methods
    def bind_add_loan(self, callback):
        self.add_loan_callback = callback

    @abstractmethod
    def on_add_loan(self): ...

    @deprecated("Use refresh_loans instead")
    def bind_get_loan(self, callback):
        self.get_loan_callback = callback

    @deprecated("Use on_refresh_loans instead")
    @abstractmethod
    def on_get_loan(self): ...

    ## LoanDisplayComponent methods
    @abstractmethod
    def refresh_loans(self, loans: list[Loan]): ...

    def bind_delete_loan(self, callback):
        self.delete_loan_callback = callback

    @abstractmethod
    def on_delete_loan(self): ...

    def bind_edit_loan(self, callback):
        self.edit_loan_callback = callback

    @abstractmethod
    def on_edit_loan(self, loan: Loan): ...
