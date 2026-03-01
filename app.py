import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Aladdin Lite: Risk Engine", layout="wide")
st.title("🛡️ Institutional IPO Risk Engine (Aladdin Lite)")

# --- 2. DATA LOADING (CLOUD-SAFE) ---
# This looks for the file in the same folder as the script, whether on Windows or Linux
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "ipo_data.csv")

@st.cache_data
def load_data():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()

df = load_data()

# Stop the app if data is missing so it doesn't crash
if df.empty:
    st.error(f"Dataset not found at {csv_path}. Please ensure 'ipo_data.csv' is in your GitHub repo.")
    st.stop()

# --- 3. THE RISK SIMULATOR (Monte Carlo) ---
def run_monte_carlo(mean_return, vol, initial_val=100000, days=252, sims=1000):
    dt = 1/days
    paths = np.zeros((days, sims))
    paths[0] = initial_val
    for t in range(1, days):
        z = np.random.standard_normal(sims)
        # Geometric Brownian Motion formula
        paths[t] = paths[t-1] * np.exp((mean_return - 0.5 * vol**2) * dt + vol * np.sqrt(dt) * z)
    return paths

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.header("Risk Parameters")
investment = st.sidebar.number_input("Investment Amount (₹)", value=100000)
conf_level = st.sidebar.slider("Confidence Level (%)", 90, 99, 95)
market_vol = st.sidebar.select_slider("Market Volatility Environment", options=["Low", "Normal", "High", "Black Swan"])

vol_map = {"Low": 0.15, "Normal": 0.25, "High": 0.45, "Black Swan": 0.80}
current_vol = vol_map[market_vol]

# --- 5. CALCULATIONS & DASHBOARD ---
avg_gain = df['Listing Gain %'].mean() / 100

# Run the Engine
simulation_results = run_monte_carlo(avg_gain, current_vol, initial_val=investment)
final_prices = simulation_results[-1]

# VaR and CVaR (Expected Shortfall)
var_limit = np.percentile(final_prices, 100 - conf_level)
cvar_limit = final_prices[final_prices <= var_limit].mean()

# --- 6. DISPLAY METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("Expected Portfolio Value", f"₹{final_prices.mean():,.2f}")
m2.metric(f"VaR ({conf_level}%)", f"₹{investment - var_limit:,.2f}", delta_color="inverse")
m3.metric("Tail Risk (CVaR)", f"₹{investment - cvar_limit:,.2f}")

# --- 7. VISUALIZATIONS ---
st.subheader("Simulated Market Paths (1,000 Scenarios)")
fig_paths = px.line(simulation_results[:, :50], labels={'index': 'Days', 'value': 'Value (₹)'})
fig_paths.update_layout(showlegend=False)
st.plotly_chart(fig_paths, use_container_width=True)

st.subheader("Probability Distribution of Final Returns")
fig_hist = px.histogram(final_prices, nbins=50, labels={'value': 'Final Value'}, title="Distribution of Possible Outcomes")
fig_hist.add_vline(x=var_limit, line_dash="dash", line_color="red", annotation_text="VaR Threshold")
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Raw IPO Data Insights")
st.dataframe(df.head(10), use_container_width=True)