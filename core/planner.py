from agent.core import simulate_strategy, baseline_performance, get_strategy_recommendation
from agent.llm import get_goal_analysis

def log_company_data(company_data):
    if company_data is not None:
        print("📊 Received company_data:")
        print(company_data.head())

def get_strategies_for_goal(goal):
    strategies = get_goal_analysis(goal)
    if not strategies:
        print(f"⚠️ LLM couldn't generate relevant strategies for goal: '{goal}'")
        return None
    print(f"🧠 Strategies considered for goal '{goal}': {strategies}")
    return strategies

def find_best_strategy(market, strategies_to_test, baseline, company_data=None):
    best = baseline
    best_score = baseline["Score"]

    for strategy in strategies_to_test:
        try:
            result = simulate_strategy(market, strategy, company_data=company_data)
            if result["Score"] > best_score:
                best = result
                best_score = result["Score"]
        except KeyError:
            print(f"⚠️ Strategy '{strategy}' failed simulation. Skipping.")

    return best

def plan_strategy(user_goal: str, market: str = None, company_data=None):
    """
    Analyze the user's goal and suggest a growth strategy.
    """
    market = market or "India"  # 🌍 Default market fallback

    # Step 1: Optional debug for uploaded company data
    log_company_data(company_data)

    # Step 2: Use LLM to interpret user goal into strategies
    strategies_to_test = get_strategies_for_goal(user_goal)
    if not strategies_to_test:
        return {
            "Note": "The AI was unable to generate relevant strategies for your goal.",
            "Goal_Analyzed": user_goal,
            "Used_LLM": True,
            "Recommended_Strategy": None
        }

    # Step 3: Simulate strategies and compare with baseline
    baseline = baseline_performance(market, company_data=company_data)
    best = find_best_strategy(market, strategies_to_test, baseline, company_data=company_data)

    # Step 4: If no improvement over baseline, ask LLM for fallback
    if best == baseline:
        best["Note"] = "No strategy outperformed the baseline for this goal."
        llm_fallback = get_strategy_recommendation(market)
        best["LLM_Suggested_Strategy"] = llm_fallback.get("Strategy")

    # Final metadata
    best["Recommended_Strategy"] = best["Strategy"]
    best["Goal_Analyzed"] = user_goal
    best["Used_LLM"] = True

    return best
