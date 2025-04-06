from agent.core import simulate_strategy, baseline_performance, get_strategy_recommendation
from agent.llm import get_goal_analysis

def plan_strategy(user_goal: str, market: str = None):
    """
    Takes a user goal and recommends a strategy plan.
    Uses LLM goal analysis to suggest strategies.
    No longer falls back to hardcoded keyword-based rules.
    """

    market = market or "India"  # 🌍 Default market if none provided

    # 1. Try LLM-based goal analysis
    strategies_to_test = get_goal_analysis(user_goal)

    # 2. If LLM gives nothing, log it and exit gracefully
    if not strategies_to_test:
        print(f"⚠️ LLM couldn't generate relevant strategies for goal: '{user_goal}'")
        return {
            "Note": "The AI was unable to generate relevant strategies for your goal.",
            "Goal_Analyzed": user_goal,
            "Used_LLM": True,
            "Recommended_Strategy": None
        }

    # ⛔️ Hardcoded fallback logic (deprecated, now unused)
    """
    if not strategies_to_test:
        if "retention" in user_goal.lower():
            strategies_to_test = ["freemium_model", "localization", "referral_program"]
        elif "cac" in user_goal.lower() or "customer acquisition" in user_goal.lower():
            strategies_to_test = ["referral_program", "freemium_model"]
        elif "growth" in user_goal.lower() or "overall" in user_goal.lower():
            strategies_to_test = ["influencer_marketing", "localization", "paid_ads"]
    """

    print(f"🧠 Strategies considered for goal '{user_goal}': {strategies_to_test}")

    # 3. Simulate all strategies and pick the best
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

    # 4. If none outperformed baseline, optionally ask LLM again
    if best == baseline:
        best["Note"] = "No strategy outperformed the baseline for this goal."
        llm_fallback = get_strategy_recommendation(market)
        best["LLM_Suggested_Strategy"] = llm_fallback.get("Strategy")

    best["Recommended_Strategy"] = best["Strategy"]
    best["Goal_Analyzed"] = user_goal
    best["Used_LLM"] = True

    return best
