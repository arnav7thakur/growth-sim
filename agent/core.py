import random
from data.markets import markets
from data.strategy_effects import strategy_effects


def baseline_performance(market_name):
    base = markets[market_name]
    CAC = base["base_CAC"]
    LTV = base["base_LTV"]
    retention = base["retention"]
    score = (LTV / CAC) * retention

    return {
        "Market": market_name,
        "Strategy": "baseline",
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Score": round(score, 2),
    }


def simulate_strategy(market_name, strategy):
    base = markets[market_name]

    if strategy == "baseline":
        return baseline_performance(market_name)

    strat = strategy_effects.get(strategy, {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.0,
    })

    rand = random.uniform(0.9, 1.1)

    CAC = base["base_CAC"] * strat["CAC_multiplier"] * rand
    LTV = base["base_LTV"] * strat["LTV_multiplier"] * rand
    retention = base["retention"] * strat["retention_multiplier"] * random.uniform(0.95, 1.05)
    score = (LTV / CAC) * retention

    return {
        "Market": market_name,
        "Strategy": strategy,
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Score": round(score, 2),
    }


def run_full_simulation():
    strategies = list(strategy_effects.keys())
    results = []

    for market in markets:
        results.append(baseline_performance(market))
        for strategy in strategies:
            results.append(simulate_strategy(market, strategy))
    return results

def get_strategy_recommendation(market_name, strategies=None):
    """
    Recommends the best growth strategy for a given market.
    If a list of strategies is provided, it evaluates only those.
    Otherwise, it evaluates all available strategies.
    """
    # Default to all strategies if none are specified
    strategies = strategies or list(strategy_effects.keys())

    baseline = baseline_performance(market_name)
    baseline_score = baseline["Score"]

    scored = []
    for s in strategies:
        sim = simulate_strategy(market_name, s)
        sim["Delta_Score"] = sim["Score"] - baseline_score
        scored.append(sim)

    # Sort strategies by performance improvement
    scored.sort(key=lambda x: x["Delta_Score"], reverse=True)
    
    best = scored[0] if scored else None

    return {
        "recommended": best["Strategy"] if best else None,
        "delta_score": round(best["Delta_Score"], 2) if best else None,
        "details": scored,
        "baseline_score": baseline_score
    }
