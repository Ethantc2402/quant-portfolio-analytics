from fastapi import APIRouter
from app.quant.metrics import (
    compute_simple_returns,
    compute_cumulative_return,
    compute_annualized_volatility,
    compute_sharpe_ratio,
)

router = APIRouter()

@router.get("/analytics/demo")
def analytics_demo():
    # 1. dummy price series
    prices = [100, 102, 101, 105, 110]

    # 2. compute metrics
    simple_returns = compute_simple_returns(prices)
    cumulative_return = compute_cumulative_return(simple_returns)
    annualized_volatility = compute_annualized_volatility(simple_returns)
    sharpe_ratio = compute_sharpe_ratio(simple_returns)

    # 3. return as JSON
    return {
        "prices": prices,
        "simple_returns": simple_returns,
        "cumulative_return": cumulative_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
    }
