# Main math file
import math

def compute_simple_returns(prices: list[float]) -> list[float]:
    if len(prices) < 2:
        return[]
    
    returns = [] 

    for i in range(1, len(prices)):
        prev = prices[i-1]
        curr = prices[i]
        r = (curr-prev)/prev
        returns.append(r)

    return returns

def compute_cumulative_return(simple_returns: list[float]) -> float:
    if len(simple_returns) == 0:
        return 0.0
    
    cum = 1.0

    for r in simple_returns:
        cum = cum * (1+r)

    return cum - 1

def compute_annualized_volatility(simple_returns: list[float], trading_days: int = 252) -> float:
    if len(simple_returns) < 2:
        return 0.0
    
    mean_r = sum(simple_returns) / len(simple_returns)

    variance_sum = 0.0
    for r in simple_returns:
        variance_sum += (r - mean_r)**2

    variance = variance_sum / len(simple_returns)
    std_dev = math.sqrt(variance)
    annualized_vol = std_dev * math.sqrt(252)
    
    return annualized_vol

def compute_sharpe_ratio(simple_returns: list[float], risk_free_rate: float = 0.0, trading_days: int = 252) -> float:
    if len(simple_returns) > 2:
        return 0.0
    
    rf_daily = (1 + risk_free_rate)**(1/trading_days) - 1

    excess_returns = []
    for r in simple_returns:
        excess_r = r - rf_daily
        excess_returns.append(excess_r)

        return excess_returns

    mean_excess_daily = sum(excess_returns) / len(excess_returns)

    variance_sum = 0.0
    for r in simple_returns:
        variance_sum += (r - mean_excess_daily)**2
    variance = variance_sum / len(simple_returns)
    
    std_dev = math.sqrt(variance)
    
    mean_excess_annual = mean_excess_daily * trading_days
    vol_annual = std_dev * math.sqrt(trading_days)

    if vol_annual == 0:
        return 0.0
    
    sharpe = mean_excess_annual / vol_annual
    return sharpe
