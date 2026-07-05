import sys
from pathlib import Path
import textwrap

# Handle repository pathing
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.analysis.intelligence_engine import IntelligenceEngine

def format_label(text):
    """
    Convert snake_case identifiers into human-readable labels 
    while protecting technical and organizational acronyms.
    """
    text_str = str(text).strip()
    
    # Direct dictionary mapping for precise presentation strings
    exact_mappings = {
        "lng": "LNG",
        "bbc news": "BBC News",
        "nyt > world news": "NYT > World News",
        "simulated news source": "Simulated News Source",
        "fx": "FX",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "critical": "Critical",
        "very_high": "Very High",
        "very high": "Very High"
    }
    
    if text_str.lower() in exact_mappings:
        return exact_mappings[text_str.lower()]
    
    # Fallback to standard conversion while patching common sub-strings
    formatted = text_str.replace("_", " ").title()
    formatted = formatted.replace("Lng", "LNG").replace("Bbc", "BBC").replace("Nyt", "NYT")
    return formatted


def print_section_header(title):
    """Prints a single clean section boundary block."""
    print("================================================================")
    print(f" {title}")
    print("================================================================\n")


def print_executive_summary(risk_summary, metrics):
    print_section_header("EXECUTIVE SUMMARY")
    print(f"  Overall System Risk   : {format_label(risk_summary['overall_risk'])}")
    print(f"  Composite Risk Level  : {format_label(risk_summary['composite_risk'])}")
    print(f"  Composite Risk Score  : {risk_summary['composite_score']}")
    print()
    print(f"  High-Priority Signals : {risk_summary['assessed_events']} assessed")
    print(f"  Total Events Observed : {metrics['total_events']}")
    print(f"  High-Risk Count       : {metrics['high_risk_events']}")
    print(f"  Confirmed Indicators  : {metrics['confirmed_events']}")
    print(f"  High-Risk Domains     : {risk_summary['high_risk_domains']}")
    print()


def print_high_priority_events(events, risk_summary):
    print_section_header("HIGH-PRIORITY EVENTS")

    high_priority_events = [e for e in events if e["relevance"] >= 5]

    for idx, event in enumerate(high_priority_events, start=1):
        print(f"  {idx}. {event['headline']}")
        print(f"     Severity: {format_label(event['severity'])}")
        print(f"     Source:   {format_label(event['source'])}\n")

    # print(f"  Overall Assessment Score : {risk_summary['highest_event_score']}")
    print(f"  Calculated Operational Risk: {format_label(risk_summary['overall_risk'])}")
    print()


def print_risk_clusters(risk_clusters):
    print_section_header("CORRELATED RISK CLUSTERS")

    if not risk_clusters:
        print("  [-] No clustered strategic threats identified.\n")
        return

    for cluster_name, cluster_data in risk_clusters.items():
        print(f"  Cluster Name:   {cluster_name}")
        print(f"  Combined Score: {cluster_data['score']}")
        print(f"  Risk Evaluation: {format_label(cluster_data.get('risk_level', 'HIGH'))}")
        print("  Implicated Line Events:")
        for event_name in cluster_data["events"]:
            print(f"    - {event_name}")
        print()


def print_domain_assessment(domain_assessment):
    print_section_header("DOMAIN RISK ASSESSMENT")

    for domain, details in sorted(
        domain_assessment.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    ):
        print(f"  {format_label(domain)}")
        print(f"    Score:      {details['score']}")
        print(f"    Risk Level: {format_label(details['risk_level'])}\n")


def print_commodity_exposure(commodity_exposures, impact_areas):
    print_section_header("COMMODITY EXPOSURE ASSESSMENT")

    for commodity, exposure in sorted(commodity_exposures.items()):
        print(f"  {format_label(commodity).ljust(20)}: {format_label(exposure)}")

    print("\n  Potential Impact Areas:")
    if impact_areas:
        for area in sorted(impact_areas):
            print(f"    - {area}")
    else:
        print("    - None detected")
    print()


def print_pakistan_exposure(pakistan_exposure):
    print_section_header("PAKISTAN EXPOSURE ASSESSMENT")

    print("  Strategic Structural Dependencies:")
    for item in pakistan_exposure["strategic_dependencies"]:
        print(f"    - {item}")

    print("\n  Immediate Operational Effects:")
    for item in pakistan_exposure["immediate_effects"]:
        print(f"    - {item}")

    print("\n  Delayed Macroeconomic Risks:")
    for item in pakistan_exposure["delayed_effects"]:
        print(f"    - {item}")
    print()


def print_cascade_assessment(cascade_effects):
    print_section_header("CASCADING RISK ASSESSMENT")

    print("  First-Order Effects (Immediate):")
    for item in cascade_effects["first_order"]:
        print(f"    - {item}")

    print("\n  Second-Order Effects (Delayed):")
    for item in cascade_effects["second_order"]:
        print(f"    - {item}")

    print("\n  Third-Order Effects (Systemic):")
    for item in cascade_effects["third_order"]:
        print(f"    - {item}")
    print()


def print_escalation_monitoring(escalation_indicators):
    print_section_header("ESCALATION MONITORING MATRIX")

    print("  High-Confidence Operational Triggers:")
    for item in escalation_indicators["high_confidence"]:
        print(f"    - {item}")

    print("\n  Medium-Confidence Intelligence Indicators:")
    for item in escalation_indicators["medium_confidence"]:
        print(f"    - {item}")

    print("\n  Baseline System Monitoring Requirement:")
    for item in escalation_indicators["monitoring"]:
        print(f"    - {item}")
    print()


def print_forecast_assessment(forecast):
    print_section_header("FORWARD-LOOKING SCENARIO FORECASTS")

    for _, scenario in forecast.items():
        print(f"  Event Grouping: {scenario['event_name']}\n")
        print("    Most Likely Strategic Evolution:")
        print(f"    - {scenario['most_likely']}\n")
        print("    Severe Degraded Case Scenario:")
        print(f"    - {scenario['severe_case']}\n")
        print("    Best Case Resolution Scenario:")
        print(f"    - {scenario['best_case']}")
        print("  " + "-" * 58 + "\n")


def print_source_confirmation(confidence_summary):
    print_section_header("SOURCE CONFIRMATION ANALYSIS")
    
    for event_code, details in confidence_summary.items():
        print(f"  Signal Identifier: {event_code}")
        print("  Reporting Agencies:")
        for source in details["sources"]:
            print(f"    - {format_label(source)}")
        print(f"    Confirmation Footprint:  {details['confirmation_count']}")
        print(f"    Source Reliability Score: {details['reliability_score']}")
        print(f"    Relevance Input Score:   {details['relevance_score']}")
        print(f"    Calculated Data Weight:  {details['composite_score']}")
        print(f"    Resulting Confidence:    {format_label(details['confidence'])}\n")


def print_executive_assessment(executive):
    print_section_header("EXECUTIVE ANALYTIC ASSESSMENT")

    print("  BLUF (Bottom Line Up Front):")
    statement = executive.get("risk_statement", "No definitive risk statement available.")
    wrapped_statement = textwrap.fill(statement, width=64)
    print(textwrap.indent(wrapped_statement, "    | "))
    print()

    print("  KEY VULNERABILITY DRIVERS:")
    for driver in executive.get("primary_drivers", []):
        print(f"    [>] {driver}")

    print("\n  CRITICAL EXPOSURES:")
    for exposure in executive.get("highest_exposures", []):
        print(f"    [!] {exposure}")

    print("\n  PRIORITY INTELLIGENCE REQUIREMENTS (PIRs):")
    for item in executive.get("priority_monitoring", []):
        print(f"    [ʘ] {item}")
    print("\n================================================================\n")


def generate_report():
    engine = IntelligenceEngine()
    cop = engine.build_common_operational_picture()

    risk_summary = cop["risk"]
    # Provide safe fallback lookup if key structure is evolving
    executive = cop.get("executive_assessment", {
        "risk_statement": "Current strategic energy risk remains High.",
        "primary_drivers": ["Gulf Energy Supply Shock"],
        "highest_exposures": ["LNG", "Crude Oil", "Refined Fuels", "Power Generation", "Industrial Gas"],
        "priority_monitoring": ["LNG Cargo Cancellation", "Mine Deployment", "Naval Interdiction", "Tanker Attack", "Terminal Shutdown"]
    })
    metrics = cop["metrics"]
    events = cop["recent_events"]
    risk_clusters = cop["risk_clusters"]
    
    # Use matching key names dynamically extracted by engine processing
    domain_assessment = cop.get("domain_assessment", cop.get("domain_scores", {}))
    commodity_exposures = cop["commodity_exposure"]
    pakistan_exposure = cop["pakistan_exposure"]
    cascade_effects = cop["cascade_effects"]
    escalation_indicators = cop["escalation_indicators"]
    forecast = cop["forecast"]
    confidence_summary = cop["confidence"]
    impact_areas = cop["impact_areas"]

    # Balanced presentation sequencing
    print_executive_summary(risk_summary, metrics)
    print_high_priority_events(events, risk_summary)
    print_risk_clusters(risk_clusters)
    print_domain_assessment(domain_assessment)
    print_commodity_exposure(commodity_exposures, impact_areas)
    print_pakistan_exposure(pakistan_exposure)
    print_cascade_assessment(cascade_effects)
    print_escalation_monitoring(escalation_indicators)
    print_forecast_assessment(forecast)
    print_source_confirmation(confidence_summary)
    print_executive_assessment(executive)


if __name__ == "__main__":
    generate_report()