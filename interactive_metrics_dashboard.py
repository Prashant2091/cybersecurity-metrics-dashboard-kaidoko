
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="🧬 Feature Importance Grid", layout="wide")
st.title("📌 Feature Importance Table (Cybersecurity Model)")

# Load enhanced feature table
df = pd.read_csv("feature_importance_table_for_streamlit.csv")

# Define JS code for cell color rendering
impact_renderer = JsCode("""
function(params) {
    if (params.value == 'High') {
        return '<span style="color: white; background-color: #ff4d4f; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    } else if (params.value == 'Moderate') {
        return '<span style="color: black; background-color: #faad14; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    } else {
        return '<span style="color: white; background-color: #52c41a; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    }
}
""")

relevance_renderer = JsCode("""
function(params) {
    if (params.value == 'Very High') {
        return '<span style="color: white; background-color: #722ed1; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    } else if (params.value == 'High') {
        return '<span style="color: white; background-color: #1890ff; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    } else if (params.value == 'Moderate') {
        return '<span style="color: black; background-color: #13c2c2; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    } else {
        return '<span style="color: black; background-color: #d9d9d9; padding: 4px; border-radius: 4px;">' + params.value + '</span>'
    }
}
""")

# Setup AgGrid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter=True, sortable=True, resizable=True)
gb.configure_column("Impact Level", cellRenderer=impact_renderer)
gb.configure_column("Business Relevance", cellRenderer=relevance_renderer)
gb.configure_column("Percentage Contribution (%)", type=["numericColumn"], cellStyle={'backgroundColor': '#e6f7ff'})
gb.configure_column("Importance Score", type=["numericColumn"], cellStyle={'backgroundColor': '#fffbe6'})
grid_options = gb.build()

st.markdown("Use filters and sorting to analyze how each feature contributes to threat detection.")
AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=False, theme='alpine', fit_columns_on_grid_load=True, height=550)
