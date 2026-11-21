from datetime import date, timedelta

import pytest

from ledger.markets import UnknownMarketError
from ledger.settlement import is_settled, settlement_date


def test_settlement_t_plus_one_us_equity():
    # Friday trade, T+1 lands on Monday.
    assert settlement_date(date(2026, 3, 6), "XNYS") == date(2026, 3, 9)


def test_settlement_t_plus_two_spans_weekend():
    # Thursday trade in London, T+2 skips Saturday and Sunday.
    assert settlement_date(date(2026, 3, 5), "XLON") == date(2026, 3, 9)


def test_settlement_skips_market_holiday():
    # Thursday 27 Aug 2026 in London. Monday 31 Aug is the Summer bank holiday,
    # so T+2 is Tuesday 1 Sep, not Monday 31 Aug.
    assert settlement_date(date(2026, 8, 27), "XLON") == date(2026, 9, 1)


def test_is_settled_on_and_after_settlement_date():
    trade = date(2026, 3, 6)
    assert not is_settled(trade, "XNYS", date(2026, 3, 8))
    assert is_settled(trade, "XNYS", date(2026, 3, 9))
    assert is_settled(trade, "XNYS", date(2026, 3, 10))


@pytest.mark.parametrize(
    ("trade", "next_business_day"),
    [
        # Monday to Thursday: the next business day is the next calendar day.
        (date(2026, 3, 2), date(2026, 3, 3)),
        (date(2026, 3, 5), date(2026, 3, 6)),
        # Friday: settles Monday, not Saturday.
        (date(2026, 3, 6), date(2026, 3, 9)),
        # Thursday 2 Apr 2026: Friday 3 Apr is Good Friday, so settles Monday.
        (date(2026, 4, 2), date(2026, 4, 6)),
        # Wednesday 25 Nov 2026: Thursday 26 Nov is Thanksgiving.
        (date(2026, 11, 25), date(2026, 11, 27)),
    ],
)
def test_us_equity_settled_the_next_business_day(trade, next_business_day):
    # XNYS is T+1: a trade settles on the next business day, not the next calendar day.
    assert settlement_date(trade, "XNYS") == next_business_day
    assert not is_settled(trade, "XNYS", next_business_day - timedelta(days=1))
    assert is_settled(trade, "XNYS", next_business_day)


def test_unknown_market_raises():
    with pytest.raises(UnknownMarketError):
        settlement_date(date(2026, 3, 6), "XXXX")
