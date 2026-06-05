import argparse

from financefixer.data.loanRepo import LoanRepo
from financefixer.application.loanApplication import LoanActions

from financefixer.ui.loanAppPresenter import LoanAppPresenter


def run():
    parser = argparse.ArgumentParser(description="FinanceFixer Loan Management")
    parser.add_argument(
        "--ui",
        choices=["tkinter", "pyside"],
        default="tkinter",
        help="UI framework to use",
    )
    args = parser.parse_args()

    loan_repo = LoanRepo()
    loan_actions = LoanActions(loan_repo)

    if args.ui == "tkinter":
        import tkinter as tk
        from financefixer.ui.tkinterUi.loanAppView import LoanAppView

        root = tk.Tk()
        root.title("FinanceFixer - Loan Management")
        view = LoanAppView(root)
    elif args.ui == "pyside":
        from financefixer.ui.pySideUi.loanAppView import LoanAppView

        view = LoanAppView()
    else:
        raise ValueError(f"Unsupported UI framework: {args.ui}")

    presenter = LoanAppPresenter(view, loan_actions)
    presenter.start()
