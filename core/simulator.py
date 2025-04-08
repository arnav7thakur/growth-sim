import random
from data.markets import markets
from data.strategy_effects import strategy_effects

def simulate_strategy(market_name, strategy):
    base = markets[market_name]
    strat = strategy_effects.get(strategy, {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.0,
        "conversion_rate_multiplier": 1.0,
        "revenue_per_customer_multiplier": 1.0
    })

    rand = random.uniform(0.9, 1.1)

    # Prepare available metrics
    results = {
        "Market": market_name,
        "Strategy": strategy,
    }
    available = []
    missing = []

    # Handle each metric conditionally
    if "base_CAC" in base:
        CAC = base["base_CAC"] * strat["CAC_multiplier"] * rand
        results["CAC"] = round(CAC, 2)
        available.append("CAC")
    else:
        CAC = None
        missing.append("CAC")

    if "base_LTV" in base:
        LTV = base["base_LTV"] * strat["LTV_multiplier"] * rand
        results["LTV"] = round(LTV, 2)
        available.append("LTV")
    else:
        LTV = None
        missing.append("LTV")

    if "retention" in base:
        retention = base["retention"] * strat["retention_multiplier"] * random.uniform(0.95, 1.05)
        results["Retention"] = round(retention, 2)
        available.append("Retention")
    else:
        retention = None
        missing.append("Retention")

    if "conversion_rate" in base:
        conversion_rate = base["conversion_rate"] * strat["conversion_rate_multiplier"] * random.uniform(0.95, 1.05)
        results["Conversion Rate"] = round(conversion_rate, 3)
        available.append("Conversion Rate")
    else:
        conversion_rate = None
        missing.append("Conversion Rate")

    if "revenue_per_customer" in base:
        revenue_per_customer = base["revenue_per_customer"] * strat["revenue_per_customer_multiplier"] * rand
        results["Revenue per Customer"] = round(revenue_per_customer, 2)
        available.append("Revenue per Customer")
    else:
        revenue_per_customer = None
        missing.append("Revenue per Customer")

    # Compute score based only on available metrics
    score = 0
    weights = {
        "LTV/CAC": 0.35,
        "Retention": 0.25,
        "Conversion Rate": 0.2,
        "Revenue per Customer": 0.2,
    }

    if LTV and CAC:
        score += (LTV / CAC) * weights["LTV/CAC"]
    if retention:
        score += retention * weights["Retention"]
    if conversion_rate:
        score += conversion_rate * weights["Conversion Rate"]
    if revenue_per_customer:
        score += (revenue_per_customer / 100) * weights["Revenue per Customer"]

    results["Score"] = round(score, 2)

    if missing:
        results["Note"] = (
            f"⚠️ Missing metrics: {', '.join(missing)}. "
            f"Score computed using: {', '.join(available)}."
        )

    return results
