from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Currency(Enum):
    KRW = "KRW"
    USD = "USD"
    JPY = "JPY"


class PaymentMethod(Enum):
    OA = "OA"
    TT = "TT"


@dataclass(frozen=True)
class Sale:
    currency: Currency
    amount: Decimal
    payment_method: PaymentMethod
    collection_day: int


@dataclass(frozen=True)
class ForeignPayable:
    currency: Currency
    amount: Decimal
    payment_day: int


@dataclass(frozen=True)
class KrwCost:
    amount_krw: Decimal
    payment_day: int


@dataclass(frozen=True)
class DealCase:
    sale: Sale
    foreign_payables: tuple[ForeignPayable, ...]
    krw_costs: tuple[KrwCost, ...]
    available_cash_krw: Decimal
    annual_funding_rate: Decimal
    target_margin: Decimal


@dataclass(frozen=True)
class FxRates:
    usd_krw: Decimal
    jpy_krw_per_100: Decimal

    def to_krw(self, amount: Decimal, currency: Currency) -> Decimal:
        if currency is Currency.KRW:
            return amount
        if currency is Currency.USD:
            return amount * self.usd_krw
        if currency is Currency.JPY:
            return amount * self.jpy_krw_per_100 / Decimal("100")
        raise ValueError(f"Unsupported currency: {currency}")


def reference_deal() -> DealCase:
    return DealCase(
        sale=Sale(
            currency=Currency.USD,
            amount=Decimal("100000"),
            payment_method=PaymentMethod.OA,
            collection_day=90,
        ),
        foreign_payables=(
            ForeignPayable(Currency.USD, Decimal("20000"), 30),
            ForeignPayable(Currency.JPY, Decimal("3000000"), 30),
        ),
        krw_costs=(
            KrwCost(Decimal("30000000"), 0),
            KrwCost(Decimal("25000000"), 30),
            KrwCost(Decimal("9000000"), 60),
        ),
        available_cash_krw=Decimal("50000000"),
        annual_funding_rate=Decimal("0.048"),
        target_margin=Decimal("0.14"),
    )


def reference_fx() -> FxRates:
    return FxRates(
        usd_krw=Decimal("1400"),
        jpy_krw_per_100=Decimal("900"),
    )
