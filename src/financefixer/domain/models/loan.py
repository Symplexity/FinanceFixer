from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Loan:
    name: str
    principal_cents: int
    annual_rate: float
    min_payment_cents: int
    as_of_date: datetime = field(default_factory=datetime.now)
    id: int | None = None

    def __post_init__(self):
        if self.principal_cents < 0:
            raise ValueError("Principal cannot be negative")
        if self.annual_rate < 0:
            raise ValueError("Annual rate cannot be negative")
        if self.min_payment_cents < 0:
            raise ValueError("Minimum payment cannot be negative")

        if isinstance(self.as_of_date, str):
            self.as_of_date = datetime.fromisoformat(self.as_of_date)
        if not isinstance(self.as_of_date, datetime):
            raise ValueError(
                "as_of_date must be a datetime object or ISO format string"
            )

    def monthly_rate(self) -> float:
        return self.annual_rate / 12 / 100
