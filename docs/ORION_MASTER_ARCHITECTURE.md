# ORION MASTER ARCHITECTURE

Laatste update: 19-07-2026

---

# Missie

Project Orion is een modulair AI-gedreven algoritmisch tradingplatform dat volledig autonoom kan handelen.

Het systeem is ontworpen volgens Clean Architecture en Domain-Driven Design, waarbij iedere module één duidelijke verantwoordelijkheid heeft.

Doelstellingen:

- betrouwbare besluitvorming
- volledig autonoom handelen
- reproduceerbare resultaten
- maximale herbruikbaarheid
- production-ready architectuur

Nieuwe functionaliteit wordt alleen toegevoegd wanneer bestaande componenten niet aan de eisen voldoen.

---

# Architectuur

Project Orion bestaat uit de volgende hoofdlagen:

```
Market Data
      │
      ▼
News Intelligence (SHADOW / audit only)
      │
      ▼
Indicators
      │
      ▼
Signal Generation
      │
      ▼
Decision Engine
      │
      ▼
Risk Management
      │
      ▼
Portfolio Management
      │
      ▼
Execution Engine
      │
      ▼
Broker (Paper / IBKR)
      │
      ▼
Synchronization
      │
      ▼
Monitoring & Reporting
```

Iedere laag communiceert uitsluitend via duidelijke interfaces en domeinmodellen.

---

# Belangrijkste subsystemen

## Data

- Universe
- Market Data Providers
- Indicator Builder

De actuele IBKR Paper-datalaag gebruikt een gecureerd universum van 100
EU/VS-symbolen. `LivePaperMarketScanner` filtert eerst op officiële beursuren en
vraagt daarna historische data aan via de canonieke batchprovider. De provider
werkt in batches van 25 met een cache-TTL van 15 minuten; broker- en
positieprijzen blijven via de afzonderlijke gevalideerde actuele-prijsservice
lopen.

---

## Trading

- Trading Pipeline
- Signal Fusion
- Decision Engine
- Position Allocator

---

## Risk

- RiskPlan
- Stop Loss
- Trailing Stop
- Break Even
- Time Stop
- Exit Evaluation

---

## Execution

- Execution Engine
- Paper Trading
- IBKR Broker
- Order Transport
- Broker Synchronization

---

## Portfolio

- Position Management
- Cash Management
- Equity Management
- Portfolio Synchronization

---

## Monitoring

- Position Monitoring
- Trade Journal
- CLI-presentatie en TWS
- Performance Analytics
- Logging
- Reporting

De Orion-desktop-GUI is verwijderd. Nieuws gebruikt een providerinterface; de
eerste adapter leest IBKR-headlines met een afzonderlijk client-ID.
Normalisatie, deduplicatie, beoordeling en opslag zijn broker-onafhankelijk.
`SHADOW` is een harde grens: nieuws wordt alleen aan kandidaat- en journaldata
toegevoegd en verandert geen handelsbesluit.

Na een volledig gesloten positie koppelt `trade_id` de entry- of
adoptiejournalregel aan de exit. Het `CompletedTradeRecord` is de canonieke
toekomstige input voor offline performance- en learninganalyse. Learning heeft
geen schrijfpad naar live configuratie of orders.

---

# Ontwikkelprincipes

Project Orion volgt de volgende uitgangspunten:

- Clean Architecture
- Domain Driven Design
- SOLID-principes
- Hoge testdekking
- Geen dubbele implementaties
- Productiecode boven prototypes
- Kleine, herbruikbare services

---

# Huidige status

De autonome IBKR Paper Trading infrastructuur is operationeel.

Werkende onderdelen:

- marktdata
- indicatoren
- trading pipeline
- AI-besluitvorming
- position allocation
- execution
- broker communicatie
- synchronisatie
- autonome runner

De basisarchitectuur wordt als stabiel beschouwd.

---

# Ontwikkelfase

Project Orion bevindt zich niet langer in de fase van infrastructuurontwikkeling.

De huidige focus is:

1. bestaande functionaliteit volledig inventariseren;
2. bestaande modules koppelen aan de Autonomous Runner;
3. ontbrekende functionaliteit identificeren;
4. uitsluitend ontbrekende onderdelen ontwikkelen.

---

# Eerstvolgende doel

Een volledige functionele audit van de complete codebase uitvoeren.

Per module wordt vastgesteld:

- bestaat de functionaliteit;
- is deze volledig geïmplementeerd;
- is deze getest;
- wordt deze gebruikt;
- kan deze direct worden geactiveerd;
- of moet deze verder worden ontwikkeld.

Pas na deze audit worden nieuwe ontwikkelwerkzaamheden gestart.
