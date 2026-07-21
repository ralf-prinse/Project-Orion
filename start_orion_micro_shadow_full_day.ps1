param(
    [Parameter(Mandatory = $false)]
    [string]$PaperAccountId = $env:ORION_IBKR_PAPER_ACCOUNT_ID
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($PaperAccountId)) {
    throw (
        "Provide -PaperAccountId with the IBKR Paper account beginning " +
        "with DU, or set ORION_IBKR_PAPER_ACCOUNT_ID."
    )
}

$normalizedAccountId = $PaperAccountId.Trim().ToUpperInvariant()
if (-not $normalizedAccountId.StartsWith("DU")) {
    throw "PaperAccountId must be an IBKR Paper account beginning with DU."
}

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$runner = Join-Path $PSScriptRoot "run_autonomous_ibkr_paper.py"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Project virtual-environment Python was not found: $python"
}
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) {
    throw "Autonomous runner was not found: $runner"
}

# Remove the obsolete, similarly named variable so it cannot mislead the user.
Remove-Item Env:ORION_IBKR_CAPITAL_PROFILE -ErrorAction SilentlyContinue

$env:ORION_IBKR_PAPER_ACCOUNT_ID = $normalizedAccountId
$env:ORION_IBKR_EXECUTION_MODE = "SHADOW"
$env:ORION_IBKR_ALLOW_ORDERS = "false"
$env:ORION_CAPITAL_PROFILE = "MICRO_500"
$env:ORION_IBKR_NEWS_MODE = "DISABLED"
$env:ORION_IBKR_CYCLES = "160"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS = "300"
$env:ORION_IBKR_EXIT_STRATEGY = "COST_AWARE_SMALL_PROFIT"
$env:ORION_IBKR_PRICING_PLAN = "TIERED"
$env:ORION_MONTHLY_MARKET_DATA_COST_EUR = "3"

Write-Host "Starting the bounded MICRO_500 full-day shadow configuration."
Write-Host "Expected confirmation: START 160 ORION MICRO 500 SHADOW CYCLES"

Push-Location $PSScriptRoot
try {
    & $python $runner
}
finally {
    Pop-Location
}
