import random
from datetime import date, timedelta

import pytest

from ledger.markets import UnknownMarketError, get_market, is_business_day
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


def _random_trading_day(market_code: str) -> date:
    market = get_market(market_code)
    start = date(2026, 1, 2)
    while True:
        day = start + timedelta(days=random.randrange(180))
        if is_business_day(day, market):
            return day


def test_us_equity_settled_the_next_day():
    # XNYS is T+1: a trade is settled by the day after it was executed.
    trade = _random_trading_day("XNYS")
    assert is_settled(trade, "XNYS", trade + timedelta(days=1))


def test_unknown_market_raises():
    with pytest.raises(UnknownMarketError):
        settlement_date(date(2026, 3, 6), "XXXX")
