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

## Eén veilige observatiecyclus

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<YOUR_DU_PAPER_ACCOUNT_ID>"
$env:ORION_IBKR_EXECUTION_MODE="BUY_AND_SELL"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_CYCLES="1"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="900"

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
