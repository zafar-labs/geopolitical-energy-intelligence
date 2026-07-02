import streamlit as st
import pandas as pd

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

sys.path.append(
    str(project_root)
)

from src.storage.event_store import EventStore

st.set_page_config(
    page_title="Geopolitical Energy Intelligence",
    layout="wide"
)

st.title(
    "Geopolitical Energy Intelligence Dashboard"
)

store = EventStore()

from src.analysis.intelligence_engine import IntelligenceEngine

engine = IntelligenceEngine()

events = engine.get_recent_events()


metrics = engine.get_executive_metrics()

confidence_summary = (
    engine.get_confidence_summary()
)

st.subheader(
    "Executive Overview"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Events",
        metrics["total_events"]
    )

with col2:

    st.metric(
        "High-Risk Events",
        metrics["high_risk_events"]
    )

with col3:

    st.metric(
        "Confirmed Events",
        metrics["confirmed_events"]
    )

st.divider()

st.subheader(
    "Confidence Analysis"
)

confidence_rows = []

for event_code, details in confidence_summary.items():

    confidence_rows.append({

        "Event": event_code,

        "Confidence": details["confidence"],

        "Composite Score": details["composite_score"],

        "Confirmations": details["confirmation_count"]

    })

confidence_df = pd.DataFrame(
    confidence_rows
)

st.dataframe(
    confidence_df,
    use_container_width=True
)


st.subheader(
    "Recent Intelligence Events"
)

if events:

    event_rows = []

    for event in events:

        event_rows.append({
            "Headline": event.get("headline"),
            "Event ID": event.get("event_id"),
            "Severity": event.get("severity"),
            "Relevance": event.get("relevance"),
            "Source": event.get("source")
        })

    events_df = pd.DataFrame(
        event_rows
    )

    st.dataframe(
        events_df,
        use_container_width=True
    )

else:

    st.warning(
        "No events available."
    )