import argparse

from financefixer.data.loanRepo import LoanRepo
from financefixer.application.loanApplication import LoanActions

from financefixer.ui.loanAppPresenter import LoanAppPresenter
from financefixer.ui.loanAppViewBase import LoanAppViewBase


class FinanceFixerApp:
    def __init__(self):
        self.loan_repo = LoanRepo()
        self.loan_actions = LoanActions(self.loan_repo)
        self.view: LoanAppViewBase | None = None

    def _run(self):
        if self.view is None:
            raise RuntimeError("UI view is not initialized")
        presenter = LoanAppPresenter(self.view, self.loan_actions)
        presenter.start()

    def run_tkinter(self):
        import tkinter as tk
        from financefixer.ui.tkinterUi.loanAppView import LoanAppView

        root = tk.Tk()
        root.title("FinanceFixer - Loan Management")
        self.view = LoanAppView(root)
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


# def run():
#     parser = argparse.ArgumentParser(description="FinanceFixer Loan Management")
#     parser.add_argument(
#         "--ui",
#         choices=["tkinter", "pyside"],
#         default="tkinter",
#         help="UI framework to use",
#     )
#     args = parser.parse_args()

#     loan_repo = LoanRepo()
#     loan_actions = LoanActions(loan_repo)

#     if args.ui == "tkinter":
#         import tkinter as tk
#         from financefixer.ui.tkinterUi.loanAppView import LoanAppView

#         root = tk.Tk()
#         root.title("FinanceFixer - Loan Management")
#         view = LoanAppView(root)
#     elif args.ui == "pyside":
#         from financefixer.ui.pySideUi.loanAppView import LoanAppView

#         view = LoanAppView()
#     else:
#         raise ValueError(f"Unsupported UI framework: {args.ui}")

#     presenter = LoanAppPresenter(view, loan_actions)
#     presenter.start()
