import random
from data.markets import markets
from data.strategy_effects import strategy_effects


def baseline_performance(market_name):
    base = markets[market_name]

    # Handle missing values with fallback/defaults
    CAC = base.get("base_CAC", 1.0)
    LTV = base.get("base_LTV", 1.0)
    retention = base.get("retention", 1.0)
    conversion_rate = base.get("conversion_rate", 1.0)
    revenue_per_customer = base.get("revenue_per_customer", 1.0)

    score = (LTV / CAC) * retention * conversion_rate * (revenue_per_customer / 100)

    return {
        "Market": market_name,
        "Strategy": "baseline",
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Conversion Rate": round(conversion_rate, 4),
        "Revenue per Customer": round(revenue_per_customer, 2),
        "Score": round(score, 2),
    }


def simulate_strategy(market_name, strategy):
    base = markets[market_name]

    # Default multipliers if strategy not found
    strat = strategy_effects.get(strategy, {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.0,
        "conversion_rate_multiplier": 1.0,
        "revenue_per_customer_multiplier": 1.0
    })

    # Use base values with fallbacks
    base_CAC = base.get("base_CAC", 1.0)
    base_LTV = base.get("base_LTV", 1.0)
    retention = base.get("retention", 1.0)
    conversion_rate = base.get("conversion_rate", 1.0)
    revenue_per_customer = base.get("revenue_per_customer", 1.0)

    rand = random.uniform(0.9, 1.1)

    CAC = base_CAC * strat["CAC_multiplier"] * rand
    LTV = base_LTV * strat["LTV_multiplier"] * rand
    retention *= strat["retention_multiplier"] * random.uniform(0.95, 1.05)
    conversion_rate *= strat["conversion_rate_multiplier"] * random.uniform(0.95, 1.05)
    revenue_per_customer *= strat["revenue_per_customer_multiplier"] * random.uniform(0.95, 1.05)

    score = (LTV / CAC) * retention * conversion_rate * (revenue_per_customer / 100)

    return {
        "Market": market_name,
        "Strategy": strategy,
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Conversion Rate": round(conversion_rate, 4),
        "Revenue per Customer": round(revenue_per_customer, 2),
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
    strategies = strategies or list(strategy_effects.keys())
    baseline = baseline_performance(market_name)
    baseline_score = baseline["Score"]

    scored = []
    for s in strategies:
        sim = simulate_strategy(market_name, s)
        sim["Delta_Score"] = sim["Score"] - baseline_score
        scored.append(sim)

    scored.sort(key=lambda x: x["Delta_Score"], reverse=True)
    best = scored[0] if scored else None

    return {
        "recommended": best["Strategy"] if best else None,
        "delta_score": round(best["Delta_Score"], 2) if best else None,
        "details": scored,
        "baseline_score": baseline_score
    }
