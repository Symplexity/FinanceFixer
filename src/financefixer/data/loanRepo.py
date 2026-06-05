from financefixer.data.base import get_connection
from financefixer.data.schema import init_db
from financefixer.domain.models.loan import Loan


class LoanRepo:
    def __init__(self):
        init_db()

    def insert_loan(self, loan: Loan) -> Loan:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM loans ORDER BY id")
            existing_ids = {row[0] for row in cur.fetchall()}

            next_id = 1
            while next_id in existing_ids:
                next_id += 1

            cur.execute(
                """
            INSERT INTO loans (id, name, principal_cents, annual_rate, min_payment_cents, as_of_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    next_id,
                    loan.name,
                    loan.principal_cents,
                    loan.annual_rate,
                    loan.min_payment_cents,
                    loan.as_of_date,
                ),
            )
            loan.id = next_id
            conn.commit()
        return loan

    def get_loan(self, loan_id: int) -> Loan:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, principal_cents, annual_rate, min_payment_cents, as_of_date FROM loans WHERE id = ?",
                (loan_id,),
            )
            row = cur.fetchone()
            if row:
                return Loan(**row)
            else:
                raise ValueError(f"Loan with id {loan_id} not found")

    def get_all_loans(self) -> list[Loan]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, principal_cents, annual_rate, min_payment_cents, as_of_date FROM loans"
            )
            rows = cur.fetchall()
            return [Loan(**row) for row in rows]

    def update_loan(self, loan: Loan) -> bool:
        if loan.id is None:
            raise ValueError("Loan must have an id to be updated")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
            UPDATE loans
            SET name = ?, principal_cents = ?, annual_rate = ?, min_payment_cents = ?, as_of_date = ?
            WHERE id = ?
            """,
                (
                    loan.name,
                    loan.principal_cents,
                    loan.annual_rate,
                    loan.min_payment_cents,
                    loan.as_of_date,
                    loan.id,
                ),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_loan(self, loan_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM loans WHERE id = ?", (loan_id,))
            conn.commit()
            return cur.rowcount > 0
