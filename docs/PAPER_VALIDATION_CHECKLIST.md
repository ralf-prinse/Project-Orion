# PROJECT ORION — PAPER VALIDATION CHECKLIST

**Purpose:** Operational validation before enabling new functionality  
**Branch:** `feature-ibkr-integration`  
**Updated:** 2026-07-14

---

# Before Starting

Confirm:

- [ ] Correct Git branch
- [ ] Working tree is clean (runtime files excluded)
- [ ] Regression suite: **75 passed, 0 failed**
- [ ] TradingSession reset completed
- [ ] Cash = €10,000
- [ ] Equity = €10,000
- [ ] Open positions = 0
- [ ] Position states = 0
- [ ] Risk plans = 0
- [ ] Runtime journals preserved
- [ ] Only one Orion runner is active

---

# Runtime Configuration

Current validation profile:

- [ ] Maximum 20 open positions
- [ ] Approx. €500 maximum position value
- [ ] Maximum 90% portfolio exposure
- [ ] Minimum cash reserve enforced
- [ ] Maximum holding time: 48 hours
- [ ] Fractional shares disabled
- [ ] Internal PaperBroker enabled
- [ ] Quote validation enabled
- [ ] Market session service enabled
- [ ] RuntimeSupervisor enabled

---

# Start Runner

```powershell
python run_continuous_paper_trading.py
```

Confirm:

- [ ] Runner starts successfully
- [ ] TradingSession loads
- [ ] RuntimeSupervisor starts
- [ ] No traceback
- [ ] No failed iteration

---

# Market Session Validation

If markets are closed:

- [ ] Runtime enters `MARKETS_IDLE`
- [ ] No scan starts
- [ ] No BUY decisions
- [ ] No portfolio updates
- [ ] No failed iterations
- [ ] Next market-open check is scheduled

If markets are open:

- [ ] Market scan starts
- [ ] Opportunity ranking completes
- [ ] Decision journal receives entries

---

# Quote Validation

Verify invalid prices are rejected:

- [ ] None
- [ ] NaN
- [ ] Infinity
- [ ] Zero
- [ ] Negative values

Verify:

- [ ] Previous valid price is preserved
- [ ] Portfolio equity remains finite
- [ ] Runtime continues

---

# First BUY

Confirm:

- [ ] BUY decision exists
- [ ] Allocation approved
- [ ] Quantity > 0
- [ ] Cash decreases
- [ ] PaperPosition created
- [ ] PositionState created
- [ ] RiskPlan created
- [ ] UTC timestamp stored
- [ ] Trade journal updated

---

# Position Management

Verify:

- [ ] Current price updates
- [ ] Highest price only increases
- [ ] Initial stop active
- [ ] Break-even activates
- [ ] Trailing stop updates
- [ ] Target flags update
- [ ] Restart preserves lifecycle state

---

# First SELL

Confirm:

- [ ] Exit reason recorded
- [ ] Position removed
- [ ] PositionState removed
- [ ] RiskPlan removed
- [ ] Cash updated
- [ ] CLOSE_POSITION recorded
- [ ] Realized P&L stored

---

# Runtime Shutdown

Stop using:

```powershell
Ctrl+C
```

Verify:

- [ ] TradingSession saved
- [ ] Runtime stopped cleanly
- [ ] Journals preserved

---

# Validation Report

Record:

- completed iterations;
- failed iterations;
- BUY decisions;
- executed trades;
- rejected opportunities;
- open positions;
- cash;
- equity;
- realized P&L;
- unrealized P&L;
- runtime warnings;
- runtime exceptions.

---

# Freeze Rule

During validation:

- Do not modify indicators.
- Do not modify strategy logic.
- Do not modify exit rules.
- Do not modify ranking.
- Only fix critical runtime defects after stopping the runner.

---

# Completion

Before committing:

```powershell
python run_tests.py
git status -sb
```

Only commit when:

- regression suite passes;
- runtime behaved correctly;
- validation evidence is preserved.