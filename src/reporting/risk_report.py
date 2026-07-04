import sys
from pathlib import Path

# Handle repository pathing
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.analysis.intelligence_engine import IntelligenceEngine

def generate_report():
    # Instantiate engine and consume unified COP payload
    engine = IntelligenceEngine()
    cop = engine.build_common_operational_picture()
    
    # Unpack the calculated products from the client data layer
    risk_summary = cop["risk"]
    executive = cop["executive_assessment"]
    metrics = cop["metrics"]
    events = cop["recent_events"]
    risk_clusters = cop["risk_clusters"]
    domain_assessment = cop["domain_assessment"]
    commodity_exposures = cop["commodity_exposure"]
    pakistan_exposure = cop["pakistan_exposure"]
    cascade_effects = cop["cascade_effects"]
    escalation_indicators = cop["escalation_indicators"]
    forecast = cop["forecast"]
    confidence_summary = cop["confidence"]

    print("\n=================================")
    print("PAKISTAN ENERGY RISK SUMMARY")
    print("=================================\n")

    print("EXECUTIVE SUMMARY")
    print("---------------------------------")
    print(f"Overall Risk      : {risk_summary['overall_risk']}")
    print(f"Composite Risk    : {risk_summary['composite_risk']}")
    print(f"Composite Score   : {risk_summary['composite_score']}")
    print()
    print(f"Events Assessed   : {risk_summary['assessed_events']}")
    print(f"Total Events      : {metrics['total_events']}")
    print(f"High Risk Events  : {metrics['high_risk_events']}")
    print(f"Confirmed Events  : {metrics['confirmed_events']}")
    print(f"High Risk Domains : {risk_summary['high_risk_domains']}")
    print("\n=================================\n")

    if not events:
        print("No High-Priority Events.")
        return

    print("=================================")
    print("HIGH-PRIORITY EVENTS")
    print("=================================\n")

    high_priority_events = [
        event for event in events
        if event["relevance"] >= 5
    ]

    for idx, event in enumerate(high_priority_events, start=1):
        print(f"{idx}. {event['headline']}")
        print(f"   Severity: {event['severity'].upper()}")
        print(f"   Source: {event['source']}\n")

    print("Overall Risk Assessment:")
    print(f"{risk_summary['overall_risk']}\n")

    print("Composite Risk Assessment:")
    print(f"Risk Level: {risk_summary['composite_risk']}")
    print(f"Composite Score: {risk_summary['composite_score']}\n")

    print("=================================")
    print("CORRELATED RISK CLUSTERS")
    print("=================================\n")
    for cluster_name, cluster_data in risk_clusters.items():
        print(f"Cluster: {cluster_name}")
        print(f"Combined Score: {cluster_data['score']}")
        print(f"Risk Level: {cluster_data['risk_level']}")

        print("Events:")
        for event_name in cluster_data["events"]:
            print(f"- {event_name}")
        print()

    print("=================================")
    print("DOMAIN RISK ASSESSMENT")
    print("=================================\n")

    for domain, details in sorted(
        domain_assessment.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    ):

        print(domain)
        print(f"Score: {details['score']}")
        print(f"Risk Level: {details['risk_level']}\n")

    print("=================================")
    print("COMMODITY EXPOSURE ASSESSMENT")
    print("=================================\n")
    for commodity, exposure in sorted(commodity_exposures.items()):
        print(f"{commodity}: {exposure.upper()}")
    print()
    
    print("Potential Areas of Concern:")
    if cop["impact_areas"]:
        for area in cop["impact_areas"]:
            print(f"- {area}")
    else:
        print("- None detected")
    
    print("=================================")
    print("PAKISTAN EXPOSURE ASSESSMENT")
    print("=================================\n")
    print("Strategic Dependencies:")
    for item in pakistan_exposure["strategic_dependencies"]:
        print(f"- {item}")
    print("\nImmediate Effects:")
    for item in pakistan_exposure["immediate_effects"]:
        print(f"- {item}")
    print("\nDelayed Effects:")
    for item in pakistan_exposure["delayed_effects"]:
        print(f"- {item}")
    print("=================================\n")

    print("CASCADING RISK ASSESSMENT")
    print("=================================\n")
    print("First-Order Effects:")
    for item in cascade_effects["first_order"]:
        print(f"- {item}")
    print("\nSecond-Order Effects:")
    for item in cascade_effects["second_order"]:
        print(f"- {item}")
    print("\nThird-Order Effects:")  
    for item in cascade_effects["third_order"]:
        print(f"- {item}")
    print("=================================\n")

    print("=================================")
    print("ESCALATION MONITORING")
    print("=================================\n")
    print("High-Confidence Indicators:")
    for item in escalation_indicators["high_confidence"]:
        print(f"- {item}")
    print("\nMedium-Confidence Indicators:")
    for item in escalation_indicators["medium_confidence"]:
        print(f"- {item}")
    print("\nMonitoring Indicators:")
    for item in escalation_indicators["monitoring"]:
        print(f"- {item}")
    print("=================================\n")

    print("=================================")
    print("FORECAST ASSESSMENT")
    print("=================================\n")
    for event_id, scenario in forecast.items():
        # Read pre-calculated metrics to display dynamically
        print(f"Event: {scenario['event_name']}\n")
        print(f"Most Likely Scenario:")
        print(f"- {scenario['most_likely']}\n")
        print(f"Severe Scenario:")
        print(f"- {scenario['severe_case']}\n")
        print(f"Best Case Scenario:")
        print(f"- {scenario['best_case']}\n")
        print("---------------------------------\n")

    print("\n=================================")
    print("SOURCE CONFIRMATION ANALYSIS")
    print("=================================\n")
    for event_code, details in confidence_summary.items():
        print(f"{event_code}")
        print("Sources:")
        for source in details["sources"]:
            print(f"- {source}")
        print(f"Confirmation Count: {details['confirmation_count']}")
        print(f"Reliability Score: {details['reliability_score']}")
        print(f"Relevance Score: {details['relevance_score']}")
        print(f"Composite Score: {details['composite_score']}")
        print(f"Confidence Level: {details['confidence']}\n")

    print("=================================")
    print("EXECUTIVE ANALYST ASSESSMENT")
    print("=================================\n")

    print(executive["risk_statement"])
    print()

    print("Primary Drivers:")
    for driver in executive["primary_drivers"]:
        print(f"- {driver}")

    print("\nHighest Exposures:")
    for exposure in executive["highest_exposures"]:
        print(f"- {exposure}")

    print("\nPriority Monitoring:")
    for item in executive["priority_monitoring"]:
        print(f"- {item}")

    print()

if __name__ == "__main__":
    generate_report()