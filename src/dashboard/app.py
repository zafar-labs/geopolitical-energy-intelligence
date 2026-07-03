import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Fix path resolutions for deep project-root module resolution
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.analysis.intelligence_engine import IntelligenceEngine

st.set_page_config(
    page_title="Geopolitical Energy Intelligence",
    layout="wide"
)

st.title("Geopolitical Energy Intelligence Dashboard")

# Initialize Engine and generate the Unified Common Operational Picture
engine = IntelligenceEngine()
cop = engine.build_common_operational_picture()

# Extract pre-calculated data points from the unified operational picture
metrics = cop.get("metrics", {})
risk_summary = cop.get("risk", {})
confidence_summary = cop.get("confidence", {})
events = cop.get("recent_events", [])
commodity_exposure = cop.get("commodity_exposure", {})
pakistan_exposure = cop.get("pakistan_exposure", {})
risk_clusters = cop.get("risk_clusters", {})
forecast = cop.get("forecast", {})

# ---------------------------------------------------------
# 1. System Threat Banner & Executive Metrics Dashboard
# ---------------------------------------------------------
overall_risk = risk_summary.get("overall_risk", "LOW")
composite_risk = risk_summary.get("composite_risk", "LOW")

if overall_risk in ["CRITICAL", "HIGH"]:
    st.error(f"⚠️ SYSTEM RISK STATUS: {overall_risk} (Composite Assessment: {composite_risk})")
elif overall_risk == "MEDIUM":
    st.warning(f"⚡ SYSTEM RISK STATUS: MEDIUM")
else:
    st.success(f"✅ SYSTEM RISK STATUS: LOW")

st.subheader("Executive Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events (24h)", metrics.get("total_events", 0))
with col2:
    st.metric("High-Risk Events", metrics.get("high_risk_events", 0))
with col3:
    st.metric("Confirmed Incidents", metrics.get("confirmed_events", 0))
with col4:
    st.metric("Composite Score", risk_summary.get("composite_score", 0))

st.divider()

# ---------------------------------------------------------
# 2. National Exposure Matrices
# ---------------------------------------------------------
st.subheader("Strategic Vulnerability & Exposure Profile")
exp_col1, exp_col2 = st.columns(2)

with exp_col1:
    st.markdown("### 🛢️ Commodity Exposure Tracking")
    if commodity_exposure:
        comm_rows = [{"Commodity": k, "Exposure Level": v.upper()} for k, v in commodity_exposure.items()]
        st.dataframe(pd.DataFrame(comm_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No active market commodity exposures flagged.")

with exp_col2:
    st.markdown("### 🇵🇰 National Infrastructure Impact")
    tabs = st.tabs(["Strategic Dependencies", "Immediate Effects", "Delayed Risks"])
    
    with tabs[0]:
        if pakistan_exposure.get("strategic_dependencies"):
            for item in pakistan_exposure["strategic_dependencies"]:
                st.markdown(f"- {item}")
        else:
            st.caption("No critical dependencies disrupted.")
            
    with tabs[1]:
        if pakistan_exposure.get("immediate_effects"):
            for item in pakistan_exposure["immediate_effects"]:
                st.markdown(f"- 🔴 {item}")
        else:
            st.caption("No immediate network shocks detected.")
            
    with tabs[2]:
        if pakistan_exposure.get("delayed_effects"):
            for item in pakistan_exposure["delayed_effects"]:
                st.markdown(f"- ⏳ {item}")
        else:
            st.caption("No delayed structural effects predicted.")

st.divider()

# ---------------------------------------------------------
# 3. Dynamic Forward Scenario Assessments
# ---------------------------------------------------------
st.subheader("🔮 Predictive Scenario Forecasts")
if forecast:
    for event_id, scenario in forecast.items():
        with st.container(border=True):
            st.markdown(f"#### Target Trigger: **{scenario['event_name']}** (`{event_id}`)")
            
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.info("**Most Likely Scenario**")
                st.markdown(f"{scenario['most_likely']}")
                
            with f_col2:
                st.error("**Severe Case Scenario**")
                st.markdown(f"{scenario['severe_case']}")
                
            with f_col3:
                st.success("**Best Case Scenario**")
                st.markdown(f"{scenario['best_case']}")
else:
    st.info("No active structural forecasts associated with the current alerts pipeline.")

st.divider()

# ---------------------------------------------------------
# 4. Risk Clusters & Confidence Matrix Log
# ---------------------------------------------------------
st.subheader("Correlated Risk Clusters")
if risk_clusters:
    for cluster_name, details in risk_clusters.items():
        with st.expander(f"📌 Cluster: {cluster_name} (Aggregate Score: {details['score']})"):
            st.markdown("**Implicated Pipeline Events:**")
            for ev in details["events"]:
                st.markdown(f"- {ev}")
else:
    st.info("No cascading risk clusters identified in current execution window.")

st.subheader("Confidence Analysis")
if confidence_summary:
    confidence_rows = [{
        "Event Code": k,
        "Confidence Level": v["confidence"],
        "Composite Score": v["composite_score"],
        "Reporting Sources": len(v["sources"])
    } for k, v in confidence_summary.items()]
    st.dataframe(pd.DataFrame(confidence_rows), use_container_width=True, hide_index=True)

st.subheader("Recent Intelligence Events Log")
if events:
    event_rows = [{
        "Headline": e.get("headline"),
        "Event ID": e.get("event_id"),
        "Severity": e.get("severity", "").upper(),
        "Relevance": e.get("relevance"),
        "Source": e.get("source")
    } for e in events]
    st.dataframe(pd.DataFrame(event_rows), use_container_width=True, hide_index=True)
else:
    st.warning("No live telemetry raw events found in the database store.")