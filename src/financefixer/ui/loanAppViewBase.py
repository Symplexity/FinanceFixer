from warnings import deprecated
from abc import ABC, abstractmethod

from financefixer.domain.models.loan import Loan


class LoanAppViewBase(ABC):
    ## Common UI methods
    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def show_message(self, message: str): ...
