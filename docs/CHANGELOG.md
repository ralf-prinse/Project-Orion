# CHANGELOG.md

## 2026-07-17 - Atomic IBKR lifecycle price synchronization

Een tweede runnerstart kon na broker-sync veilig maar onterecht stoppen wanneer
de actuele `PaperPosition.current_price` al was vernieuwd en de persistente
`PositionState.current_price` nog de vorige cyclusprijs bevatte. De sync werkt
nu beide waarden atomair bij en verhoogt zo nodig ook `highest_price`.

De premature session-save direct na idempotente adoptie is verwijderd; opslag
vindt plaats nadat lifecycle-state en brokerportfolio consistent zijn. De
integriteitscontrole blijft ongewijzigd streng en orderuitvoering vindt nog
steeds pas daarna plaats.

## 2026-07-17 - Fail-closed IBKR EXIT_ONLY mode

De autonome runner ondersteunt nu expliciet `EXIT_ONLY` en `BUY_AND_SELL`.
De IBKR-entrypoint kiest standaard `EXIT_ONLY`; in die modus worden scanner,
allocator en BUY-execution geheel overgeslagen, terwijl broker-sync,
positieadoptie, lifecycle-updates en de canonieke managed SELL-keten actief
blijven. Een afzonderlijke teller rapporteert werkelijk uitgevoerde exits.

De interactieve bevestiging benoemt de gekozen modus. `BUY_AND_SELL` vereist
zowel een expliciete environmentconfiguratie als de bestaande bevestiging en
orderpermissie. De maximale positie-cap van de IBKR-configuratie is verhoogd
van 4 naar 20, maar blijft uitsluitend een bovengrens: cashreserve,
portfolio-exposure, positie-exposure, trade-risk, cumulatief risico en drawdown
blijven ongewijzigd leidend.

De lokale persistente IBKR sessie- en portefeuillebestanden zijn aan
`.gitignore` toegevoegd; ze blijven lokaal beschikbaar maar komen niet in Git.

## 2026-07-17 - EUR valuation, official calendars and position adoption

De autonome IBKR Paper runtime vereist nu EUR als account- en
portefeuillebasisvaluta. USD-posities en Amerikaanse BUY-kandidaten worden met
een gedeelde, gevalideerde USD/EUR-koers naar EUR omgerekend voor equity,
cashreserve, exposure en trade-/portefeuillerisico. Koersprijzen, stop-losses en
targets blijven in de noteringsvaluta zodat brokerorders en managed exits de
correcte marktprijs gebruiken. Wanneer alleen een fallback-FX-koers beschikbaar
is, stopt de IBKR-runtime fail-closed.

`MarketSessionService` gebruikt `exchange_calendars` voor XAMS, XETR en XNYS.
Daarmee worden beursvakanties, DST en verkorte handelsdagen door dezelfde
per-symbool BUY- en SELL-gate verwerkt.

De vier expliciet toegestane bestaande IBKR Paper-posities (`AAPL`, `AAL`,
`ASML.AS` en `ASM.AS`) kunnen gecontroleerd en idempotent worden geadopteerd.
Adoptie maakt een persistente `PositionState` en `RiskPlan` op basis van de
bestaande Orion stop-, target-, trailing-stop-, break-even- en time-stopconfig.
De audittrail vermeldt uitdrukkelijk dat de oorspronkelijke BUY-redenering niet
beschikbaar is; er wordt geen historische handelsreden verzonnen. Na adoptie
loopt een SELL via dezelfde canonieke managed-exit- en IBKR Paper-keten.

Orderinzending blijft standaard uitgeschakeld.

## 2026-07-17 - Persistent EU/US IBKR Paper runtime foundation

De canonieke autonome IBKR Paper factory ondersteunt nu persistente opslag van
de volledige `TradingSession` en `PaperPortfolio`. Daardoor blijven onder
andere positielevenscyclus, stopplannen en de portfolio-high-watermark over
afzonderlijke runnerstarts behouden.

De BUY-scanner en managed SELL-keten controleren per symbool de reguliere
marktsessie. Gesloten Amerikaanse of Europese markten veroorzaken geen
orderpoging. Een gecombineerde, beperkte IBKR-validatiewatchlist bevat zowel
Amerikaanse als Euronext-symbolen.

IBKR-symbolen zonder Yahoo-marktsuffix worden bij synchronisatie teruggekoppeld
naar een reeds bekend, eenduidig Orion-symbool. Zo blijft bijvoorbeeld een door
Orion geopende `ASML.AS`-positie na broker-sync gekoppeld aan haar bestaande
`PositionState` en `RiskPlan`.

Orderinzending blijft standaard uitgeschakeld. Valuta-normalisatie voor een
gemengde EUR/USD-portefeuille, beursvakanties/verkorte handelsdagen en bewuste
adoptie van reeds bestaande brokerposities blijven activeringsvoorwaarden.

## 2026-07-17 - Portfolio-aware pre-order risk integration

### Canonical RiskManager gekoppeld

`services.risk.RiskManager` is als harde pre-order-gate gekoppeld aan
`PortfolioAllocator`.

De allocator toetst nu voor iedere voorgestelde BUY:

- risico per trade op basis van quantity, entry en stop-loss;
- cumulatief risico van bestaande en eerder goedgekeurde posities;
- persistente portfolio drawdown vanaf de high-watermark;
- minimale cashreserve;
- positie- en totale portfolio-exposure.

Posities zonder beheerde `RiskPlan` blokkeren nieuwe allocaties fail-closed,
met een expliciete afwijzingsreden. De bestaande IBKR BUY-, SELL-,
synchronisatie- en managed-exitketen blijft ongewijzigd. Live trading en
zelfstandige AI/learning-aanpassingen zijn niet geactiveerd.

### Risk observability gekoppeld

De pre-order risk-uitkomsten worden nu als immutable snapshots opgenomen in
het bestaande decision journal. Daardoor zijn onder andere risk allowed,
trade-risico, cumulatief portefeuillerisico, drawdown, cashreserve,
positie-exposure en de volledige redenen/waarschuwingen historisch auditbaar.

De bestaande `RuntimeSupervisor` neemt aantallen risk-evaluaties en
afwijzingen op in runtime health en runtime events. `DashboardService` leest
het decision journal en projecteert de resultaten naar de bestaande CLI- en
GUI-tradingdashboards. De autonome IBKR Paper runtime krijgt hiervoor een
afzonderlijk decision journal; trade-events en decision-events blijven
gescheiden.

## 2026-07-17

### IBKR Paper Trading volledig operationeel

De complete end-to-end IBKR Paper Trading workflow functioneert nu succesvol.

Werkende keten:

- Universe loading
- Yahoo Market Data
- Indicator Builder
- Trading Pipeline
- Signal Fusion
- Position Allocation
- Execution Engine
- IBKR Order Transport
- Broker Synchronization
- Portfolio Synchronization
- Autonomous Runner

---

### Broker Exit stabiliteit

De Autonomous Runner probeerde eerder exits uit te voeren voor broker-posities die niet door Orion werden beheerd.

Oplossing:

Brokerposities zonder `PositionState` of `RiskPlan` worden nu veilig overgeslagen.

Resultaat:

- geen crashes meer
- stabiele broker synchronisatie

---

### Yahoo ticker correctie

Yahoo ticker aangepast:

```
ASMI.AS
```

naar

```
ASM.AS
```

Hierdoor werkt marktdata voor ASM International correct.

---

### Position Allocation

Configuratie aangepast zodat ook aandelen met een hogere koers gekocht kunnen worden.

Hierdoor kan de Position Allocator correct orders aanmaken voor dure aandelen.

---

### IBKR Post-Fill Synchronisatie

Synchronisatie tussen Yahoo-symbolen en IBKR-symbolen verbeterd.

Voorbeeld:

```
Yahoo
ASM.AS

↓

IBKR
ASM
```

Resultaat:

De laatste synchronisatieproblemen na een BUY-order zijn opgelost.

---

### Eerste Repository Audit

Een eerste architectuuranalyse van Project Orion is uitgevoerd.

Belangrijkste conclusie:

Een aanzienlijk deel van de gewenste functionaliteit blijkt al aanwezig te zijn.

Onder andere gevonden:

- Trailing Stop
- Break Even
- Time Stop
- Exit Engine
- RiskPlan
- Dashboard
- Performance Analyse
- Trade Journal
- Position Monitoring
- Portfolio Management

De volgende ontwikkelfase richt zich daarom op het analyseren en activeren van bestaande modules in plaats van het ontwikkelen van nieuwe functionaliteit.

---

### Ontwikkelstrategie gewijzigd

De projectstrategie is aangepast.

Oude aanpak:

> Nieuwe functionaliteit ontwikkelen.

Nieuwe aanpak:

> Eerst de bestaande codebase volledig inventariseren, daarna alleen ontbrekende functionaliteit bouwen.

Dit voorkomt dubbele implementaties en maakt maximaal gebruik van de bestaande Orion-architectuur.
