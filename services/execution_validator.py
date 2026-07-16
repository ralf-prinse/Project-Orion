from __future__ import annotations

from dataclasses import dataclass

from models.execution_context import ExecutionContext


@dataclass(frozen=True)
class ExecutionValidationResult:
    """
   Deterministic validation result for execution requests.
    """

    is_valid: bool
    errors: list[str]

    @property
    def status(self) -> str:
        return "PASS" if self.is_valid else "FAIL"


class ExecutionValidator:
    """
    Validates whether an execution request may proceed.

    BUY and SELL share the same validator but use different
    deterministic validation rules.

    No broker logic.
    No portfolio mutation.
    No AI.
    """

    BUY_ACTIONS = {
        "BUY",
        "OPEN_POSITION",
    }

    SELL_ACTIONS = {
        "SELL",
        "CLOSE_POSITION",
    }

    def validate(
        self,
        context: ExecutionContext,
    ) -> ExecutionValidationResult:

        errors: list[str] = []

        request = context.request
        action = request.action.upper().strip()

        #
        # Common validation
        #

        if not request.symbol:
            errors.append("Symbol is missing.")

        if request.entry_price <= 0:
            errors.append("Entry price must be greater than zero.")

        if request.quantity <= 0:
            errors.append("Quantity must be greater than zero.")

        if request.confidence <= 0:
            errors.append("Confidence must be greater than zero.")

        #
        # BUY validation
        #

        if action in self.BUY_ACTIONS:

            if context.requested_value > context.available_cash:
                errors.append("Insufficient available cash.")

            if (
                context.position_size_percent
                > context.max_position_percentage
            ):
                errors.append(
                    "Requested position exceeds maximum portfolio allocation."
                )

        #
        # SELL validation
        #

        elif action in self.SELL_ACTIONS:

            position = context.portfolio.positions.get(context.symbol)

            if position is None:
                errors.append(
                    f"No open position exists for {context.symbol}."
                )
            elif request.quantity > position.quantity:
                errors.append(
                    "Cannot sell more shares than currently owned."
                )

        #
        # Unknown action
        #

        else:
            errors.append(
                f"Unsupported execution action '{request.action}'."
            )

        return ExecutionValidationResult(
            is_valid=not errors,
            errors=errors,
        )