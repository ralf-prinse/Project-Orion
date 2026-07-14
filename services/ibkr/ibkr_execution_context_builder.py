from __future__ import annotations

import math
from collections.abc import Mapping

from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from services.ibkr.ibkr_portfolio_service import IbkrPortfolioService


class IbkrExecutionContextBuilderError(ValueError):
    """
    Raised when an IBKR-backed ExecutionContext cannot be built safely.
    """


class IbkrExecutionContextBuilder:
    """
    Builds the existing Orion ExecutionContext from:

    - an existing ExecutionRequest;
    - current IBKR account and position state;
    - externally validated current prices.

    This builder does not:

    - place orders;
    - generate trading decisions;
    - create risk plans;
    - own TradingSession state;
    - fetch market data.
    """

    SUPPORTED_TRADING_MODE = "PAPER"

    def __init__(
        self,
        *,
        portfolio_service: IbkrPortfolioService,
        max_position_percentage: float = 1.0,
        allow_fractional_shares: bool = False,
    ) -> None:
        self._portfolio_service = portfolio_service
        self._max_position_percentage = (
            self._validate_max_position_percentage(
                max_position_percentage
            )
        )
        self._allow_fractional_shares = bool(
            allow_fractional_shares
        )

    def build(
        self,
        *,
        request: ExecutionRequest,
        current_prices: Mapping[str, float],
    ) -> ExecutionContext:
        self._validate_request(request)

        portfolio = self._portfolio_service.read_portfolio(
            current_prices=current_prices,
        )

        return ExecutionContext(
            request=request,
            portfolio=portfolio,
            trading_mode=self.SUPPORTED_TRADING_MODE,
            max_position_percentage=(
                self._max_position_percentage
            ),
            allow_fractional_shares=(
                self._allow_fractional_shares
            ),
        )

    def _validate_request(
        self,
        request: ExecutionRequest,
    ) -> None:
        symbol = request.symbol.strip().upper()
        action = request.action.strip().upper()

        if not symbol:
            raise IbkrExecutionContextBuilderError(
                "ExecutionRequest symbol must not be empty."
            )

        if action != "OPEN_POSITION":
            raise IbkrExecutionContextBuilderError(
                "IbkrExecutionContextBuilder currently supports "
                "only OPEN_POSITION requests."
            )

        if not isinstance(request.quantity, int):
            raise IbkrExecutionContextBuilderError(
                "ExecutionRequest quantity must be an integer."
            )

        if request.quantity <= 0:
            raise IbkrExecutionContextBuilderError(
                "ExecutionRequest quantity must be greater than zero."
            )

        self._require_finite_positive(
            request.entry_price,
            field_name="ExecutionRequest entry price",
        )

        self._require_finite_probability(
            request.confidence,
            field_name="ExecutionRequest confidence",
        )

        if request.risk_plan is None:
            raise IbkrExecutionContextBuilderError(
                "ExecutionRequest risk_plan must not be None."
            )

        risk_symbol = (
            request.risk_plan.symbol.strip().upper()
        )

        if risk_symbol != symbol:
            raise IbkrExecutionContextBuilderError(
                "ExecutionRequest symbol and RiskPlan symbol "
                "must match."
            )

    def _validate_max_position_percentage(
        self,
        value: float,
    ) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrExecutionContextBuilderError(
                "max_position_percentage must be numeric."
            ) from exc

        if not math.isfinite(normalized):
            raise IbkrExecutionContextBuilderError(
                "max_position_percentage must be finite."
            )

        if normalized <= 0 or normalized > 1:
            raise IbkrExecutionContextBuilderError(
                "max_position_percentage must be greater than "
                "zero and at most 1."
            )

        return normalized

    def _require_finite_positive(
        self,
        value: float,
        *,
        field_name: str,
    ) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be numeric."
            ) from exc

        if not math.isfinite(normalized):
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be finite."
            )

        if normalized <= 0:
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be greater than zero."
            )

        return normalized

    def _require_finite_probability(
        self,
        value: float,
        *,
        field_name: str,
    ) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be numeric."
            ) from exc

        if not math.isfinite(normalized):
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be finite."
            )

        if normalized < 0 or normalized > 1:
            raise IbkrExecutionContextBuilderError(
                f"{field_name} must be between 0 and 1."
            )

        return normalized