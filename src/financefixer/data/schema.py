from financefixer.data.base import get_connection


def init_db():
    with get_connection() as conn:
        loans_schema = """
        CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        principal_cents INTEGER NOT NULL,
        annual_rate REAL NOT NULL,
        min_payment_cents INTEGER NOT NULL,
        as_of_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""

        payments_schema = """
        CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY,
        loan_id INTEGER NOT NULL,
        amount_cents INTEGER NOT NULL,
        payment_ts TEXT NOT NULL,
        FOREIGN KEY (loan_id) REFERENCES loans (id) ON DELETE CASCADE
        );"""

        conn.execute(loans_schema)
        conn.execute(payments_schema)
        conn.commit()
