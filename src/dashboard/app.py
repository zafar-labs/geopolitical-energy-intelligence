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

events = store.fetch_recent_events(20)

total_events = len(events)

high_severity_events = 0

for event in events:

    if event[5] in [
        "high",
        "very_high"
    ]:

        high_severity_events += 1

st.subheader(
    "Executive Overview"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Events",
        total_events
    )

with col2:

    st.metric(
        "High-Risk Events",
        high_severity_events
    )

with col3:

    st.metric(
        "Confirmed Events",
        3
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