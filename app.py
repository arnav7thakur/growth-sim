# Streamlit App
# Global Growth Simulation Agent for Stimuler
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Core imports
from core.simulator import simulate_strategy
from data.strategy_effects import strategy_effects
from data.markets import markets
from core.planner import plan_strategy
from utils.file_parser import parse_uploaded_file

# Strategies list
strategies = list(strategy_effects.keys())

# App setup
st.set_page_config(page_title="Global Growth Simulation Agent", layout="wide")
st.title("🌍 Global Growth Simulation Agent")

st.markdown("""
Simulate digital growth strategies across key markets: **India**, **Indonesia**, and **Latin America**.
""")

# --- Company Data Upload ---
company_data = None
uploaded_file = st.file_uploader("📁 Upload your company data (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])
if uploaded_file:
    try:
        company_data = parse_uploaded_file(uploaded_file)
        st.success("✅ Company data uploaded and parsed successfully.")
    except Exception as e:
        st.error(f"❌ Failed to parse file: {str(e)}")

# --- Helper to simulate with optional company_data ---
def simulate_with_data(market, strategy, data=None):
    return simulate_strategy(market, strategy, company_data=data)

# --- TAB 1: Single Strategy Simulation ---
tab1, tab2 = st.tabs(["🔍 Single Strategy", "📊 Full Simulation"])

with tab1:
    selected_strategy = st.selectbox("Choose a Growth Strategy to Simulate", strategies)

    if st.button("Simulate Across Markets"):
        results = [simulate_with_data(market, selected_strategy, company_data) for market in markets.keys()]
        df = pd.DataFrame(results)

        baseline_results = [simulate_with_data(market, "baseline", company_data) for market in markets.keys()]
        baseline_df = pd.DataFrame(baseline_results)

        comparison_df = df.merge(baseline_df, on="Market", suffixes=("", "_baseline"))
        comparison_df["Delta_Score"] = comparison_df["Score"] - comparison_df["Score_baseline"]
        comparison_df["Delta_LTV"] = comparison_df["LTV"] - comparison_df["LTV_baseline"]
        comparison_df["Delta_CAC"] = comparison_df["CAC"] - comparison_df["CAC_baseline"]
        comparison_df["Delta_Retention"] = comparison_df["Retention"] - comparison_df["Retention_baseline"]

        st.subheader("📈 Delta vs. Baseline")
        st.dataframe(comparison_df[["Market", "Strategy", "Score", "Score_baseline", "Delta_Score"]], use_container_width=True)

        fig_delta = px.bar(
            comparison_df,
            x="Market",
            y="Delta_Score",
            color="Market",
            title="🚀 Improvement Over Baseline (Score Delta)"
        )
        st.plotly_chart(fig_delta, use_container_width=True)

        st.subheader("📊 Simulation Results")
        st.dataframe(df, use_container_width=True)

        fig = px.bar(df, x="Market", y="Score", color="Strategy", title="Strategy Effectiveness by Market")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Score Formula** = (LTV / CAC) × Retention")

# --- TAB 2: Full Simulation ---
with tab2:
    if st.button("Run Full Simulation"):
        full_results = []
        for market in markets.keys():
            full_results.append(simulate_with_data(market, "baseline", company_data))
            for strategy in strategies:
                full_results.append(simulate_with_data(market, strategy, company_data))

        full_df = pd.DataFrame(full_results)

        ranked_df = full_df.copy()
        ranked_df["Rank"] = ranked_df.groupby("Market")["Score"].rank(ascending=False, method="dense")
        ranked_df_sorted = ranked_df.sort_values(["Market", "Rank"])

        global_avg_df = full_df[full_df["Strategy"] != "baseline"].groupby("Strategy", as_index=False)["Score"].mean()
        global_avg_df = global_avg_df.sort_values("Score", ascending=False)

        st.subheader("🌐 Full Market × Strategy Simulation")

        show_top3 = st.checkbox("Show Only Top 3 Strategies per Market", value=False)
        if show_top3:
            filtered_df = ranked_df_sorted[ranked_df_sorted["Rank"] <= 3]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(ranked_df_sorted, use_container_width=True)

        heatmap_data = full_df.pivot(index="Market", columns="Strategy", values="Score")
        fig2 = px.imshow(
            heatmap_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="Heatmap: Strategy Score per Market"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🌍 Global Strategy Performance (Average Score Across All Markets)")
        st.dataframe(global_avg_df, use_container_width=True)

        fig3 = px.bar(global_avg_df, x="Strategy", y="Score", title="Top Performing Strategies (Global Average)", color="Strategy")
        st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: Advisor ---
tab3 = st.tabs(["📋 Strategy Advisor"])[0]

with tab3:
    st.subheader("💡 Personalized Strategy Recommendation")

    selected_market = st.selectbox("Choose a Market to Analyze", list(markets.keys()))

    if st.button("Run Advisor for Market"):
        baseline = simulate_with_data(selected_market, "baseline", company_data)
        strategy_results = [simulate_with_data(selected_market, s, company_data) for s in strategies]

        df = pd.DataFrame(strategy_results)
        baseline_score = baseline["Score"]
        df["Delta_Score"] = df["Score"] - baseline_score

        best_row = df.sort_values(by="Delta_Score", ascending=False).iloc[0]
        best_strategy = best_row["Strategy"]

        st.success(f"✅ Recommended Strategy for **{selected_market}**: **{best_strategy}**")
        st.metric(label="Best Score Improvement", value=round(best_row['Delta_Score'], 2))

        fig = px.bar(df, x="Strategy", y="Delta_Score", color="Strategy",
                     title=f"📈 Strategy Impact vs. Baseline in {selected_market}")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df[["Strategy", "Score", "Delta_Score", "CAC", "LTV", "Retention"]], use_container_width=True)

# --- Growth Goal Simulation ---
st.title("🚀 Growth Strategy Simulator")
st.write("Give me your growth goal, and I’ll simulate and recommend the best strategy!")

user_goal = st.text_input("🎯 What's your growth goal?", placeholder="e.g., improve retention, lower CAC, maximize growth")
selected_market = st.selectbox("🌍 Select a market", [""] + list(markets.keys()), key="goal_market")

if st.button("Simulate & Recommend") and user_goal:
    with st.spinner("Thinking like a strategist..."):
        recommendation = plan_strategy(user_goal, selected_market or None, company_data=company_data)

    if recommendation:
        st.success("📈 Recommended Strategy:")
        st.write(f"**Strategy**: {recommendation['Strategy']}")
        st.metric("Overall Score", round(recommendation["Score"], 2))
        st.metric("Retention", round(recommendation["Retention"], 2))
        st.metric("CAC", round(recommendation["CAC"], 2))
    else:
        st.error("Couldn't find a suitable strategy. Try rephrasing the goal?")
