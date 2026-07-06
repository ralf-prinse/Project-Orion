# PROJECT VISION

---

# Documentation Information

Documentation Version

v1.12

Architecture Version

v2.1

Last Updated

2026-07-05

---

# Vision

The long-term vision of Orion is to become a complete professional desktop trading workstation centered around Mission Control.

Mission Control should allow a trader to understand the current market within seconds after launching the application.

Instead of manually analysing hundreds of symbols, Orion continuously performs deterministic analysis and highlights only the opportunities that deserve attention.

Orion no longer focuses solely on finding trading opportunities.

The platform now supports the complete deterministic trading workflow:

Market Awareness

↓

Opportunity Discovery

↓

Trading Decision

↓

Position Sizing

↓

Open Trade

↓

Trade Lifecycle

↓

Trade Monitor

↓

Exit Intelligence

↓

Trade History

↓

Portfolio Intelligence

↓

Paper Trading

↓

Optional Broker Integration

Every stage of this workflow must remain deterministic, explainable and independently testable.

---

# Current Direction

Trade Lifecycle is now the primary development focus.

Mission Control remains the operational center of Orion.

Trading Workspace remains the deterministic entry point for individual BUY / HOLD / SELL analysis.

Trade Monitor is evolving into the central workspace for active open trades.

Portfolio remains responsible for trading capital configuration.

Broker connectivity remains optional.

Orion does not execute real broker orders.

Orion is a deterministic decision-support platform, not an automated trading bot.

---

# Broker Context

Current broker context:

DEGIRO

Current account currency:

EUR

Default market currency:

USD

Current supported market direction:

- NASDAQ
- NYSE
- Euronext Amsterdam
- Xetra

Live FX conversion supports EUR/USD-aware position sizing.

Broker execution remains outside Orion.

Future broker integration may support import, export or assisted workflows, but must never replace deterministic decision making.

---

# Core Principle

Every new feature must strengthen the deterministic architecture before expanding automation.

Artificial Intelligence may explain deterministic output.

Artificial Intelligence may never create BUY, SELL or EXIT decisions.

---

# End of PROJECT_VISION