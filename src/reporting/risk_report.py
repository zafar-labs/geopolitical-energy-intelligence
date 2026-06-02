import yaml
from src.storage.event_store import EventStore

def load_taxonomy():

    with open("config/event_taxonomy.yaml", "r") as file:

        taxonomy = yaml.safe_load(file)

    return taxonomy["events"]

def calculate_risk_level(score):

    if score >= 13:
        return "CRITICAL"

    elif score >= 9:
        return "HIGH"

    elif score >= 5:
        return "MEDIUM"

    else:
        return "LOW"
    
def calculate_composite_risk(
    highest_score,
    event_count,
    high_risk_domains
):

    composite_score = (
        highest_score
        + event_count
        + high_risk_domains
    )

    if composite_score >= 14:
        return "CRITICAL", composite_score

    elif composite_score >= 10:
        return "HIGH", composite_score

    elif composite_score >= 6:
        return "MEDIUM", composite_score

    else:
        return "LOW", composite_score

def generate_report():

    store = EventStore()

    taxonomy = load_taxonomy()

    events = store.fetch_high_relevance_events(5)

    impact_areas = set()

    domain_scores = {}

    high_risk_domains = 0

    strategic_dependencies = set()

    immediate_effects = set()

    delayed_effects = set()

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

        for ontology_event in taxonomy:
            if ontology_event["event_id"] == event_code:
                impact_domains = ontology_event.get("impact_domains", {})
                pakistan_exposure = ontology_event.get(
                    "pakistan_exposure",
                    {}
                )
                event_score = event[6]

                for item in pakistan_exposure.get(
                    "strategic_dependency",
                    []
                ):
                    strategic_dependencies.add(item)

                for item in pakistan_exposure.get(
                    "immediate_effects",
                    []
                ):
                    immediate_effects.add(item)

                for item in pakistan_exposure.get(
                    "delayed_effects",
                    []
                ):
                    delayed_effects.add(item)

                for domain_name in impact_domains.keys():
                    domain_scores[domain_name] = (
                        domain_scores.get(domain_name, 0)
                        + event_score
                    )
                for domain_impacts in impact_domains.values():
                    impact_areas.update(domain_impacts)
                break

                    # Overall risk based on highest event score

    if highest_score >= 7:
        risk_level = "CRITICAL"

    elif highest_score >= 5:
        risk_level = "HIGH"

    elif highest_score >= 3:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    # Composite risk calculation

    # Composite risk calculation

    high_risk_domains = 0

    for score in domain_scores.values():

        if score >= 9:

            high_risk_domains += 1

    event_count = len(events)

    composite_risk_level, composite_score = (
        calculate_composite_risk(
            highest_score,
            event_count,
            high_risk_domains
        )
    )

    print("Overall Risk Assessment:")
    print(f"{risk_level}\n")

    print("Composite Risk Assessment:")
    print(f"Risk Level: {composite_risk_level}")
    print(f"Composite Score: {composite_score}\n")

    print("=================================")
    print("DOMAIN RISK ASSESSMENT")
    print("=================================\n")

    
    
    for domain, score in sorted(
        domain_scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        domain_risk = calculate_risk_level(score)

        print(f"{domain}")
        print(f"Score: {score}")
        print(f"Risk Level: {domain_risk}\n")

    print("Potential Areas of Concern:")
    if impact_areas:
        for area in sorted(impact_areas):
            print(f"- {area}")
    else:
        print("- None detected")

    print("\n=================================")
    print("PAKISTAN EXPOSURE ASSESSMENT")
    print("=================================\n")

    print("Strategic Dependencies:")

    for item in sorted(strategic_dependencies):
        print(f"- {item}")

    print("\nImmediate Effects:")

    for item in sorted(immediate_effects):

        print(f"- {item}")

    print("\nDelayed Effects:")

    for item in sorted(delayed_effects):

        print(f"- {item}")

if __name__ == "__main__":
    generate_report()