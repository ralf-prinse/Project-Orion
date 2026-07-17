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
- Dashboard
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