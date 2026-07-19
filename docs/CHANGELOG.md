# CHANGELOG.md

## 2026-07-19 - Headless runtime, IBKR news shadow mode and trade memory

De ongebruikte Qt-desktop-GUI, bijbehorende tests en `PySide6`-dependency zijn
verwijderd. De tekstuele dashboardpresenter blijft beschikbaar onder de
neutrale `presentation`-laag. TWS blijft de operationele broker-GUI.

Een provider-onafhankelijke nieuwslaag kan via de IBKR API recente headlines
voor open posities en de hoogst gerangschikte BUY-kandidaten ophalen,
normaliseren, dedupliceren en persistent beoordelen. De eerste modus is alleen
`SHADOW`: nieuwscontext en een hypothetische blokkeerindicatie worden
gejournaliseerd, maar veranderen geen BUY, SELL, quantity, RiskPlan of order.
Providerfouten leveren `UNAVAILABLE` op en onderbreken de handelsketen niet.

Iedere geopende of geadopteerde positie krijgt een persistente `trade_id`. Na
een volledig bevestigde exit wordt één idempotent `CompletedTradeRecord`
opgeslagen met entryreden, exitreden, regime, confidence, nieuwscontext,
holdingduur, bruto P&L, geraamde kosten en netto-P&L. Bij adoptie blijft
expliciet dat de oorspronkelijke BUY-redenering onbekend is. Dit bereidt latere
offline learning voor; learningservices wijzigen nog geen handelsparameters.

## 2026-07-19 - Cost-aware small-profit Paper exits

De autonome IBKR Paper-runner kan beheerde posities nu sluiten op een geschatte
netto-opbrengst in EUR in plaats van uitsluitend op het laatste procentuele
winstdoel. De nieuwe `COST_AWARE_SMALL_PROFIT`-modus raamt de volledige
round-tripkosten uit het gekozen IBKR-prijsmodel, commissie-minima, een
configureerbare slippagebuffer, externe kosten en optionele EUR/USD-conversie.

De conservatieve Paper-defaults zijn EUR 5 netto winst / EUR 8 netto verlies
voor Amerikaanse aandelen en EUR 10 netto winst / EUR 15 netto verlies voor
Europese aandelen. De oorspronkelijke dynamische lifecycle-stop blijft de
hoogste-prioriteit veiligheidsgrens. `SWING` blijft beschikbaar als expliciete
fallback. De IBKR-runner start kostengevoelig met prijsmodel `FIXED`; beide zijn
overschrijfbaar via `ORION_IBKR_EXIT_STRATEGY` en
`ORION_IBKR_PRICING_PLAN`.

Exitredenen en journalregels bevatten de geschatte round-tripkosten en netto
P&L. Dit zijn bewust conservatieve ramingen: de IBKR-transportlaag ontvangt nog
geen definitief commission report en Yahoo levert geen executeerbare bid/ask.
Daarom blijft deze functie uitsluitend onderdeel van gecontroleerde Paper-
validatie.

## 2026-07-19 - 100-symbol bounded IBKR Paper scanning

De autonome IBKR Paper-runner gebruikt nu een gecureerd validatie-universum van
100 liquide aandelen: 50 Verenigde Staten, 25 Euronext Amsterdam en 25 Xetra.
Alleen symbolen waarvan de officiële beurs open is worden gedownload en door de
pipeline verwerkt.

De bestaande `YahooHistoricalDataProvider` is beoordeeld, gerepareerd en als
canonieke batchlaag gekoppeld. Open symbolen worden in batches van 25 opgehaald
en 15 minuten persistent gecachet. De positieprijs- en broker-syncpaden blijven
ongewijzigd fail-closed werken.

Een begrensde multi-cycle Paper-sessie kan expliciet worden ingesteld via
`ORION_IBKR_CYCLES` (maximaal 96) en
`ORION_IBKR_SCAN_INTERVAL_SECONDS` (60-3600; standaard 900). De runner wacht nu
daadwerkelijk tussen cycli en vereist bij meerdere cycli een bevestiging met het
exacte aantal. Per cyclus mogen maximaal drie nieuwe posities worden geopend;
de bestaande cap van 20 en alle portefeuille-risicolimieten blijven gelden.

Xetra-symbolen (`.DE`) worden voor IBKR SMART-routing vertaald naar een EUR
contract met `IBIS` als primary exchange en na broker-sync weer eenduidig naar
het Orion/Yahoo-symbool hersteld.

## 2026-07-17 - Explicit execution-rejection observability

Een door risico goedgekeurde trade die later door de uitvoeringslaag wordt
geblokkeerd, wordt nu afzonderlijk als `EXECUTION_REJECTED` met de concrete
broker- of permissiereden in het beslisjournaal vastgelegd. De runnersamenvatting
splitst allocatie- en uitvoeringsafwijzingen, en SAFE MODE toont BUY en SELL
expliciet als `DISABLED`.

## 2026-07-17 - Post-fill cash ordering and IBKR log privacy

De broker-truthsync leest de IBKR-accountwaarden nu pas nadat de verwachte
post-fill positiehoeveelheid zichtbaar is. Dit voorkomt dat een al bevestigde
SELL wordt gecombineerd met een accountsummary die vlak vóór die fill was
opgevraagd. Een regressietest simuleert expliciet een oud cashsaldo vóór en het
bijgewerkte saldo ná de bevestigende positielijst.

Bevestigde brokerexits converteren `invested_amount` en gerealiseerde P&L nu
met de gevalideerde positie-FX-koers naar de EUR-portefeuillebasis. Entry- en
fillprijzen blijven terecht in de noteringsvaluta van het instrument.

Orions orderlog maskeert het Paper-account voortaan ook bij orderinzending. De
zeer uitvoerige `ibapi` INFO-protocoldumps zijn gedempt omdat daarin het volledige
accountveld van een order kon verschijnen; waarschuwingen en fouten blijven
zichtbaar.

## 2026-07-17 - IBKR managed-account handshake race fix

De ordertransportlaag behoudt nu een geldige `managedAccounts`-callback die
TWS direct na `startApi` kan sturen. Orion wist deze vroege accountlijst niet
meer voordat de accountgate wordt uitgevoerd en vraagt de lijst alleen opnieuw
op wanneer nog geen callback is ontvangen. Daarmee blijft de harde controle op
het geconfigureerde Paper-account intact zonder de callbackvolgorde uit de
praktijk onterecht als `Returned accounts: none` af te wijzen.

Een regressietest bootst exact deze vroege callbackvolgorde na en verifieert dat
de accountcontrole vóór orderplaatsing slaagt. Accountnummers worden bovendien
gemaskeerd in transportlogs en foutmeldingen.

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
