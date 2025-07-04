
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Setup
st.set_page_config(page_title="Cybersecurity Live Metrics", layout="wide")

# Sample data
labels = ["Normal Users", "Malicious Users"]
metric_values = {
    "F1-Score": [93.68, 92.40],
    "Precision": [91.55, 95.06],
    "Recall": [95.92, 89.88],
    "Accuracy": [94.2, 93.1]
}
colors = ["#2563eb", "#fb923c"]

# Sidebar - Metric Selector
st.sidebar.header("🔧 Select & Simulate")
selected_metric = st.sidebar.radio("Select Metric", list(metric_values.keys()))

simulate = st.sidebar.checkbox("Adjust Malicious Score")
if simulate:
    new_val = st.sidebar.slider("New Malicious Score", 85.0, 100.0, metric_values[selected_metric][1], 0.1)
    values = [metric_values[selected_metric][0], new_val]
else:
    values = metric_values[selected_metric]

# Live Metric Comparison Chart
st.title("🧠 Cybersecurity Metrics: Real-Time Comparison")
st.markdown("This live dashboard compares model performance across Normal vs Malicious user classes.")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=labels,
    y=values,
    marker_color=colors,
    text=[f"{v:.2f}%" for v in values],
    textposition="outside"
))
fig.update_layout(
    title=f"{selected_metric} Comparison",
    yaxis=dict(title="Score (%)", range=[85, 100]),
    xaxis=dict(title="User Type"),
    margin=dict(l=40, r=30, t=60, b=40),
    plot_bgcolor="white",
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)

# Dynamic Gap Interpretation
gap = round(abs(values[0] - values[1]), 2)
leading = labels[0] if values[0] > values[1] else labels[1]
if gap < 0.5:
    status = "🟢 Balanced — Minimal performance gap"
elif gap < 2:
    status = f"🟡 Mild difference — {leading} leads by {gap:.2f}%"
else:
    status = f"🔴 Significant gap — {leading} dominates by {gap:.2f}%"

st.subheader("📊 Interpretation")
st.success(status)

# Interactive Feature Simulation (Real-Time Table)
st.subheader("📌 Simulated Feature Table (Live Interaction)")
df = pd.DataFrame({
    "Feature": ["ip_bad_rep", "geo_suspicion", "user_agent_lolbin", "domain_freq"],
    "Importance": [0.87, 0.76, 0.52, 0.34],
    "Category": ["IP", "Geo", "UA", "Domain"],
    "Source": ["Threat DB", "GeoIP", "Header", "Parsed Domain"]
})
df["Impact (%)"] = df["Importance"].apply(lambda x: round(x * 100, 1))

# Display interactive table with sort + style
styled_df = df.sort_values(by="Importance", ascending=False).style.background_gradient(subset=["Impact (%)"], cmap="Blues")
st.dataframe(styled_df, use_container_width=True)
