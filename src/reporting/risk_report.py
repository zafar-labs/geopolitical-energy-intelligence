import yaml
from src.storage.event_store import EventStore

EXPOSURE_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "very_high": 4
}

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

    risk_clusters = {}

    commodity_exposures = {}

    high_risk_domains = 0

    strategic_dependencies = set()

    immediate_effects = set()

    delayed_effects = set()

    first_order_effects = set()

    second_order_effects = set()

    third_order_effects = set()

    high_confidence_indicators = set()

    medium_confidence_indicators = set()

    monitoring_indicators = set()

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
                crisis_cluster = ontology_event.get("crisis_cluster",{} )# Not used in current report but can be included in future iterations
                pakistan_exposure = ontology_event.get(
                    "pakistan_exposure",
                    {}
                )

                cascade_effects = ontology_event.get(
                    "cascade_effects",
                    {}
                )

                escalation_indicators = ontology_event.get(
                    "escalation_indicators",
                    {}
                )

                commodity_exposure = ontology_event.get(
                    "commodity_exposure",
                    {}
                )

                for item in cascade_effects.get(
                    "first_order",
                    []
                ):
                    first_order_effects.add(item)

                for item in cascade_effects.get(
                    "second_order",
                    []
                ):
                    second_order_effects.add(item)

                for item in cascade_effects.get(
                    "third_order",
                    []
                ):
                    third_order_effects.add(item)

                event_score = event[6]

                for item in escalation_indicators.get(
                    "high_confidence",
                    []
                ):
                    high_confidence_indicators.add(item)

                for item in escalation_indicators.get(
                    "medium_confidence",
                    []
                ):
                    medium_confidence_indicators.add(item)

                for item in escalation_indicators.get(
                    "monitoring",
                    []
                ):
                    monitoring_indicators.add(item)

                for commodity, details in commodity_exposure.items():
                    exposure_level = details.get(
                        "exposure_level",
                        "unknown"
                    )
                    current_level = commodity_exposures.get(
                        commodity
                    )

                    if current_level is None:
                        commodity_exposures[commodity] = exposure_level
                    else:
                        if (
                            EXPOSURE_RANK.get(exposure_level, 0)
                            >
                            EXPOSURE_RANK.get(current_level, 0)
                        ):
                            commodity_exposures[commodity] = exposure_level

                cluster_name = crisis_cluster.get(
                    "cluster_name"
                )

                if cluster_name:

                    if cluster_name not in risk_clusters:

                        risk_clusters[cluster_name] = {
                            "events": [],
                            "score": 0
                        }

                    risk_clusters[cluster_name]["events"].append(
                        ontology_event["trigger_event"]["name"]
                    )

                    risk_clusters[cluster_name]["score"] += event_score

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
    print("CORRELATED RISK CLUSTERS")
    print("=================================\n")

    for cluster_name, cluster_data in risk_clusters.items():

        cluster_risk = calculate_risk_level(
            cluster_data["score"]
        )

        print(f"Cluster: {cluster_name}")

        print(
            f"Combined Score: "
            f"{cluster_data['score']}"
        )

        print(
            f"Risk Level: "
            f"{cluster_risk}"
        )

        print("Events:")

        for event_name in cluster_data["events"]:

            print(f"- {event_name}")

        print()

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

    print("=================================")
    print("COMMODITY EXPOSURE ASSESSMENT")
    print("=================================\n")

    for commodity, exposure in sorted(
        commodity_exposures.items()
    ):

        print(
            f"{commodity}: "
            f"{exposure.upper()}"
        )

    print()
    
    print("Potential Areas of Concern:")
    if impact_areas:
        for area in sorted(impact_areas):
            print(f"- {area}")
    else:
        print("- None detected")

    print("\n=================================")
    print("PAKISTAN EXPOSURE ASSESSMENT")
    print("\n=================================")
    
    print("Strategic Dependencies:")

    for item in sorted(strategic_dependencies):
        print(f"- {item}")

    print("\nImmediate Effects:")

    for item in sorted(immediate_effects):

        print(f"- {item}")

    print("\nDelayed Effects:")

    for item in sorted(delayed_effects):

        print(f"- {item}")
    print("=================================\n")

    print("CASCADING RISK ASSESSMENT")
    print("=================================\n")

    print("First-Order Effects:")

    for item in sorted(first_order_effects):
        print(f"- {item}")

    print("\nSecond-Order Effects:")

    for item in sorted(second_order_effects):
        print(f"- {item}")

    print("\nThird-Order Effects:")  
    for item in sorted(third_order_effects):
        print(f"- {item}")
    print("=================================\n")

    print("=================================")
    print("ESCALATION MONITORING")
    print("=================================\n")

    print("High-Confidence Indicators:")

    for item in sorted(
        high_confidence_indicators
    ):
        print(f"- {item}")

    print("\nMedium-Confidence Indicators:")

    for item in sorted(
        medium_confidence_indicators
    ):
        print(f"- {item}")

    print("\nMonitoring Indicators:")

    for item in sorted(
        monitoring_indicators
    ):
        print(f"- {item}")

    print("=================================\n")

    


if __name__ == "__main__":
    generate_report()