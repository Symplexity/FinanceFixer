import tkinter as tk
from tkinter import ttk

from financefixer.domain.models.loan import Loan
from financefixer.utils.eventBus import EventBus, Events


class LoanInputFrame(ttk.LabelFrame):
    def __init__(self, bus: EventBus, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.name_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.interest_var = tk.DoubleVar()
        self.min_payment_var = tk.DoubleVar()

        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text="Principal ($):").grid(row=1, column=0, sticky="w")
        ttk.Label(self, text="Annual Rate (%):").grid(row=2, column=0, sticky="w")
        ttk.Label(self, text="Min Payment ($):").grid(row=3, column=0, sticky="w")

        ttk.Entry(self, textvariable=self.name_var).grid(row=0, column=1)
        ttk.Entry(self, textvariable=self.amount_var).grid(row=1, column=1)
        ttk.Entry(self, textvariable=self.interest_var).grid(row=2, column=1)
        ttk.Entry(self, textvariable=self.min_payment_var).grid(row=3, column=1)

        self.add_button = ttk.Button(
            self, text="Add Loan", command=self.handle_add_loan
        )
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

    def get_inputs(self) -> Loan:
        return Loan(
            name=self.name_var.get(),
            principal_cents=int(self.amount_var.get() * 100),
            annual_rate=self.interest_var.get(),
            min_payment_cents=int(self.min_payment_var.get() * 100),
        )

    def handle_add_loan(self):
        input = self.get_inputs()
        self.event_bus.publish(Events.ADD_LOAN, loan=input)


class LoanDisplayFrame(ttk.LabelFrame):
    def __init__(self, bus: EventBus, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus
        self.event_bus.subscribe(Events.REFRESH_LOANS, self.refresh_loans)

        ttk.Label(self, text="Added Loans:").pack(anchor="w")

        list_container = ttk.Frame(self)
        list_container.pack(fill=tk.X, pady=5)

        list_scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.loan_table = ttk.Treeview(
            list_container,
            columns=("id", "name", "principal", "rate", "min_payment", "as_of_date"),
            show="headings",
            height=5,
            yscrollcommand=list_scrollbar.set,
        )

        self.loan_table.heading("id", text="ID")
        self.loan_table.heading("name", text="Name")
        self.loan_table.heading("principal", text="Principal ($)")
        self.loan_table.heading("rate", text="Annual Rate (%)")
        self.loan_table.heading("min_payment", text="Min Payment ($)")
        self.loan_table.heading("as_of_date", text="As of Date")

        self.loan_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        list_scrollbar.config(command=self.loan_table.yview)

        button_container = ttk.Frame(self)
        button_container.pack(fill=tk.X, pady=5)

        self.delete_button = ttk.Button(
            button_container, text="Delete Selected", command=self.handle_delete_loan
        )
        self.delete_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(
            button_container, text="Edit Selected", command=self.handle_edit_loan
        )
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

    def refresh_loans(self, loans: list[Loan]):
        self.loan_table.delete(*self.loan_table.get_children())
        for loan in loans:
            self.loan_table.insert(
                "",
                "end",
                iid=loan.id,
                values=(
                    loan.id,
                    loan.name,
                    f"{loan.principal_cents / 100:.2f}",
                    f"{loan.annual_rate:.2f}",
                    f"{loan.min_payment_cents / 100:.2f}",
                    loan.as_of_date.strftime("%Y-%m-%d"),
                ),
            )

    def get_selected(self):
        selected = self.loan_table.selection()
        return [int(item) for item in selected]

    def handle_delete_loan(self):
        self.event_bus.publish(Events.DELETE_LOAN, loan_ids=self.get_selected())

    def handle_edit_loan(self):
        self.event_bus.publish(Events.EDIT_LOAN, loan_id=self.get_selected())
