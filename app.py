import streamlit as st
import pandas as pd
import time
from engine import DigitalTwinEngine

st.set_page_config(page_title="ETC Digital Twin", layout="wide")
st.title("🛰️ Event-Triggered Digital Twin")

# Sidebar Configuration
st.sidebar.header("Control Parameters")
sigma = st.sidebar.slider("Trigger Threshold (Sigma)", 0.01, 0.50, 0.10)
run_sim = st.sidebar.button("Start Simulation")

if run_sim:
    engine = DigitalTwinEngine(sigma=sigma)
    
    # Placeholders for live updates
    chart_placeholder = st.empty()
    metric_placeholder = st.columns(3)
    
    history = []

    for t in range(50):
        phys, twin, triggered = engine.update_step()
        
        history.append({
            "step": t,
            "Physical_Pos": phys[0][0],
            "Twin_Pos": twin[0][0],
            "Triggered": 1 if triggered else 0
        })
        
        df = pd.DataFrame(history)

        # Update Metrics
        metric_placeholder[0].metric("Physical State", round(phys[0][0], 3))
        metric_placeholder[1].metric("Twin State", round(twin[0][0], 3))
        metric_placeholder[2].metric("Sync Events", df["Triggered"].sum())

        # Update Chart
        chart_placeholder.line_chart(df.set_index("step")[["Physical_Pos", "Twin_Pos"]])
        
        time.sleep(0.1) # Simulate real-time data flow
