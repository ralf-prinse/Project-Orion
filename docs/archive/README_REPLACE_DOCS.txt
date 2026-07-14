PROJECT ORION DOCUMENTATION UPDATE

Replace the complete contents of your repository's docs folder with the files in this ZIP.

Included:
- AI_CONTEXT.md
- PROJECT_STATUS.md
- TODO.md
- CHANGELOG.md
- ORION_MASTER_ARCHITECTURE.md
- PROJECT_VISION.md
- TRADING_STRATEGY.md
- POSITION_STATE_STORE_USAGE_AUDIT.md

These files are synchronized for:
- branch sprint-8.13-position-state-store-removal
- PositionStateStore removed
- TradingSession sole lifecycle owner
- 69 tests passing
- next step: Engine 1.0 review

After replacing:
python run_tests.py
git status
git add docs
git commit -m "Docs: synchronize Orion Engine 1.0 handoff"
git push
