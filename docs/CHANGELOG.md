# CHANGELOG.md

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