
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="🔐 Cybersecurity Metrics Dashboard", layout="wide")

# --- DATA SETUP ---
labels = ['Normal Users', 'Malicious Users']
metrics = {
    'F1-Score': [93.68, 92.40],
    'Precision': [91.55, 95.06],
    'Recall': [95.92, 89.88],
    'Accuracy': [94.2, 93.1]
}
colors = ['#2563eb', '#fb923c']

# Load PNGs (visualizations)
image1 = "Final_Clear_Binary_Classification_Labels.png"
image2 = "final_explicit_feature_importance.png"

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🔧 Control Panel")
story_mode = st.sidebar.radio("Select Metric Story:", list(metrics.keys()))
simulate = st.sidebar.checkbox("🔄 Simulate Malicious Score")

if simulate:
    adjusted_val = st.sidebar.slider("Adjust Malicious Score", 85.0, 100.0, value=metrics[story_mode][1], step=0.1)
    story_values = [metrics[story_mode][0], adjusted_val]
else:
    story_values = metrics[story_mode]

# --- HEADER ---
st.title("🔐 Cybersecurity Classification Dashboard")
st.markdown("Real-time comparative insights across classification metrics and cybersecurity features.")

tab1, tab2 = st.tabs(["📊 Metric Explorer", "🧠 Feature Importance Explorer"])

# --- TAB 1: METRIC EXPLORER ---
with tab1:
    st.subheader(f"📈 {story_mode} Comparison")
    df = pd.DataFrame({'Class': labels, 'Score': story_values})

    fig = px.bar(df, x='Class', y='Score', color='Class',
                 text=[f"{v:.2f}%" for v in story_values],
                 color_discrete_sequence=colors)
    fig.update_layout(yaxis_range=[85, 100], yaxis_title='Score (%)', xaxis_title=None,
                      font=dict(size=14), plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    gap = abs(story_values[0] - story_values[1])
    better = labels[0] if story_values[0] > story_values[1] else labels[1]
    if gap < 1:
        msg = "🔍 Very tight performance. No significant lead."
    else:
        msg = f"📌 **{better}** is ahead by **{gap:.2f}%** on **{story_mode}**."

    st.markdown("### 📌 Insight")
    st.info(msg)

    st.markdown("### 🖼️ Snapshot Summary")
    st.image(image1, use_column_width=True)

# --- TAB 2: FEATURE IMPORTANCE EXPLORER ---
with tab2:
    st.subheader("🧠 Feature Importance Table")

    # Display PNG image
    st.image(image2, use_column_width=True)

    st.markdown("### 📘 Explanation:")
    st.markdown("""
    - **Importance Score**: Feature's predictive value
    - **Contribution %**: Relative weight in model
    - **Impact Level**: High, Moderate, or Low  
    - **Business Relevance**: How it affects cybersecurity decision-making
    """)
