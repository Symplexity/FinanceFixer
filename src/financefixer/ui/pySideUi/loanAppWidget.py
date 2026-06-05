from PySide6 import QtWidgets


class LoanAppWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.main = QtWidgets.QVBoxLayout(self)

        # Loan section
        self.loan_layout = QtWidgets.QGridLayout()
        self.main.addLayout(self.loan_layout)

        # Labels and inputs
        self.name_label = QtWidgets.QLabel("Name:")
        self.name_input = QtWidgets.QLineEdit()

        self.principal_label = QtWidgets.QLabel("Principal ($):")
        self.principal_input = QtWidgets.QDoubleSpinBox()
        self.principal_input.setDecimals(2)

        self.interest_label = QtWidgets.QLabel("Annual Interest Rate (%):")
        self.interest_input = QtWidgets.QDoubleSpinBox()
        self.interest_input.setDecimals(2)
        self.interest_input.setRange(0, 100)

        self.min_payment_label = QtWidgets.QLabel("Minimum Payment ($):")
        self.min_payment_input = QtWidgets.QDoubleSpinBox()
        self.min_payment_input.setDecimals(2)

        self.add_loan_button = QtWidgets.QPushButton("Add Loan")

        self.loan_layout.addWidget(self.name_label, 0, 0)
        self.loan_layout.addWidget(self.name_input, 0, 1)
        self.loan_layout.addWidget(self.principal_label, 1, 0)
        self.loan_layout.addWidget(self.principal_input, 1, 1)
        self.loan_layout.addWidget(self.interest_label, 2, 0)
        self.loan_layout.addWidget(self.interest_input, 2, 1)
        self.loan_layout.addWidget(self.min_payment_label, 3, 0)
        self.loan_layout.addWidget(self.min_payment_input, 3, 1)
        self.loan_layout.addWidget(self.add_loan_button, 4, 0, 1, 2)

        self.get_layout = QtWidgets.QGridLayout()
        self.main.addLayout(self.get_layout)

        self.get_loan_id_label = QtWidgets.QLabel("Loan ID:")
        self.get_loan_id_input = QtWidgets.QSpinBox()

        self.get_loan_button = QtWidgets.QPushButton("Get Loan")

        self.get_layout.addWidget(self.get_loan_id_label, 0, 0)
        self.get_layout.addWidget(self.get_loan_id_input, 0, 1)
        self.get_layout.addWidget(self.get_loan_button, 1, 0, 1, 2)
