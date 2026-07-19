# Orion IBKR Autonomous Paper Runbook

Laatste update: 19-07-2026

## Veiligheidsgrens

Deze runtime ondersteunt uitsluitend een IBKR Paper-account met `DU`-prefix.
Live-moneyaccounts zijn niet toegestaan. Begin na iedere code- of
universumwijziging met orders uitgeschakeld.

Actuele schaalconfiguratie:

- 100 symbolen: 50 VS, 25 Amsterdam en 25 Xetra;
- alleen open beurzen worden geanalyseerd;
- historische downloads in batches van 25;
- cache-TTL 15 minuten;
- maximaal 3 nieuwe posities per cyclus;
- maximaal 20 open posities totaal;
- standaard 1 cyclus en 900 seconden scaninterval.

Actuele exitconfiguratie:

- standaard `COST_AWARE_SMALL_PROFIT` voor deze IBKR Paper-runner;
- Amerikaanse posities: EUR 5 geschatte nettowinst, EUR 8 geschat nettoverlies;
- Europese posities: EUR 10 geschatte nettowinst, EUR 15 geschat nettoverlies;
- standaard prijsmodel `FIXED`, totdat het account aantoonbaar `TIERED` gebruikt;
- commissie, slippage, externe kosten en optionele valutaconversie worden
  conservatief geraamd;
- de bestaande dynamische stop-loss blijft altijd vóór de kleine-winstlogica
  gelden.

## Eén veilige observatiecyclus

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<YOUR_DU_PAPER_ACCOUNT_ID>"
$env:ORION_IBKR_EXECUTION_MODE="BUY_AND_SELL"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_CYCLES="1"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="900"
$env:ORION_IBKR_EXIT_STRATEGY="COST_AWARE_SMALL_PROFIT"
$env:ORION_IBKR_PRICING_PLAN="FIXED"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START ONE AUTONOMOUS IBKR PAPER CYCLE
```

## Begrensde observatiesessie

Onderstaand voorbeeld draait acht cycli met vijftien minuten ertussen. Dat is
ongeveer 1 uur en 45 minuten tussen de eerste en laatste starttijd.

```powershell
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_CYCLES="8"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="900"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START 8 AUTONOMOUS IBKR PAPER CYCLES
```

Stop een actieve sessie zo nodig met `Ctrl+C`. Schakel ordertoestemming pas in
nadat een veilige observatie de verwachte 100 symbolen, marktsluitingen,
afwijzingsredenen en risicometingen heeft getoond.

## Ordertoestemming

`ORION_IBKR_ALLOW_ORDERS="true"` kan echte IBKR Paper BUY- en SELL-orders
plaatsen. Gebruik dit eerst met één cyclus. De positiecap van 20 is alleen een
bovengrens; cashreserve, exposure, trade-risk, portefeuillerisico en drawdown
kunnen een veel lager aantal afdwingen.

Controleer in TWS welk prijsmodel werkelijk bij het account hoort. Alleen als
dat `Tiered` is, stel je in PowerShell het volgende in:

```powershell
$env:ORION_IBKR_PRICING_PLAN="TIERED"
```

Terugschakelen naar de oorspronkelijke swing-exits kan expliciet met:

```powershell
$env:ORION_IBKR_EXIT_STRATEGY="SWING"
```

De netto-P&L is in deze fase een kostenraming en geen definitief IBKR-
commission report. Gebruik de strategie daarom eerst met orders uitgeschakeld
en daarna uitsluitend op het `DU` Paper-account. Activeer haar niet op een
live-moneyaccount.
