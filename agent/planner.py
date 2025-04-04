# agent/planner.py

from agent.core import run_full_simulation, get_strategy_recommendation
from data.markets import markets

def plan_strategy(user_goal: str, market: str = None):
    """
    Takes a user goal and recommends a strategy plan.
    Currently handles:
    - retention optimization
    - CAC minimization
    - overall score max
    """

    strategies_to_test = []

    if "retention" in user_goal.lower():
        strategies_to_test = ["freemium_model", "localization", "referral_program"]
    elif "cac" in user_goal.lower() or "customer acquisition" in user_goal.lower():
        strategies_to_test = ["referral_program", "freemium_model"]
    elif "growth" in user_goal.lower() or "overall" in user_goal.lower():
        strategies_to_test = ["influencer_marketing", "localization", "paid_ads"]

    # Fall back to recommending based on full simulation
    if not strategies_to_test:
        return get_strategy_recommendation(market)

    best = None
    best_score = float("-inf")

    for strategy in strategies_to_test:
        result = get_strategy_recommendation(market, [strategy])
        if result["Score"] > best_score:
            best = result
            best_score = result["Score"]

    return best
