"""
EcoTrace Dashboard - Streamlit
"""

import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="EcoTrace Dashboard",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ EcoTrace Dashboard")
st.markdown("AI-Driven Sustainability Traceability for Fashion Supply Chains")

st.divider()

# Sidebar
page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📍 Facilities",
    "🏭 Facility Details",
    "🎯 Brand Dashboard",
    "ℹ️ About"
])

if page == "🏠 Overview":
    st.subheader("Welcome to EcoTrace")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Facilities", "30")
    with col2:
        st.metric("Avg. Risk Score", "45/100")
    with col3:
        st.metric("High-Risk", "8")
    with col4:
        st.metric("Regions", "4")
    
    st.divider()
    st.markdown("""
    ### How It Works
    1. Satellite data collection (Sentinel-2)
    2. Feature extraction (NDVI, NDWI, BSI)
    3. AI scoring (XGBoost model)
    4. Supply chain mapping
    5. Transparency scores
    """)

elif page == "📍 Facilities":
    st.subheader("Facility Monitoring")
    st.info("30 facilities monitored across India, Vietnam, Pakistan, Bangladesh")
    
    # Sample data
    data = {
        "Facility": ["Mill-A", "Dye-B", "Weave-C"],
        "Country": ["India", "Vietnam", "Pakistan"],
        "Type": ["Spinning", "Dyeing", "Weaving"],
        "Risk": [35, 65, 42],
        "Score": [65, 35, 58]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

elif page == "🏭 Facility Details":
    st.subheader("Facility Analysis")
    
    facility = st.selectbox("Select Facility", ["Mill-A", "Dye-B", "Weave-C"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Water Stress", "65/100")
    with col2:
        st.metric("Deforestation", "35/100")
    with col3:
        st.metric("Pollution", "42/100")
    with col4:
        st.metric("Overall", "47/100")

elif page == "🎯 Brand Dashboard":
    st.subheader("Brand Sustainability Score")
    
    brand = st.selectbox("Select Brand", ["SUSMIE'S", "Ananas Anam"])
    
    st.metric("Sustainability Score", "62/100", "+5")
    
    st.markdown("""
    ### Supply Chain Breakdown
    - 60% from low-risk supplier
    - 25% from medium-risk supplier
    - 15% from high-risk supplier
    """)

elif page == "ℹ️ About":
    st.markdown("""
    ## About EcoTrace
    
    EcoTrace uses satellite data + AI to provide objective sustainability scores
    for fashion supply chains.
    
    ### Key Features
    - Real-time monitoring
    - Objective satellite data
    - No supplier cooperation needed
    - 50-100× cheaper than audits
    
    ### Model Performance
    - R² = 0.73
    - MAE = 7.2 points
    - 85% confidence
    """)

st.divider()
st.markdown("**EcoTrace MVP** | ESADE BAIB 2025-2026")
