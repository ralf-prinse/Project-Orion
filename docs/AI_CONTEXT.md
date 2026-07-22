# AI_CONTEXT.md

## Project
Project Orion

AI-gestuurd autonoom tradingplatform met ondersteuning voor:
- Backtesting
- Paper Trading
- IBKR Paper Trading
- Toekomstige Live Trading

Architectuur is modulair en production-ready. Nieuwe functionaliteit wordt uitsluitend toegevoegd via bestaande services en niet via tijdelijke oplossingen.

---

# Huidige status

Project Orion heeft nu een volledig werkende end-to-end IBKR Paper Trading pipeline.

De runtime is headless: de eigen Qt-GUI is verwijderd en TWS is de operationele
brokerinterface. Nieuwsintelligentie is gekoppeld als IBKR `SHADOW`-
observatielaag en heeft geen invloed op orders. Gesloten trades worden als één
record bewaard voor latere offline analyse; autonoom self-learning staat uit.

De echte Paper-uitvoeringslaag vereist actuele IBKR bid/askdata, begrenst normale
orders met marketable limits en verzendt BUY's met broker-native stop/profit
children. Een gedeelde trade-OCA-groep voorkomt dubbele SELL's tussen IBKR en
Orions softwarematige lifecycle. Native fills worden teruggelezen naar dezelfde
trade memory.

Zonder betaald realtime-abonnement kan Orion via execution mode `SHADOW` een
volledig geïsoleerde fictieve portefeuille beheren. Deze modus kan geen IBKR-
quote of orderpad activeren, gebruikt aparte persistentie en verwerkt Yahoo-
referentieprijzen met conservatieve slippage en geraamde round-tripkosten.

Kapitaalprofiel `MICRO_500` is uitsluitend aan execution mode `SHADOW`
toegestaan en gebruikt een eigen `data/orion_shadow_micro_500`-state. Het
profiel start met EUR 500, maximaal één positie, 30% cashreserve, maximaal
EUR 350 per positie, één entry per dag, drie per week, 240 minuten
re-entrycooldown en een 180-minuten tijdstop. Alleen XUSA is uitvoerbaar;
Europese symbolen blijven analyseerbaar maar worden voor micro-entry hard
geblokkeerd. Het Amerikaanse nettodoel is EUR 4,50 tegenover EUR 3,00 maximaal
nettoverlies. Kosten mogen maximaal 0,6% van de positie vragen en kosten plus
doel en buffer maximaal 2,5% brutobeweging.
De entryanalyse van dit profiel gebruikt vijf handelsdagen 5-minutencandles.
Een lopende candle wordt uitgesloten; de nieuwste volledige candle mag tijdens
een open sessie maximaal vijftien minuten na candle completion oud zijn. Deze
marge vangt de gemeten Yahoo-publicatievertraging op. Trend/momentum en
volatiliteitsannualisatie zijn intervalbewust. MICRO_500 vereist daarnaast een
bullish 5-minutentrigger, stijgende 15-minutentrend, koers boven sessie-VWAP,
relatief volume en positieve 15-minutensterkte tegenover SPY. Entries zijn de
eerste vijftien minuten en laatste drie uren van XUSA geblokkeerd. De
standaardconfiguratie blijft op `3mo/1d` en wordt niet door deze gates geraakt.

De vroegere structurele BUY-bias is gecorrigeerd: trend is nu een getekende
afwijking van het voortschrijdend gemiddelde en volatiliteit heeft de juiste
percentageschaal. Een tweede selectiviteitsgate vereist thesis-, ranking-,
trend-, momentum- en pressurebevestiging voordat allocatie mogelijk is.

Entryrisico omvat daarnaast een sessiecircuitbreaker, markt-/sector-/cluster-
concentratie en bekende earnings-events. Nettowachting wordt alleen offline
gerapporteerd en kan geen configuratie of order wijzigen.

Architectuurgrens: de actieve `TradingPipeline` gebruikt uitsluitend
`services.trading_decision`. `services/decisions` is research/explainability en
wordt niet door de autonome runner geïmporteerd. De oude `engines`- en
`ScannerService`-keten is verwijderd. De volledige suite telt 609 groene tests.

Werkend:

- Universe loading
- Yahoo market data
- IndicatorBuilder
- TradingPipeline
- SignalFusion
- PositionAllocator
- ExecutionEngine
- IBKR Order Transport
- IBKR Broker
- Order fills
- Broker synchronization
- Portfolio synchronization
- Autonomous runner

De volledige autonome cyclus draait succesvol zonder crashes.

Actuele IBKR Paper-schaalconfiguratie:

- 100-symbolenvalidatie-universum: 50 VS, 25 Amsterdam, 25 Xetra;
- officiële markturen bepalen welke subset per cyclus wordt verwerkt;
- historische Yahoo-data: batches van 25, cache-TTL 15 minuten;
- standaard één cyclus; begrensd configureerbaar tot 200 cycli;
- standaard scaninterval 900 seconden bij meerdere cycli;
- maximaal drie nieuwe posities per cyclus en twintig totaal;
- live-moneyaccounts blijven technisch geblokkeerd; alleen `DU` Paper-accounts.
- `MICRO_500` blijft shadow-only totdat voldoende nettoresultaten na kosten zijn
  verzameld en echte commission reports het kostenmodel valideren.

---

# Laatste grote fixes

## Broker exits

Autonomous runner probeerde eerder exits uit te voeren voor broker-posities die niet door Orion waren geopend.

Oplossing:

Brokerposities zonder PositionState of RiskPlan worden nu netjes overgeslagen.

Resultaat:

Geen crashes meer tijdens broker synchronization.

---

## Yahoo symbolen

ASM International gebruikte eerst:

ASMI.AS

Correct Yahoo symbool:

ASM.AS

Universe is aangepast.

---

## Position allocation

ASM kon niet gekocht worden omdat:

max_position_value = 150

lager was dan de aandelenprijs.

Configuratie verhoogd waardoor allocation correct werkt.

---

## Post-fill synchronization

Na een succesvolle BUY ontstond:

IbkrTradingSessionSyncError

Oorzaak:

Yahoo gebruikte:

ASM.AS

IBKR rapporteerde:

ASM

Synchronisatie normaliseert symbolen nu correct.

Resultaat:

Volledige broker synchronization werkt.

---

# Huidige status Autonomous Runner

Werkt volledig.

Autonomous cycle:

- succesvol
- geen exceptions
- broker sync werkt
- portfolio sync werkt
- BUY pipeline werkt
- SELL infrastructuur aanwezig

Wanneer maximum aantal posities bereikt is worden nieuwe BUY's correct geweigerd.

---

# Nieuwe belangrijke ontdekking

Er is een eerste repository-audit uitgevoerd.

Belangrijkste conclusie:

Een groot deel van de functionaliteit bestaat al.

Onder andere gevonden:

- Trailing Stop
- Break Even
- Time Stop
- Exit Engine
- RiskPlan
- Position Monitoring
- CLI-dashboardpresentatie
- Performance analyzers
- Trade Journal
- Portfolio Management

Waarschijnlijk hoeft een aanzienlijk deel alleen nog aangesloten te worden op de Autonomous Runner.

---

# Prioriteit volgende chat

NIET direct nieuwe functionaliteit bouwen.

Eerst een volledige functionele audit uitvoeren.

Doel:

- bestaande services inventariseren
- bepalen welke modules al volledig werken
- vaststellen welke onderdelen nog niet gekoppeld zijn
- voorkomen dat bestaande functionaliteit opnieuw gebouwd wordt

Na de audit wordt bepaald welke functionaliteit daadwerkelijk nog ontwikkeld moet worden.

---

# Ontwikkelprincipes

- Production quality
- Clean Architecture
- Geen tijdelijke oplossingen
- Geen dubbele implementaties
- Eerst bestaande code hergebruiken
- Nieuwe functionaliteit alleen indien echt noodzakelijk
