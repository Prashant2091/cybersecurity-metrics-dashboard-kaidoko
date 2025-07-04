
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

# Data
labels = ['Normal Users', 'Malicious Users']
metrics = {
    'F1-Score': [93.68, 92.40],
    'Precision': [91.55, 95.06],
    'Recall': [95.92, 89.88],
    'Accuracy': [94.2, 93.1]
}
colors = ['#2563eb', '#fb923c']

st.set_page_config(page_title="Binary Classification Insights", layout="wide")
st.title("📊 Binary Classification: Interactive Performance & Insights")

tab1, tab2 = st.tabs(["📈 Model Performance", "🧠 Feature Importance"])

# Tab 1: Metrics
with tab1:
    st.header("Class-wise Performance Comparison")
    metric_selected = st.selectbox("Choose a Metric to Compare:", list(metrics.keys()))
    simulate = st.checkbox("Simulate Malicious Class Score")

    if simulate:
        malicious_val = st.slider("Adjust Malicious Score:", 85.0, 100.0,
                                  value=metrics[metric_selected][1], step=0.1)
        values = [metrics[metric_selected][0], malicious_val]
    else:
        values = metrics[metric_selected]

    # Plot
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

    gap = abs(values[0] - values[1])
    diff_class = labels[0] if values[0] > values[1] else labels[1]
    comment = "Minimal performance variation." if gap < 1 else f"**{diff_class} is stronger by {gap:.2f}%**"

    st.markdown(f"### 🧾 Interpretation")
    st.markdown(f"""
    - **Metric:** {metric_selected}  
    - **Difference:** {gap:.2f}% between classes  
    - **Insight:** {comment}
    """)

    # Static image preview
    st.markdown("### 🖼️ Overall Visual Summary")
    image = Image.open("Final_Clear_Binary_Classification_Labels.png")
    st.image(image, use_column_width=True, caption="Detailed Multi-Metric Visualization")

# Tab 2: Feature Importance
with tab2:
    st.header("Cybersecurity Threat Feature Importance")
    st.markdown("The table below summarizes which features are most influential in threat prediction.")
    image = Image.open("final_explicit_feature_importance.png")
    st.image(image, use_column_width=True, caption="Comprehensive Feature Importance Table")

    st.markdown("""
    ### 🔍 Legend Highlights
    - **Color-coded scores**: Importance, contribution, and impact
    - **Business relevance** and **feature origin** are clearly mapped
    - Designed for cybersecurity applications with real-world mapping
    """)
