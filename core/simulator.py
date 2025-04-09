import random
from data.strategy_effects import strategy_effects

def simulate_strategy(market_name, strategy, company_data=None):
    # Strategy multipliers
    strat = strategy_effects.get(strategy, {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.0,
        "conversion_rate_multiplier": 1.0,
        "revenue_per_customer_multiplier": 1.0
    })

    rand = random.uniform(0.95, 1.05)

    results = {
        "Market": market_name,
        "Strategy": strategy,
    }

    available = []
    missing = []

    # Use uploaded data if provided, else fallback to base market assumptions
    if company_data is not None:
        CAC = company_data["customer_acquisition_cost"].mean()
        LTV = company_data["ltv"].mean()
        retention = company_data["retention_rate"].mean()
        conversion_rate = company_data["conversion_rate"].mean()
        revenue_per_customer = company_data["revenue_per_customer"].mean()
    else:
        from data.markets import markets
        base = markets[market_name]
        CAC = base.get("base_CAC")
        LTV = base.get("base_LTV")
        retention = base.get("retention")
        conversion_rate = base.get("conversion_rate")
        revenue_per_customer = base.get("revenue_per_customer")

    # Apply strategy effects
    if CAC is not None:
        CAC *= strat["CAC_multiplier"] * rand
        results["CAC"] = round(CAC, 2)
        available.append("CAC")
    else:
        missing.append("CAC")

    if LTV is not None:
        LTV *= strat["LTV_multiplier"] * rand
        results["LTV"] = round(LTV, 2)
        available.append("LTV")
    else:
        missing.append("LTV")

    if retention is not None:
        retention *= strat["retention_multiplier"] * random.uniform(0.95, 1.05)
        results["Retention"] = round(retention, 2)
        available.append("Retention")
    else:
        missing.append("Retention")

    if conversion_rate is not None:
        conversion_rate *= strat["conversion_rate_multiplier"] * random.uniform(0.95, 1.05)
        results["Conversion Rate"] = round(conversion_rate, 3)
        available.append("Conversion Rate")
    else:
        missing.append("Conversion Rate")

    if revenue_per_customer is not None:
        revenue_per_customer *= strat["revenue_per_customer_multiplier"] * rand
        results["Revenue per Customer"] = round(revenue_per_customer, 2)
        available.append("Revenue per Customer")
    else:
        missing.append("Revenue per Customer")

    # Score calculation
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
