# CHANGELOG.md

## 2026-07-23 - MICRO_500 cost-adjusted recovery profile

De tweede volledige run sloot F netto EUR 3,02 negatief en KO netto EUR 1,87
negatief. Samen met de eerste run staat de geïsoleerde portefeuille op EUR
493,24. Het eerdere EUR 0,50-doel tegenover EUR 3 verlies vereiste een
onrealistische break-even winrate van 85,7% en is daarom niet behouden.

MICRO_500 gebruikt nu maximaal één positie van EUR 350, één entry per dag en
vijf per UTC-week. Alleen XUSA kan entries krijgen; Europa blijft onderdeel van
de scan maar wordt voor dit kleine kapitaal fail-closed geblokkeerd. Het
VS-nettodoel is EUR 4,50 tegenover EUR 3 maximaal nettoverlies, met minimaal
1,5 reward/risk. De kostenratio is begrensd op 0,6% en de maximaal benodigde
brutobeweging op 2,5%.

Nieuwe entries vereisen na een openingsbuffer van vijftien minuten een bullish
afgeronde 5-minutencandle, stijgende 15-minutentrend, koers boven sessie-VWAP,
voldoende relatief volume en positieve 15-minutensterkte tegenover SPY. De
laatste drie uren van de Amerikaanse sessie zijn voor nieuwe entries gesloten;
de tijdstop is 180 minuten. Deze wijzigingen blijven uitsluitend SHADOW en
activeren geen IBKR-orderpad.

## 2026-07-22 - Net shadow accounting and empirically feasible micro targets

De eerste volledige MICRO_500-run bleek bruto EUR 0,54 positief maar na EUR
2,39 geraamde kosten EUR 1,86 negatief. Shadowexits trekken round-tripkosten nu
werkelijk van cash af. Bij starten wordt de geïsoleerde microcash opnieuw
opgebouwd uit startkapitaal, completed nettoresultaten en open kostbasis. Nieuwe
trade-journaltimestamps zijn UTC-aware. De bestaande state is herstelbaar
geback-upt en gereconcilieerd naar EUR 498,14; 6.317 timestamps en twee
houdtijden zijn gecorrigeerd. De oude bruto peak equity is hersteld naar de
netto startbasis van EUR 500 zodat drawdown weer economisch klopt.

Analyse van 15.000 Amerikaanse en 20.357 Europese 90-minutenvensters toont dat
het oude doel meestal buiten de waargenomen beweging lag. Het netto microdoel
is daarom EUR 0,50 voor VS en EU en de maximale vereiste brutobeweging is
verlaagd naar 1,6%. Europese entries blijven bij de huidige minimumcommissies
meestal terecht economisch geblokkeerd. Er is geen openingsbuffer toegevoegd:
de gemeten openingsvensters waren juist sterker dan latere vensters. De
verlieslimieten en tijdstop zijn na slechts twee trades bewust niet geoptimaliseerd.

Een vaste `start_orion_micro_shadow_full_day.ps1` voorkomt configuratiefouten
voor een volledige gezamenlijke EU/VS-shadowdag. De starter gebruikt 160 cycli
van 300 seconden, blijft hard op `MICRO_500`/`SHADOW` zonder ordertoestemming en
neemt het Paper-account uitsluitend als niet-gecommit parameter aan.

## 2026-07-21 - Isolated MICRO_500 capital profile

Een afzonderlijk `MICRO_500`-profiel simuleert voortaan het beoogde
startkapitaal van EUR 500 zonder de bestaande EUR 10.000-shadowportefeuille te
overschrijven. Het profiel is voorlopig uitsluitend toegestaan in `SHADOW`,
gebruikt eigen persistentiebestanden, maximaal twee posities, één nieuwe positie
per cyclus, twee entries per UTC-dag, 30% cashreserve en maximaal EUR 175 per
positie.

Kostenhaalbaarheid is nu een harde pre-ordergate. Round-tripkosten omvatten ook
een configureerbaar aandeel van toekomstige maandelijkse marktdata-abonnementen.
Het microprofiel weigert posities boven 2% geraamde retourkosten of wanneer
kosten, nettowinstdoel en onzekerheidsbuffer meer dan 3% brutobeweging vereisen.
TIERED is de profieldefault; daadwerkelijke IBKR commission reports blijven
vereist vóór Paper-orders of live-moneyontwerp.

De lifecycle kent daarnaast een algemene dagelijkse entrylimiet, symbol-based
herinstap-cooldown en een optionele minutennauwkeurige tijdstop. `MICRO_500`
gebruikt EUR 2,50/3,50 netto winstdoelen voor VS/EU, EUR 3/4 netto verlieslimiet,
60 minuten cooldown, 90 minuten maximale houdtijd en 1,5% dagelijks verlies.
Een eerder netwerkafhankelijke FX-test gebruikt nu een vaste testfixture.

De expliciete runnerlimiet is verhoogd van 96 naar 200 cycli. Bij het aanbevolen
5-minuteninterval kan één bevestigde run daarmee ongeveer 16 uur en 35 minuten
draaien. De bovengrens blijft als bescherming tegen typefouten en onbedoeld
praktisch eindeloze interactieve runs bestaan.

`MICRO_500` gebruikt nu daadwerkelijk `5d/5m`-historie in plaats van de
standaard `3mo/1d`-swingdata. De intradayketen verwijdert de nog niet afgesloten
5-minutencandle, weigert een laatste volledige candle ouder dan vijftien minuten
na candle completion en gebruikt een cache-TTL van twee minuten. De leeftijd
wordt vanaf het einde van de candle gemeten; dit vangt de praktisch gemeten
Yahoo-publicatievertraging van ongeveer twaalf minuten op. Trend en momentum
hebben een 5-minutenschaal; volatiliteit wordt geannualiseerd met 78 vijfminutenperioden
per Amerikaanse handelsdag. Minder dan 21 volledige candles stopt fail-closed.
De standaard EUR 10.000-strategie behoudt dagcandles en dagelijkse schaling.

## 2026-07-20 - Isolated shadow trading and signal normalization

De autonome runtime kent nu een expliciete `SHADOW`-uitvoeringsmodus. Deze
modus weigert fail-closed te starten wanneer ordertoestemming aanstaat, bouwt
geen IBKR quote- of orderpad, synchroniseert of adopteert geen brokerposities en
gebruikt een afzonderlijke lokale portefeuille, sessie, decision journal, trade
journal en completed-trade store. Fictieve fills bewaren de auditeerbare Yahoo-
referentieprijs; adverse slippage, round-tripcommissies, externe kosten en FX-
buffers blijven expliciet in journal en completed-trade-resultaten staan.

De oorzaak van de onrealistische 50-uit-50 BUY-uitkomst is hersteld. De
trendindicator gebruikte `laatste prijs / gemiddelde`, waardoor vrijwel ieder
aandeel na begrenzing een trend van `+1` kreeg en een dalende trend niet kon
bestaan. Trend is nu de geschaalde, getekende afwijking van het 20-daags
gemiddelde. Volatiliteit wordt voortaan als geannualiseerd percentage aan de
downstream 0..100-normalisatie geleverd in plaats van als vrijwel nul gelezen
dagdecimaal.

Een configureerbare selectiviteitsgate vereist naast het actieve BUY-besluit
ook bevestiging door de onafhankelijke investment thesis, minimale conviction,
opportunity score, trend, momentum en pressure confirmation. Iedere afwijzing
wordt met de gemeten waarde en grens gejournaliseerd. De volledige testsuite
eindigt op 581 geslaagde tests en nul failures.

## 2026-07-19 - Execution-grade Paper safety controls

Nieuwe IBKR BUY-orders gebruiken actuele live bid/ask- en top-of-bookdata als
fail-closed execution gate. Verouderde, onvolledige, te brede of te dunne
quotes blokkeren de order met een expliciete reden. Normale BUY- en
winstnemingsorders worden als begrensde marketable limitorder verzonden;
urgente stop- en time-exits blijven marktgericht om risico af te bouwen.

Iedere Paper BUY wordt atomair als IBKR bracket verzonden met een parent,
profit-taker en broker-native stop-loss. Parent en children gebruiken de
voorgeschreven `Transmit`-volgorde. De children en iedere latere softwarematige
SELL delen een persistente trade-ID gebaseerde OCA-groep, zodat slechts één
exit kan vullen. IBKR-uitgevoerde protective children worden bij broker-sync
via `orderRef` teruggevonden en met de oorspronkelijke `trade_id`, fillprijs en
SELL-reden in trade memory opgeslagen. Een verdwenen positie zonder
reconcilieerbare execution stopt fail-closed.

De entryketen heeft daarnaast een sessiecircuitbreaker voor verlies,
opeenvolgende verliestrades en brokerfouten. Markt-, sector- en gecureerde
correlatieclusterlimieten beschermen tegen schijnspreiding. Alle 100 huidige
EU/VS-symbolen hebben versiebeheerde risicometadata. Een earningsinterface
blokkeert bekende events en verzint geen datum wanneer brondata ontbreekt.

`analyze_completed_trades.py` rapporteert alleen offline nettowachting na
geraamde kosten. Deze analyse heeft geen schrijfpad naar runtimeconfiguratie of
orders. Live-moneyaccounts blijven geblokkeerd en nieuws blijft SHADOW-only.

Tevens is hersteld dat de gegenereerde `trade_id` vóór het append-moment in de
BUY-journalregel wordt geplaatst, zodat entry en exit betrouwbaar tot één
completed trade worden samengevoegd.

## 2026-07-19 - Canonical runtime architecture cleanup

De actieve adaptieve decisioncomponenten zijn zonder strategiewijziging
verplaatst van de dubbelzinnige `services/decision`-namespace naar de expliciete
`services/trading_decision`-laag. `TradingPipeline` is de enige productie-eigenaar
van deze decision- en sizingcomponenten. Een architectuurtest bewaakt dat de
autonome IBKR-runtime geen research-decision- of learningservices activeert.

De kapotte directe `DecisionEngine`, ongebruikte adapter, oude `engines`-
scannerketen, lege runtime- en mapperplaceholders, een dubbel leeg decision-
modelbestand en lege schijntests zijn verwijderd. Het lege
`strategy_variant_proposal`-contract is vervangen door het reeds bestaande
gelijknamige model in `models.strategy_variant`.

Verouderde regressiefixtures zijn afgestemd op de huidige EUR-FX-mapping,
`TradeJournalEntry` en `PerformanceAnalysisResult`. Persistentie blijft terecht
eigendom van repositories/runners en niet van `PaperTradingService`. De volledige
testsuite eindigt na deze cleanup op 555 geslaagde tests en nul failures.

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
`ORION_IBKR_CYCLES` (destijds maximaal 96; huidig maximum 200) en
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
