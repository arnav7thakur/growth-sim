# core/baseline.py

from data.markets import markets

def baseline_market_performance(market_name):
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
