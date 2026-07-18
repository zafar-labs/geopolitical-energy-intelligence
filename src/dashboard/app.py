import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

def render_domain_risk_chart(domain_assessment):
    """
    Render a horizontal bar chart showing
    comparative domain risk.
    """

    if not domain_assessment:
        return

    sorted_domains = sorted(
        domain_assessment.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    labels = [
        format_label(domain)
        for domain, _ in sorted_domains
    ]

    scores = [
        details["score"]
        for _, details in sorted_domains
    ]

    fig, ax = plt.subplots(figsize=(6, 2.8))

    ax.barh(labels, scores)

    ax.invert_yaxis()

    ax.tick_params(axis="y", labelsize=8)
    ax.tick_params(axis="x", labelsize=8)

    ax.set_xlabel("Risk Score")

    ax.set_title("Comparative Domain Risk")

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

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
analytical_judgment = cop.get(
    "analytical_judgment",
    []
)
metrics = cop.get("metrics", {})
events = cop.get("recent_events", [])
risk_clusters = cop.get("risk_clusters", {})
commodity_exposure = cop.get("commodity_exposure", {})
domain_assessment = cop.get("domain_assessment", {})
pakistan_exposure = cop.get("pakistan_exposure", {})
cascade_effects = cop.get("cascade_effects", {"first_order": [], "second_order": [], "third_order": []})
escalation_indicators = cop.get("escalation_indicators", {"high_confidence": [], "medium_confidence": [], "monitoring": []})
forecast = cop.get("forecast", {})
confidence_summary = cop.get("confidence", {})

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
with st.container(border=True):

    st.subheader("Executive Briefing")

    st.markdown(
        executive.get(
            "risk_statement",
            "No executive assessment available."
        )
    )

    st.write("")

    brief_col1, brief_col2 = st.columns(2)

    with brief_col1:

        st.markdown("**Primary Driver**")

        drivers = executive.get(
            "primary_drivers",
            []
        )

        if drivers:
            st.write(drivers[0])
        else:
            st.caption("None identified.")

        st.write("")

        st.markdown("**Highest Exposure**")

        exposures = executive.get(
            "highest_exposures",
            []
        )

        if exposures:
            st.write(exposures[0])
        else:
            st.caption("None identified.")

    with brief_col2:

        st.markdown(
            "**Priority Intelligence Requirement**"
        )

        monitoring = executive.get(
            "priority_monitoring",
            []
        )

        if monitoring:
            st.write(monitoring[0])
        else:
            st.caption("No active PIRs.")

        st.write("")

        st.markdown(
            "**Operational Assessment**"
        )

        st.write(
            format_label(
                risk_summary.get(
                    "overall_risk",
                    "UNKNOWN"
                )
            )
        )

        st.divider()

        st.markdown("### Assessment Basis")

        if analytical_judgment:

            for statement in analytical_judgment:

                st.markdown(f"- {statement}")

        else:

            st.caption("No analytical justification available.")

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

st.subheader("Strategic Domain Risk Overview")

render_domain_risk_chart(
    domain_assessment
)

st.write("")

op_col1, op_col2 = st.columns(2)

with op_col1:

    # --------------------------------------------------
    # Domain Risk Assessment
    # --------------------------------------------------
    st.subheader("Domain Risk Breakdown")

    with st.container(border=True):

        sorted_domains = sorted(
            domain_assessment.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        for domain, details in sorted_domains:

            st.markdown(
                f"**{format_label(domain)}**"
            )

            progress = min(
                details["score"] / 30,
                1.0
            )

            st.progress(progress)

            st.caption(
                f"Score: {details['score']} | "
                f"{format_label(details['risk_level'])}"
            )

            st.write("")

    # --------------------------------------------------
    # Commodity Exposure
    # --------------------------------------------------
    st.subheader("Commodity Exposure")

    with st.container(border=True):

        if commodity_exposure:

            for commodity, exposure in sorted(
                commodity_exposure.items()
            ):

                left, right = st.columns([3, 1])

                with left:
                    st.markdown(
                        f"**{format_label(commodity)}**"
                    )

                with right:
                    st.markdown(
                        get_status_badge(exposure)
                    )

        else:

            st.caption(
                "No critical commodity exposures."
            )

    # --------------------------------------------------
    # Strategic Impact Areas
    # --------------------------------------------------
    st.subheader("Strategic Impact Areas")

    with st.container(border=True):

        areas = cop.get("impact_areas", [])

        if areas:

            for area in areas:
                st.markdown(f"- {area}")

        else:

            st.caption(
                "No strategic impact areas identified."
            )

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

st.subheader("Strategic Risk Clusters")

if risk_clusters:

    sorted_clusters = sorted(
        risk_clusters.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    for cluster_name, details in sorted_clusters:

        with st.container(border=True):

            top_left, top_right = st.columns([4, 1])

            with top_left:
                st.markdown(f"### {cluster_name}")

            with top_right:
                st.markdown(
                    get_status_badge(
                        details["risk_level"]
                    )
                )

            info1, info2 = st.columns(2)

            with info1:
                st.metric(
                    "Combined Score",
                    details["score"]
                )

            with info2:
                st.metric(
                    "Linked Events",
                    len(details["events"])
                )

            st.markdown("**Associated Events**")

            for event in details["events"]:
                st.markdown(f"• {event}")

else:

    st.info(
        "No correlated strategic risk clusters detected."
    )

st.write("")
st.subheader("Live Intelligence Feed")

if events:

    sorted_events = sorted(
        events,
        key=lambda event: event["relevance"],
        reverse=True
    )

    for idx, event in enumerate(sorted_events, start=1):

        with st.container(border=True):

            left, right = st.columns([5,1])

            with left:

                st.markdown(
                    f"**{idx}. {event['headline']}**"
                )

                st.caption(
                    f"Source: {event['source']}"
                )

            with right:

                st.markdown(
                    get_status_badge(
                        event["severity"]
                    )
                )

            st.progress(
                min(
                    event["relevance"] / 10,
                    1.0
                )
            )

            st.caption(
                f"Relevance Score: {event['relevance']}"
            )

else:

    st.info(
        "No active intelligence signals detected."
    )

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

st.write("")

st.subheader("Source Confidence Assessment")

if confidence_summary:

    for event_code, details in confidence_summary.items():

        with st.container(border=True):

            left, right = st.columns([4,1])

            with left:

                st.markdown(
                    f"**{event_code}**"
                )

                st.caption(
                    ", ".join(details["sources"])
                )

            with right:

                st.markdown(
                    get_status_badge(
                        details["confidence"]
                    )
                )

            st.progress(
                min(
                    details["composite_score"] / 20,
                    1.0
                )
            )

            stat1, stat2, stat3 = st.columns(3)

            stat1.metric(
                "Sources",
                details["confirmation_count"]
            )

            stat2.metric(
                "Reliability",
                details["reliability_score"]
            )

            stat3.metric(
                "Composite",
                details["composite_score"]
            )

else:

    st.caption(
        "No confidence assessment available."
    )

st.divider()

# Footer
st.divider()

st.subheader("System Status")

status1, status2, status3, status4 = st.columns(4)

status1.metric(
    "Platform",
    "Version 1.0"
)

status2.metric(
    "Events Cached",
    metrics.get("total_events", 0)
)

status3.metric(
    "Database",
    "ONLINE"
)

status4.metric(
    "Feed Status",
    "ACTIVE"
)

st.caption(
    f"Common Operational Picture generated at "
    f"{cop['generated_at']}"
)