
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder
import random

st.set_page_config(page_title="🧠 Elite Cybersecurity Metrics Dashboard", layout="wide")

# --- Simulated Metric Data ---
labels = ["Normal Users", "Malicious Users"]
base_metrics = {
    "F1-Score": [93.68, 92.40],
    "Precision": [91.55, 95.06],
    "Recall": [95.92, 89.88],
    "Accuracy": [94.2, 93.1]
}
colors = ["#2563eb", "#fb923c"]

st.title("🧠 Elite Cybersecurity Metrics Dashboard")
st.markdown("Explore metrics, simulate threat score impact, and investigate features in real time.")

# --- Top Metric Summary Cards ---
st.markdown("## 🔢 Metric Overview")

cols = st.columns(4)
for i, (metric, vals) in enumerate(base_metrics.items()):
    diff = round(vals[0] - vals[1], 2)
    indicator = "🟢" if abs(diff) < 1 else ("🟡" if abs(diff) < 2 else "🔴")
    color = "green" if abs(diff) < 1 else ("orange" if abs(diff) < 2 else "red")
    with cols[i]:
        st.metric(label=f"{metric}", value=f"{vals[0]:.2f}% vs {vals[1]:.2f}%", delta=f"{diff:+.2f}%", delta_color=color)

# --- Live Dumbbell Plot Section ---
st.markdown("## 🎯 Class Performance Delta")
metric_selected = st.selectbox("Select metric to visualize:", list(base_metrics.keys()))
val1, val2 = base_metrics[metric_selected]

fig = go.Figure()
fig.add_trace(go.Scatter(x=[val1, val2], y=[0, 0],
                         mode='lines+markers+text',
                         text=labels,
                         marker=dict(size=14, color=colors),
                         line=dict(color='gray', width=4)))
fig.update_layout(title=f"{metric_selected} Comparison", xaxis=dict(range=[85, 100], title='Score (%)'),
                  yaxis=dict(showticklabels=False), height=200, margin=dict(t=40, b=20, l=50, r=30))
st.plotly_chart(fig, use_container_width=True)

# --- Simulation Panel ---
st.markdown("## 🔁 Simulate Malicious Class Shift")
simulate_val = st.slider("Simulate Malicious Score Change", 85.0, 100.0, val2, 0.1)
gap = abs(val1 - simulate_val)
trend = "🟢 Balanced" if gap < 1 else "🟡 Moderate Shift" if gap < 2 else "🔴 Large Deviation"

st.info(f"Current gap after simulation: {gap:.2f}% → {trend}")

# --- Feature Table Explorer ---
st.markdown("## 📌 Feature Importance Lens (Interactive)")
features = pd.DataFrame({
    "Feature": ["ip_bad_rep", "geo_suspicion", "lolbin_ua", "rare_tld", "domain_risk"],
    "Importance": [round(random.uniform(0.2, 0.95), 2) for _ in range(5)],
    "Type": ["IP", "Geo", "UA", "TLD", "Domain"],
    "Source": ["Blacklist", "GeoIP", "Header", "Parsed", "Threat Model"]
})
features["Impact"] = (features["Importance"] * 100).round(1)

# AgGrid Setup
gb = GridOptionsBuilder.from_dataframe(features)
gb.configure_default_column(editable=False, groupable=True)
gb.configure_grid_options(domLayout='normal')
AgGrid(features, gridOptions=gb.build(), height=250, theme='streamlit')

# Footer
st.markdown("---")
st.markdown("💡 Tip: Use the simulation above to see how shifts in malicious class metrics affect gap insights.")
