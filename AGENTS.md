# demo-ledger-service

Pure-Python fund ledger library (settlement dates, fees, invoices, day counts,
positions, realised P&L). No I/O, no framework, no runtime dependencies.

- Setup: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- Test: `pytest -q` (CI runs the same on Python 3.12).
- Code lives in `ledger/`; tests in `tests/`, one file per module.
- The README "Accounting conventions" section is authoritative. When code and
  README disagree, the README is right. Do not change settlement, fee,
  position or P&L semantics without updating it.
- Money is always `decimal.Decimal`, never floats; round to the cent with
  round half up.
- Consumers pin Git tags (`eventflow-order-service` uses `ledger.settlement`,
  `eventflow-payment-service` uses `ledger.fees`); treat public function
  signatures as a stable API.
- Releases: follow the `release` skill in `.agents/skills/release/SKILL.md`.
