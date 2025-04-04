import random
from data.markets import markets
from data.strategy_effects import strategy_effects

def simulate_strategy(market_name, strategy):
    base = markets[market_name]
    strat = strategy_effects.get(strategy, {
        "CAC_multiplier": 1.0,
        "LTV_multiplier": 1.0,
        "retention_multiplier": 1.0
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
