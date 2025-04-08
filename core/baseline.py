from data.markets import markets

def baseline_market_performance(market_name):
    base = markets[market_name]

    CAC = base["base_CAC"]
    LTV = base["base_LTV"]
    retention = base["retention"]
    conversion_rate = base.get("base_conversion_rate", 0.05)  # fallback to 5%
    revenue_per_customer = base.get("base_revenue_per_customer", 100)  # fallback to $100

    score = (LTV / CAC) * retention * conversion_rate * (revenue_per_customer / 100)

    return {
        "Market": market_name,
        "Strategy": "baseline",
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Conversion_Rate": round(conversion_rate, 2),
        "Revenue_per_Customer": round(revenue_per_customer, 2),
        "Score": round(score, 2),
    }