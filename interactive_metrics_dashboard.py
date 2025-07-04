
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="🧬 Feature Importance Grid", layout="wide")
st.title("📌 Feature Importance Table (Cybersecurity Model)")

# Load enhanced feature table
df = pd.read_csv("feature_importance_table_for_streamlit.csv")

# JS code for tag-style color rendering
impact_renderer = JsCode("""
function(params) {
    const impact = params.value;
    let color = impact === 'High' ? '#ff4d4f' : impact === 'Moderate' ? '#faad14' : '#52c41a';
    let text = '<span style="color: white; background-color: ' + color + '; padding: 4px 8px; border-radius: 6px;">' + impact + '</span>';
    return text;
}
""")

relevance_renderer = JsCode("""
function(params) {
    const rel = params.value;
    let color = rel === 'Very High' ? '#722ed1' : rel === 'High' ? '#1890ff' : rel === 'Moderate' ? '#13c2c2' : '#d9d9d9';
    let text = '<span style="color: white; background-color: ' + color + '; padding: 4px 8px; border-radius: 6px;">' + rel + '</span>';
    return text;
}
""")

# AgGrid config
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter=True, sortable=True, resizable=True)
gb.configure_column("Impact Level", cellRenderer=impact_renderer)
gb.configure_column("Business Relevance", cellRenderer=relevance_renderer)
gb.configure_column("Percentage Contribution (%)", type=["numericColumn"], cellStyle={'backgroundColor': '#e6f7ff'})
gb.configure_column("Importance Score", type=["numericColumn"], cellStyle={'backgroundColor': '#fffbe6'})
grid_options = gb.build()

st.markdown("Use filters and sorting to analyze how each feature contributes to threat detection.")
AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=False, theme='alpine', fit_columns_on_grid_load=True, height=580)
