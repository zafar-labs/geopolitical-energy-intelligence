import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Handle repository pathing
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.analysis.intelligence_engine import IntelligenceEngine

# ---------------------------------------------------------
# SETUP & HELPER FUNCTIONS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Pakistan Geopolitical Intelligence Platform",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_status_badge(level):
    """Generates visual color-coded badges for risk levels."""
    level_clean = str(level).strip().upper().replace("_", " ")
    if level_clean in ["CRITICAL", "VERY HIGH"]:
        return "🔴 **VERY HIGH**"
    elif level_clean == "HIGH":
        return "🟠 **HIGH**"
    elif level_clean == "MEDIUM":
        return "🟡 **MEDIUM**"
    elif level_clean == "LOW":
        return "🟢 **LOW**"
    return f"⚪ **{level_clean}**"

def format_label(text):
    """Converts snake_case to Title Case."""
    return str(text).replace("_", " ").title()

# ---------------------------------------------------------
# DATA FETCHING (THE COP CLIENT)
# ---------------------------------------------------------
@st.cache_data(ttl=300) # Caches the data for 5 minutes to prevent DB spam on UI reloads
def fetch_intelligence():
    engine = IntelligenceEngine()
    return engine.build_common_operational_picture()

cop = fetch_intelligence()

# Unpack the Common Operational Picture
risk_summary = cop.get("risk", {})
executive = cop.get("executive_assessment", {})
metrics = cop.get("metrics", {})
events = cop.get("recent_events", [])
risk_clusters = cop.get("risk_clusters", {})
commodity_exposure = cop.get("commodity_exposure", {})
domain_assessment = cop.get("domain_assessment", {})
pakistan_exposure = cop.get("pakistan_exposure", {})
cascade_effects = cop.get("cascade_effects", {"first_order": [], "second_order": [], "third_order": []})
escalation_indicators = cop.get("escalation_indicators", {"high_confidence": [], "medium_confidence": [], "monitoring": []})
forecast = cop.get("forecast", {})

# ---------------------------------------------------------
# UI RENDERING
# ---------------------------------------------------------

st.title("🛰️ Pakistan Geopolitical Intelligence Platform")
st.caption("Strategic Energy Security | Common Operational Picture (COP)")

header_left, header_center, header_right = st.columns([2, 1, 1])
with header_left:
    st.write(f"**Generated:** {cop['generated_at']}")
with header_center:
    st.metric("Overall Risk", format_label(risk_summary.get("overall_risk", "UNKNOWN")))
with header_right:
    st.metric("Composite Score", risk_summary.get("composite_score", 0))

st.divider()

# =========================================================
# SECTION 1: EXECUTIVE SUMMARY
# =========================================================
st.header("1. Executive Summary")

metric1, metric2, metric3, metric4 = st.columns(4)
with metric1:
    st.metric("Events Assessed", risk_summary.get("assessed_events", 0))
with metric2:
    st.metric("Events Observed", metrics.get("total_events", 0))
with metric3:
    st.metric("Confirmed Signals", metrics.get("confirmed_events", 0))
with metric4:
    st.metric("High-Risk Domains", risk_summary.get("high_risk_domains", 0))

st.write("")

# The BLUF (Bottom Line Up Front)
if executive.get("risk_statement"):
    st.info(f"**Bottom Line Up Front (BLUF)**\n\n{executive['risk_statement']}")

st.write("")

# Top Strategic Risks Ranking (Enhanced Visual Presentation)
st.subheader("Top Strategic Risks")
if risk_clusters:
    # Sort by highest score first
    sorted_clusters = sorted(risk_clusters.items(), key=lambda x: x[1]["score"], reverse=True)
    
    for idx, (cluster_name, details) in enumerate(sorted_clusters[:3], start=1):
        score = details["score"]
        # Match alerts dynamically to their threshold severity styles
        if score >= 13:
            st.error(f"**{idx}. {cluster_name}** (Score: {score}) — Critical Operational Threat")
        elif score >= 9:
            st.warning(f"**{idx}. {cluster_name}** (Score: {score}) — High Exposure Threat")
        else:
            st.info(f"**{idx}. {cluster_name}** (Score: {score}) — Active Monitored Cluster")
else:
    st.caption("No active strategic risk clusters detected.")

st.markdown("---")

# =========================================================
# SECTION 2: OPERATIONAL PICTURE
# =========================================================
st.header("2. Operational Picture")

op_col1, op_col2 = st.columns(2)

with op_col1:
    st.subheader("Domain Risk Assessment")
    with st.container(border=True):
        sorted_domains = sorted(domain_assessment.items(), key=lambda x: x[1]["score"], reverse=True)
        for domain, details in sorted_domains:
            st.markdown(f"**{format_label(domain)}**")
            st.progress(min(details["score"] / 30, 1.0))
            st.caption(f"Risk Level: {format_label(details['risk_level'])}")
            st.write("")

    st.subheader("Commodity Exposure")
    with st.container(border=True):
        if commodity_exposure:
            for commodity, exposure in sorted(commodity_exposure.items()):
                st.markdown(f"**{format_label(commodity)}** &nbsp;—&nbsp; {get_status_badge(exposure)}")
        else:
            st.caption("No critical commodity exposures.")

with op_col2:
    st.subheader("Pakistan Infrastructure Impact")
    with st.container(border=True):
        st.markdown("**Strategic Dependencies At Risk:**")
        deps = pakistan_exposure.get("strategic_dependencies", [])
        if deps:
            for item in deps: st.markdown(f"- {item}")
        else:
            st.caption("None detected")
            
        st.write("")
        st.markdown("**Immediate Network Effects:**")
        imm_eff = pakistan_exposure.get("immediate_effects", [])
        if imm_eff:
            for item in imm_eff: st.markdown(f"- {item}")
        else:
            st.caption("None detected")

st.markdown("---")

# =========================================================
# SECTION 3: OPERATIONAL INTELLIGENCE
# =========================================================
st.header("3. Operational Intelligence")

st.subheader("Implicated Risk Clusters")
if risk_clusters:
    for cluster_name, details in risk_clusters.items():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {cluster_name}")
                st.write(f"Combined Score: {details['score']}")
            with col2:
                st.write("")
                st.markdown(get_status_badge(details.get("risk_level", "HIGH")))

            st.write("**Associated Events:**")
            for event in details["events"]:
                st.markdown(f"- {event}")
else:
    st.caption("No clustered threats mapped.")

st.write("")
st.subheader("Live Event Telemetry")
if events:
    df_events = pd.DataFrame(events)
    df_events = df_events[["headline", "severity", "source", "relevance"]]
    df_events["severity"] = df_events["severity"].apply(format_label)
    df_events["source"] = df_events["source"].apply(format_label)
    df_events.columns = ["Event Headline", "Severity", "Intelligence Source", "Relevance"]
    
    st.dataframe(df_events, use_container_width=True, hide_index=True)
else:
    st.info("No active intelligence events in the current timeframe.")

st.markdown("---")

# =========================================================
# SECTION 4: STRATEGIC OUTLOOK
# =========================================================
st.header("4. Strategic Outlook")

out_col1, out_col2 = st.columns(2)

with out_col1:
    st.subheader("Cascading Effects Matrix")
    with st.container(border=True):
        st.markdown("**First-Order (Immediate):**")
        for item in cascade_effects.get("first_order", []): st.markdown(f"- {item}")
        
        st.markdown("**Second-Order (Delayed):**")
        for item in cascade_effects.get("second_order", []): st.markdown(f"- {item}")
        
        st.markdown("**Third-Order (Systemic):**")
        for item in cascade_effects.get("third_order", []): st.markdown(f"- {item}")

with out_col2:
    st.subheader("Escalation Indicators (PIRs)")
    with st.container(border=True):
        st.markdown("**High Confidence Triggers:**")
        for item in escalation_indicators.get("high_confidence", []): st.markdown(f"- 🎯 {item}")
        
        st.markdown("**Medium Confidence Triggers:**")
        for item in escalation_indicators.get("medium_confidence", []): st.markdown(f"- ⚠️ {item}")
        
        st.markdown("**Baseline Monitoring:**")
        for item in escalation_indicators.get("monitoring", []): st.markdown(f"- 👁️ {item}")

st.write("")
st.subheader("Scenario Forecasts")
if forecast:
    for event_id, scenario in forecast.items():
        with st.expander(f"Scenario Assessment: {scenario['event_name']}"):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.info(f"**Most Likely**\n\n{scenario['most_likely']}")
            with f_col2:
                st.error(f"**Severe Case**\n\n{scenario['severe_case']}")
            with f_col3:
                st.success(f"**Best Case**\n\n{scenario['best_case']}")
else:
    st.caption("No predictive models currently mapped to live events.")

st.divider()

# Footer
footer_left, footer_right = st.columns([3, 1])
with footer_left:
    st.caption("Pakistan Geopolitical Intelligence Platform • Version 1.0")
with footer_right:
    st.caption(f"Generated: {cop['generated_at']}")