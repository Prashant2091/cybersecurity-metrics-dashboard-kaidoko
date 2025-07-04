
import streamlit as st
import plotly.graph_objects as go

# Data
labels = ['Normal Users', 'Malicious Users']
metrics = {
    'F1-Score': [93.68, 92.40],
    'Precision': [91.55, 95.06],
    'Recall': [95.92, 89.88],
    'Accuracy': [94.2, 93.1]
}
colors = ['#2563eb', '#fb923c']

# Sidebar Controls
st.sidebar.title("🔧 Controls")
metric_selected = st.sidebar.selectbox("Choose a Metric to Compare:", list(metrics.keys()))
simulate = st.sidebar.checkbox("🔄 Simulate Malicious Value")

# Optional slider if simulate is checked
if simulate:
    malicious_val = st.sidebar.slider("Adjust Malicious Score:", min_value=85.0, max_value=100.0,
                                       value=metrics[metric_selected][1], step=0.1)
    values = [metrics[metric_selected][0], malicious_val]
else:
    values = metrics[metric_selected]

# Title
st.title("📊 Interactive Binary Classification Dashboard")
st.markdown("Use the controls to explore subtle differences across classification metrics.")

# Chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=labels,
    y=values,
    marker_color=colors,
    text=[f"{v:.2f}%" for v in values],
    textposition='outside',
    name=metric_selected
))
fig.update_layout(
    title=f"{metric_selected} Comparison (Normal vs Malicious)",
    yaxis=dict(title='Score (%)', range=[85, 100], tickformat=".0f"),
    xaxis=dict(title='Class'),
    bargap=0.4,
    plot_bgcolor='white',
    font=dict(size=14),
    margin=dict(l=40, r=30, t=60, b=40)
)
st.plotly_chart(fig, use_container_width=True)

# Dynamic Insight
gap = abs(values[0] - values[1])
diff_class = labels[0] if values[0] > values[1] else labels[1]
comment = "🔎 Differences are minimal." if gap < 1 else f"📌 {diff_class} is outperforming by {gap:.2f}%"

st.markdown(f"""
### 📈 Insight
- **Metric:** {metric_selected}  
- **Difference:** {gap:.2f}% between classes  
- **Observation:** {comment}
""")
