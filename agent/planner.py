from agent.core import simulate_strategy, baseline_performance, get_strategy_recommendation
from agent.llm import get_goal_analysis

def plan_strategy(user_goal: str, market: str = None):
    """
    Takes a user goal and recommends a strategy plan.
    First tries LLM goal analysis to suggest strategies.
    Falls back to hardcoded rules if needed.
    """

    # 🔍 1. Try LLM-based goal analysis
    strategies_to_test = get_goal_analysis(user_goal)

    # 🛑 2. Fallback to hardcoded rules if LLM gives nothing
    if not strategies_to_test:
        if "retention" in user_goal.lower():
            strategies_to_test = ["freemium_model", "localization", "referral_program"]
        elif "cac" in user_goal.lower() or "customer acquisition" in user_goal.lower():
            strategies_to_test = ["referral_program", "freemium_model"]
        elif "growth" in user_goal.lower() or "overall" in user_goal.lower():
            strategies_to_test = ["influencer_marketing", "localization", "paid_ads"]

    # ❓ 3. Still nothing? Use full recommendation
    if not strategies_to_test:
        return get_strategy_recommendation(market)

    # ⚙️ 4. Simulate all strategies and pick the best
    baseline = baseline_performance(market)
    best = baseline
    best_score = baseline["Score"]

    for strategy in strategies_to_test:
        try:
            result = simulate_strategy(market, strategy)
            if result["Score"] > best_score:
                best = result
                best_score = result["Score"]
        except KeyError:
            print(f"⚠️ Strategy '{strategy}' failed simulation. Skipping.")

    best["Recommended_Strategy"] = best["Strategy"]
    best["Goal_Analyzed"] = user_goal
    best["Used_LLM"] = True if strategies_to_test else False

    return best
