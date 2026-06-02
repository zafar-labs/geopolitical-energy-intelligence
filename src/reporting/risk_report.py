from src.storage.event_store import EventStore

def generate_report():

    store = EventStore()

    events = store.fetch_high_relevance_events(5)

    impact_areas = set()

    if events:
        # compute highest score from events (index 6 expected to be score)
        try:
            highest_score = max(event[6] for event in events)
        except Exception:
            highest_score = 0
    else:
        highest_score = 0

    print("\n=================================")
    print("PAKISTAN ENERGY RISK SUMMARY")
    print("=================================\n")

    if not events:
        print("No high-priority events detected.")
        return

    print("High-Priority Events Detected:\n")

    for idx, event in enumerate(events, start=1):
        print(f"{idx}. {event[1]}")
        print(f"   Severity: {event[5]}")
        print(f"   Source: {event[2]}\n")
        event_code = event[3]

        if event_code == "HORMUZ_TRANSIT_001":
            impact_areas.update([
                "Fuel Imports",
                "Freight Costs",
                "Inflationary Pressure",
                "Foreign Exchange Pressure"
            ])

        elif event_code == "QATAR_LNG_001":
            impact_areas.update([
                "LNG Supply",
                "Power Generation",
                "Industrial Gas Supply",
                "Load Shedding Risk"
            ])

    if highest_score >= 7:
        risk_level = "CRITICAL"
    elif highest_score >= 5:
        risk_level = "HIGH"
    elif highest_score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    print("Overall Risk Assessment:")
    print(f"{risk_level}\n")

    print("Potential Areas of Concern:")
    if impact_areas:
        for area in sorted(impact_areas):
            print(f"- {area}")
    else:
        print("- None detected")

if __name__ == "__main__":
    generate_report()