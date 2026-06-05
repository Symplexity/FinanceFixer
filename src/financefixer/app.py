from financefixer.data.loanRepo import LoanRepo
from financefixer.application.loanApplication import LoanActions

from financefixer.ui.interfaces.interfaces import ILoanAppView
from financefixer.ui.loanAppPresenter import LoanAppPresenter

from financefixer.utils.eventBus import EventBus


class FinanceFixerApp:
    def __init__(self):
        self.loan_repo = LoanRepo()
        self.event_bus = EventBus()
        self.loan_actions = LoanActions(self.loan_repo)
        self.view: ILoanAppView | None = None

    def _run(self):
        if self.view is None:
            raise RuntimeError("UI view is not initialized")
        presenter = LoanAppPresenter(self.view, self.event_bus, self.loan_actions)
        presenter.start()

    def run_tkinter(self):
        import tkinter as tk
        from financefixer.ui.tkinterUi.loanAppView import LoanAppView

        root = tk.Tk()
        root.title("FinanceFixer - Loan Management")
        self.view = LoanAppView(root, self.event_bus)
        self._run()

    def run_pyside(self):
        from financefixer.ui.pySideUi.loanAppView import LoanAppView

        self.view = LoanAppView()
        self._run()


app = FinanceFixerApp()


def run_tkinter():
    app.run_tkinter()


def run_pyside():
    app.run_pyside()
