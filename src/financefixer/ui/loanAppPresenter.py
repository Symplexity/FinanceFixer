from financefixer.domain.models.loan import Loan
from financefixer.application.loanApplication import LoanActions

from financefixer.utils.eventBus import EventBus, Events


class LoanAppPresenter:
    def __init__(self, view, event_bus: EventBus, loan_actions: LoanActions):
        self.view = view
        self.event_bus = event_bus
        self.loan_actions = loan_actions

        self.event_bus.subscribe(Events.ADD_LOAN, self.handle_add_loan)
        self.event_bus.subscribe(Events.GET_LOAN, self.handle_get_loan)
        self.event_bus.subscribe(Events.DELETE_LOAN, self.handle_delete_loan)
        self.event_bus.subscribe(Events.EDIT_LOAN, self.handle_edit_loan)

        self.refresh_loans()

    def start(self):
        self.view.execute()

    def handle_add_loan(self, loan: Loan):
        try:
            loan = self.loan_actions.add_loan(loan)
            self.refresh_loans()
            self.event_bus.publish(
                Events.SHOW_MESSAGE,
                message=f"Loan '{loan.name}' (id: {loan.id}) added successfully.",
            )
        except Exception as e:
            self.event_bus.publish(
                Events.SHOW_MESSAGE, message=f"Error adding loan: {str(e)}"
            )

    def handle_get_loan(self, loan_id: int):
        try:
            loan = self.loan_actions.get_loan_by_id(loan_id)
            self.event_bus.publish(
                Events.SHOW_MESSAGE,
                message=f"Loan '{loan.name}' (id: {loan.id}) retrieved.",
            )
        except Exception as e:
            self.event_bus.publish(
                Events.SHOW_MESSAGE, message=f"Error retrieving loan: {str(e)}"
            )

    def handle_delete_loan(self, loan_ids: list[int]):
        try:
            for loan_id in loan_ids:
                self.loan_actions.delete_loan(loan_id)
            self.refresh_loans()
            self.event_bus.publish(
                Events.SHOW_MESSAGE,
                message=f"Deleted loans with IDs: {', '.join(map(str, loan_ids))}",
            )
        except Exception as e:
            self.event_bus.publish(
                Events.SHOW_MESSAGE, message=f"Error deleting loans: {str(e)}"
            )

    def handle_edit_loan(self, loan_id: int):
        raise NotImplementedError("Edit loan functionality not implemented yet")

    def refresh_loans(self):
        try:
            loans = self.loan_actions.get_all_loans()
            self.event_bus.publish(Events.REFRESH_LOANS, loans=loans)
        except Exception as e:
            self.event_bus.publish(
                Events.SHOW_MESSAGE, message=f"Error refreshing loans: {str(e)}"
            )
