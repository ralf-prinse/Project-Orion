# PROJECT ORION — STRATEGY COMPONENT CONSOLIDATION AUDIT

**Status:** In progress
**Branch:** `strategy-s2.2-component-consolidation`
**Regression baseline:** `75 passed`

## 1. Doel

Deze audit bepaalt welke strategische componenten canoniek actief zijn en welke componenten een legacy-, compatibility-, GUI-, test- of experimentele rol hebben.

Tijdens deze audit wordt nog niets verwijderd.

Het einddoel is één samenhangende autonome strategieflow zonder parallelle owners of dubbele beslislogica.

---

## 2. Canonieke autonome strategieflow

```text
Market Data
        ↓
IndicatorPack
        ↓
SignalFusionEngine
        ↓
MarketIntelligenceEngine
        ↓
AdaptiveDecisionEngine
        ↓
InvestmentThesisBuilder
        ↓
AdaptiveRiskEngine
        ↓
OpportunityRankingEngine
        ↓
LivePaperCandidate
        ↓
PortfolioAllocator
        ↓
Paper Execution
        ↓
TradingSession
```

`TradingSession` blijft de enige runtime-owner van portfolio-, position- en risk-state.

---

## 3. Decision Engine-audit

### 3.1 AdaptiveDecisionEngine

**Bestand**

```text
services/decision/adaptive_decision_engine.py
```

**Actieve caller**

```text
services/orchestration/trading_pipeline.py
```

**Input**

```text
MarketSignal
```

**Output**

```text
TradeDecision
```

**Verantwoordelijkheid**

* dynamische BUY-drempel;
* dynamische SELL-drempel;
* HOLD-beslissing;
* confidence;
* deterministische uitleg.

**Classificatie**

```text
CANONIEK ACTIEF
```

Deze engine blijft voorlopig de officiële entry-decision engine van de autonome paper-tradingruntime.

---

### 3.2 Legacy DecisionEngine

**Bestand**

```text
engines/decision_engine.py
```

**Actieve caller**

```text
services/scanner_service.py
```

**Input**

```text
TechnicalAnalysis
```

**Output**

```text
TradeDecision / BUY / HOLD / SELL / NONE
```

**Verantwoordelijkheid**

* nieuwe positie beoordelen;
* bestaande positie beoordelen;
* korte holdingduur adviseren;
* RSI-, trend-, momentum- en volumegebaseerde beslissingen.

**Classificatie**

```text
LEGACY SCANNER ROUTE
```

Deze engine maakt geen onderdeel uit van de officiële autonomous paper-tradingruntime.

Voor verwijdering moet eerst worden vastgesteld of `ScannerService` nog door GUI-, CLI- of legacyflows wordt gebruikt.

---

### 3.3 Core DecisionEngine

**Bestand**

```text
services/decision/decision_engine.py
```

**Input**

```text
DecisionInput
```

**Output**

```text
TradeDecision
```

**Verantwoordelijkheid**

* scoregebaseerde BUY/SELL/HOLD;
* position sizing aanroepen;
* expected risk berekenen.

**Bekende callers**

* gerichte tests;
* geen bevestigde caller vanuit de actieve autonomous runtime.

**Classificatie**

```text
TEST / EXPERIMENTELE ROUTE
```

De verantwoordelijkheid overlapt gedeeltelijk met:

* `AdaptiveDecisionEngine`;
* `PositionSizer`;
* `PortfolioAllocator`;
* `AdaptiveRiskEngine`.

Nog niet verwijderen totdat alle imports en tests formeel zijn geclassificeerd.

---

### 3.4 Analyzer-based DecisionEngine

**Bestand**

```text
services/decisions/engine/decision_engine.py
```

**Input**

```text
SignalResult
DecisionContext
```

**Output**

```text
DecisionResult
```

**Verantwoordelijkheid**

* analyzer-orchestratie;
* decision registry;
* generieke decision state;
* deterministische analyzer-volgorde.

**Bekende callers**

* gespecialiseerde tests;
* compatibility import;
* geen bevestigde caller vanuit de actieve autonomous runtime.

**Classificatie**

```text
AFZONDERLIJK DECISION FRAMEWORK
```

Dit framework mag niet parallel in de autonome runtime worden geïntegreerd zonder een expliciete migratiebeslissing.

---

### 3.5 Compatibility wrapper

**Bestand**

```text
services/decisions/decision_engine.py
```

**Functie**

Re-export van:

```text
services.decisions.engine.decision_engine.DecisionEngine
```

**Classificatie**

```text
COMPATIBILITY WRAPPER
```

Kan alleen worden verwijderd wanneer geen externe imports meer bestaan.

---

## 4. Besluit Decision Ownership

Voor de actuele autonomous paper-tradingruntime geldt:

```text
AdaptiveDecisionEngine
```

is de enige canonieke actieve entry-decision engine.

De overige decision engines mogen niet worden gekoppeld aan de autonome runtime zonder:

1. volledige caller-audit;
2. expliciete migratie;
3. gerichte tests;
4. volledige regressie;
5. documentatie-update.

---

## 5. Signal ownership

Voor de actuele autonomous runtime geldt:

```text
SignalFusionEngine
```

is de canonieke eigenaar van fused trading signals.

De experimentele `SignalInterpreter` wordt niet geïntegreerd, omdat zijn verantwoordelijkheid overlapt met:

* `SignalFusionEngine`;
* `MarketIntelligenceEngine`;
* `InvestmentThesisBuilder`.

---

## 6. Explanation ownership

Voor strategische uitleg geldt:

```text
InvestmentThesis
├── supporting_reasons
├── risk_reasons
├── invalidation_conditions
└── factors
```

De experimentele `ConvictionExplainer` wordt niet geïntegreerd zolang dezelfde uitleg uit de thesis kan worden afgeleid.

---

## 7. Opportunity ownership

Voor de autonome runtime gelden voorlopig:

```text
InvestmentThesis
```

voor inhoudelijke kwaliteit en uitleg;

```text
OpportunityRanking
```

voor rangschikking en factorbijdragen;

```text
LivePaperCandidate
```

als runtimecontainer voor een gescande kandidaat.

Er wordt geen nieuw algemeen `Opportunity`-model toegevoegd.

`OpportunityService` blijft voorlopig een GUI-/presentatie-adapter en wordt niet de owner van strategische beslissingen.

---

## 8. Volgende audits

De consolidatie wordt in deze volgorde voortgezet:

1. ranking-engine-audit;
2. opportunity-model-audit;
3. journal- en trade-evaluation-audit;
4. scanner-route-audit;
5. legacy import-audit;
6. position-intelligence-ontwerp.

---

## 9. Regels

* Geen nieuwe decision engine toevoegen.
* Geen nieuwe signal owner toevoegen.
* Geen parallel opportunitymodel toevoegen.
* Geen component verwijderen zonder caller-audit.
* De actieve autonome runtime blijft regressievrij.
* `TradingSession` blijft de enige lifecycle-state-owner.

# End
