# PROJECT ORION — PAPER VALIDATION CHECKLIST

**Branch:** `validation-mode-v1`  
**Version:** `v0.9-paper-validation`

## Voor de start

- [ ] Branch is `validation-mode-v1`
- [ ] Git working tree is clean
- [ ] Regressie: `75 passed`, `0 failed`
- [ ] Cash: €10.000
- [ ] Equity: €10.000
- [ ] Open posities: 0
- [ ] Position states: 0
- [ ] Risk plans: 0
- [ ] Session status: ACTIVE
- [ ] Er draait nog geen andere Python-runner

## Actieve configuratie

- [ ] Maximaal 20 open posities
- [ ] Maximaal €500 per positie
- [ ] Maximaal 5% per positie
- [ ] Maximaal 90% portfolio-exposure
- [ ] Minimaal 10% cashreserve
- [ ] Maximaal 48 verstreken uren per positie
- [ ] Maximaal 150 gescande symbolen
- [ ] Fractionele aandelen uitgeschakeld
- [ ] Broker: interne PaperBroker

## Starten

```powershell
python run_continuous_paper_trading.py

Eerste cyclus
 Runner start zonder traceback
 Bestaande TradingSession wordt geladen
 Market scan wordt voltooid
 Decision journal krijgt entries
 Runtime event log krijgt entries
 Geen failed iterations
Eerste BUY
 BUY-beslissing aanwezig
 Opportunity ranking aanwezig
 Allocation goedgekeurd
 Quantity groter dan 0
 Cash wordt correct verminderd
 PaperPosition wordt aangemaakt
 PositionState wordt aangemaakt
 RiskPlan wordt aangemaakt
 opened_at wordt in UTC opgeslagen
 OPEN_POSITION staat in het trade journal
Positiebeheer
 Current price wordt bijgewerkt
 Highest price beweegt alleen omhoog
 opened_at blijft ongewijzigd
 Initial stop werkt
 Break-even werkt
 Trailing stop werkt
 Target-flags worden bijgewerkt
 Restart behoudt alle state
Eerste SELL
 Exitreden wordt geregistreerd
 Actie is STOP_LOSS, TAKE_PROFIT of MAX_HOLDING_TIME
 Positie wordt verwijderd
 PositionState wordt verwijderd
 RiskPlan wordt verwijderd
 Cash wordt verhoogd
 CLOSE_POSITION staat in het trade journal
 Realized P&L wordt geregistreerd
Einde handelsdag

Noteer:

totaal aantal cycli;
failed cycles;
BUY-beslissingen;
uitgevoerde aankopen;
uitgevoerde verkopen;
afgewezen kandidaten;
open posities;
cash;
equity;
realized P&L;
unrealized P&L;
gebruikte exitredenen;
fouten en waarschuwingen.
Freeze-regel

Tijdens de eerste validatierun:

geen entrylogica wijzigen;
geen exitpercentages wijzigen;
geen indicatoren toevoegen;
geen ranking aanpassen;
alleen kritieke runtimebugs oplossen nadat de runner is gestopt.
Stoppen

Stop gecontroleerd met:

Ctrl+C

Controleer daarna dat de sessie is opgeslagen en bewaar alle journals.


Commit en push:

```powershell
git add docs\PAPER_VALIDATION_CHECKLIST.md
git commit -m "Add paper validation run checklist"
git push

Controleer ten slotte:

git status -sb