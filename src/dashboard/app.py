import streamlit as st

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
    "Recent Intelligence Events"
)

if events:

    for event in events:

        st.write(
            f"**{event[1]}**"
        )

        st.write(
            f"Event: {event[3]}"
        )

        st.write(
            f"Severity: {event[5]}"
        )

        st.write(
            f"Relevance Score: {event[6]}"
        )

        st.write(
            f"Source: {event[2]}"
        )

        st.divider()

else:

    st.warning(
        "No events available."
    )