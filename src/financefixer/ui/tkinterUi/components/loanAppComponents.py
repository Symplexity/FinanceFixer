import tkinter as tk
from tkinter import ttk

from financefixer.ui.interfaces.interfaces import IUiComponent
from financefixer.ui.tkinterUi.components.commonComponents import HeaderFrame

from financefixer.domain.models.loan import Loan
from financefixer.utils.eventBus import EventBus, Events


class LoanPanelFrame(ttk.Frame, IUiComponent):
    def __init__(self, bus: EventBus, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.build()

    def build(self):
        pass


class LoanPanelHeaderFrame(HeaderFrame, IUiComponent):
    class LoanInputDialogFrame(tk.Toplevel, IUiComponent):
        def __init__(self, parent, bus: EventBus, title: str):
            super().__init__(parent)
            self.event_bus = bus
            self.title(title)
            self.transient(parent)  # Set to be on top of the main window
            self.grab_set()

            self.build()

        def build(self):

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

            self.save_button = ttk.Button(self, text="Save", command=self.handle_save)
            self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        def get_inputs(self) -> Loan:
            return Loan(
                name=self.name_var.get(),
                principal_cents=int(self.amount_var.get() * 100),
                annual_rate=self.interest_var.get(),
                min_payment_cents=int(self.min_payment_var.get() * 100),
            )

        def handle_save(self):
            try:
                loan = self.get_inputs()
                self.event_bus.publish(Events.ADD_LOAN, loan=loan)
                self.destroy()  # Close the dialog after saving
            except Exception as e:
                self.event_bus.publish(
                    Events.SHOW_MESSAGE, message=f"Error saving loan: {str(e)}"
                )

    def __init__(self, parent, bus: EventBus, text: str, **kwargs):
        super().__init__(parent, text, **kwargs)

        self.event_bus = bus
        super().build()  # Build the header label
        self.build()

    def build(self):

        self.add_button = ttk.Button(
            self, text="Add Loan", command=self.handle_add_loan
        )
        self.add_button.grid(row=0, column=1, sticky="e", pady=5)

    def handle_add_loan(self):
        dialog = self.LoanInputDialogFrame(self, self.event_bus, title="Add Loan")
        dialog.grab_set()  # Make the dialog modal
        self.wait_window(dialog)  # Wait until the dialog is closed


class LoanPanelDisplayFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus
        self.event_bus.subscribe(Events.REFRESH_LOANS, self.refresh_loans)

        self.build()

    def build(self):
        # ttk.Label(self, text="Added Loans:").pack(anchor="w")

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


class LoanRepaymentSimulationFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.build()

    def build(self):
        pass
        # Options frame
        self.options_frame = LoanRepaymentSimOptionsFrame(self, self.event_bus)
        self.options_frame.pack(fill=tk.X, pady=5)

        # Charts frame
        self.charts_frame = LoanRepaymentSimChartsFrame(self, self.event_bus)
        self.charts_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Summary frame
        self.summary_frame = LoanRepaymentSimSummaryFrame(self, self.event_bus)
        self.summary_frame.pack(fill=tk.X, pady=5)

        # Amortization frame
        self.amortization_frame = LoanRepaymentSimAmortizationFrame(
            self, self.event_bus
        )
        self.amortization_frame.pack(fill=tk.BOTH, expand=True, pady=5)


class LoanRepaymentSimOptionsFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.event_bus.subscribe(
            Events.SIM_OPTIONS_CHANGED,
            lambda options: print(f"Received options changed event: {options}"),
        )

        self._suspend_events = False
        self._options_change_job = None  # Job reference for debouncing option changes

        self.build()
        self._wire_change_events()

        self._suspend_events = False
        self._emit_options_changed()  # Emit initial options on startup

    def build(self):
        ttk.Label(self, text="Repayment Strategy:").grid(row=0, column=0, sticky="w")

        ## Strategy selection
        self.strategy_var = tk.StringVar(value="avalanche")

        ttk.Radiobutton(
            self,
            text="Avalanche (Highest Interest First)",
            variable=self.strategy_var,
            value="avalanche",
        ).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(
            self,
            text="Snowball (Smallest Balance First)",
            variable=self.strategy_var,
            value="snowball",
        ).grid(row=1, column=1, sticky="w")

        ## Payment settings
        ttk.Label(self, text="Monthly Payment Settings:").grid(
            row=2, column=0, sticky="w"
        )

        self.payment_type_var = tk.StringVar(value="fixed")
        ttk.Radiobutton(
            self,
            text="Fixed Monthly Payment",
            variable=self.payment_type_var,
            value="fixed",
            command=self._on_payment_type_change,
        ).grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(
            self,
            text="Increasing Payment",
            variable=self.payment_type_var,
            value="increasing",
            command=self._on_payment_type_change,
        ).grid(row=3, column=1, sticky="w")

        # Dynamic input area
        self.inputs_frame = ttk.Frame(self)
        self.inputs_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        self.inputs_frame.columnconfigure(1, weight=1)

        # Fixed payment widgets
        self.fixed_amount_var = tk.DoubleVar(value=1000.0)
        self.fixed_amount_label = ttk.Label(
            self.inputs_frame, text="Monthly Amount ($):"
        )
        self.fixed_amount_entry = ttk.Entry(
            self.inputs_frame, textvariable=self.fixed_amount_var
        )

        # Increasing payment widgets
        self.start_amount_var = tk.DoubleVar(value=1000.0)
        self.increase_frequency_months_var = tk.IntVar(value=6)
        self.increase_type_var = tk.StringVar(value="percent")
        self.increase_value_percent_var = tk.DoubleVar(value=5.0)
        self.increase_value_fixed_var = tk.DoubleVar(value=100.0)

        self.start_amount_label = ttk.Label(
            self.inputs_frame, text="Starting Amount ($):"
        )
        self.start_amount_entry = ttk.Entry(
            self.inputs_frame, textvariable=self.start_amount_var
        )

        self.frequency_label = ttk.Label(
            self.inputs_frame, text="Increase Frequency (months):"
        )
        self.frequency_spinbox = ttk.Spinbox(
            self.inputs_frame,
            from_=1,
            to=120,
            textvariable=self.increase_frequency_months_var,
        )

        self.increase_type_label = ttk.Label(self.inputs_frame, text="Increase Type:")
        self.increase_type_combo = ttk.Combobox(
            self.inputs_frame,
            textvariable=self.increase_type_var,
            values=("percent", "fixed"),
            state="readonly",
        )

        self.increase_value_fixed_label = ttk.Label(
            self.inputs_frame, text="Increase Value ($):"
        )
        self.increase_value_percent_label = ttk.Label(
            self.inputs_frame, text="Increase Value (%):"
        )
        self.increase_value_percent_entry = ttk.Spinbox(
            self.inputs_frame,
            from_=0,
            to=100,
            increment=0.01,
            textvariable=self.increase_value_percent_var,
            format="%.2f",
        )
        self.increase_value_fixed_entry = ttk.Entry(
            self.inputs_frame, textvariable=self.increase_value_fixed_var
        )

        self._on_payment_type_change()

    def _wire_change_events(self):
        watched_vars = (
            self.strategy_var,
            self.payment_type_var,
            self.fixed_amount_var,
            self.start_amount_var,
            self.increase_frequency_months_var,
            self.increase_type_var,
            self.increase_value_percent_var,
            self.increase_value_fixed_var,
        )
        for var in watched_vars:
            var.trace_add("write", self._on_option_changed)

        # If there are issue with events not firing, add bind for <KeyRelease> on entries and
        # <<ComboboxSelected>> on combobox, and call self._on_option_changed from those handlers as
        # well.
        self.increase_type_combo.bind(
            "<<ComboboxSelected>>", self._on_increase_type_change
        )

    def _on_option_changed(self, *_):
        # Schedule options changed event with debounce
        if self._suspend_events:
            return

        if self._options_change_job is not None:
            self.after_cancel(self._options_change_job)

        self._options_change_job = self.after(300, self._emit_options_changed)

    def _emit_options_changed(self):
        self._options_change_job = None
        self.event_bus.publish(Events.SIM_OPTIONS_CHANGED, options=self.get_options())

    def _hide_all_payment_inputs(self):
        for widget in (
            self.fixed_amount_label,
            self.fixed_amount_entry,
            self.start_amount_label,
            self.start_amount_entry,
            self.frequency_label,
            self.frequency_spinbox,
            self.increase_type_label,
            self.increase_type_combo,
        ):
            widget.grid_remove()

        self._hide_all_increase_value_inputs()

    def _hide_all_increase_value_inputs(self):
        for widget in (
            self.increase_value_percent_label,
            self.increase_value_percent_entry,
            self.increase_value_fixed_label,
            self.increase_value_fixed_entry,
        ):
            widget.grid_remove()

    def _on_payment_type_change(self):
        self._hide_all_payment_inputs()

        if self.payment_type_var.get() == "fixed":
            self.fixed_amount_label.grid(
                row=0, column=0, sticky="w", padx=(0, 8), pady=2
            )
            self.fixed_amount_entry.grid(row=0, column=1, sticky="ew", pady=2)
        else:
            self.start_amount_label.grid(
                row=0, column=0, sticky="w", padx=(0, 8), pady=2
            )
            self.start_amount_entry.grid(row=0, column=1, sticky="ew", pady=2)

            self.frequency_label.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=2)
            self.frequency_spinbox.grid(row=1, column=1, sticky="ew", pady=2)

            self.increase_type_label.grid(
                row=2, column=0, sticky="w", padx=(0, 8), pady=2
            )
            self.increase_type_combo.grid(row=2, column=1, sticky="ew", pady=2)

            self._on_increase_type_change()  # Trigger increase type change to show correct inputs

        self._on_option_changed()  # Trigger options changed when payment type changes

    def _on_increase_type_change(self, *_):
        self._hide_all_increase_value_inputs()

        if self.increase_type_var.get() == "percent":
            self.increase_value_percent_label.grid(
                row=3, column=0, sticky="w", padx=(0, 8), pady=2
            )
            self.increase_value_percent_entry.grid(row=3, column=1, sticky="ew", pady=2)

        elif self.increase_type_var.get() == "fixed":
            self.increase_value_fixed_label.grid(
                row=3, column=0, sticky="w", padx=(0, 8), pady=2
            )
            self.increase_value_fixed_entry.grid(row=3, column=1, sticky="ew", pady=2)

    def get_options(self) -> dict:
        options = {}
        options["strategy"] = self.strategy_var.get()

        if self.payment_type_var.get() == "fixed":
            options["payment_type"] = "fixed"
            options["fixed_amount"] = self.fixed_amount_var.get()
        else:
            options["payment_type"] = "increasing"
            options["start_amount"] = self.start_amount_var.get()
            options["increase_frequency_months"] = (
                self.increase_frequency_months_var.get()
            )
            options["increase_type"] = self.increase_type_var.get()
            if options["increase_type"] == "percent":
                options["increase_value"] = self.increase_value_percent_var.get()
            else:
                options["increase_value"] = self.increase_value_fixed_var.get()

        return options


class LoanRepaymentSimChartsFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.build()

    def build(self):
        label = ttk.Label(self, text="Charts (TODO)")
        label.pack(anchor="w")


class LoanRepaymentSimSummaryFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.build()

    def build(self):
        label = ttk.Label(self, text="Summary (TODO)")
        label.pack(anchor="w")


class LoanRepaymentSimAmortizationFrame(ttk.Frame, IUiComponent):
    def __init__(self, parent, bus: EventBus, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_bus = bus

        self.build()

    def build(self):
        label = ttk.Label(self, text="Amortization (TODO)")
        label.pack(anchor="w")
