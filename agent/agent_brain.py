# agent_brain.py

from simulation_engine import run_simulation  # assuming we have this already
def analyze_market(market_name):
    print(f"Analyzing strategies for {market_name}...")
    results = []
    # Example: simulate different strategies (can be expanded)
    strategies = ["Aggressive", "Moderate", "Conservative"]
    for strategy in strategies:
        output = run_simulation(market_name, strategy)
        results.append({"strategy": strategy, **output})
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results

def recommend_top_strategies(markets):
    all_results = {}
    for market in markets:
        market_results = analyze_market(market)
        all_results[market] = market_results
    return all_results

def rollout_plan(all_results):
    # Flatten and sort globally
    flattened = []
    for market, results in all_results.items():
        for result in results:
            flattened.append({"market": market, **result})
    flattened.sort(key=lambda x: x["final_score"], reverse=True)
    return flattened[:5]  # top 5 global rollout suggestions

if __name__ == "__main__":
    # quick test
    markets = ["India", "LatAm", "SEA"]
    results = recommend_top_strategies(markets)
    top_rollout = rollout_plan(results)
    for plan in top_rollout:
        print(plan)  # preview plan
