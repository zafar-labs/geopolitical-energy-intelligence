import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import yaml

from src.storage.event_store import EventStore

SOURCE_RELIABILITY = {

    "BBC News": 5,

    "NYT > World News": 5,

    "Reuters World News": 5,

    "Associated Press": 5,

    "Simulated News Source": 1
}

EXPOSURE_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "very_high": 4
}


class IntelligenceEngine:

    def __init__(self):

        self.store = EventStore()

    def _load_taxonomy(self):

        """
        Load the geopolitical event ontology.
        """

        with open(
            "config/event_taxonomy.yaml",
            "r"
        ) as file:

            taxonomy = yaml.safe_load(file)

        return taxonomy["events"]

    def build_common_operational_picture(self):
        """
        Build the Common Operational Picture (COP)
        from all currently available intelligence.
        """
        from datetime import datetime

        cop = {
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "metrics": {},
            "risk": {},
            "confidence": {},
            "commodity_exposure": {},
            "pakistan_exposure": {},
            "risk_clusters": {},
            "forecast": {},
            "recent_events": [],
            "alerts": [],
            "metadata": {
                "version": "1.0",
                "generated_by": "IntelligenceEngine"
            }
        }

        cop["recent_events"] = self.get_recent_events()
        cop["metrics"] = self.get_executive_metrics()
        cop["confidence"] = self.get_confidence_summary()

        events = self.store.fetch_high_relevance_events(5)
        taxonomy = self._load_taxonomy()

        intelligence = self._process_events(
            events,
            taxonomy
        )
        
        # Populate exposure matrices and risk clusters from processed events
        cop["commodity_exposure"] = intelligence["commodity_exposure"]
        cop["pakistan_exposure"] = intelligence["pakistan_exposure"]
        cop["risk_clusters"] = intelligence["risk_clusters"]
        cop["forecast"] = intelligence["forecast"]
        cop["domain_scores"] = intelligence["domain_scores"]
        cop["domain_assessment"] = intelligence["domain_assessment"]
        cop["cascade_effects"] = intelligence["cascade_effects"]
        cop["escalation_indicators"] = intelligence["escalation_indicators"]
        cop["impact_areas"] = intelligence["impact_areas"]
        # cop["executive_assessment"] = self._build_executive_assessment(cop)

        # Safely compute highest event relevance score
        highest_score = max((event[6] for event in events), default=0) if events else 0

        if highest_score >= 7:
            overall_risk = "CRITICAL"
        elif highest_score >= 5:
            overall_risk = "HIGH"
        elif highest_score >= 3:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"

        # Dynamically calculate composite operational risk profiles
        event_count = len(events)
        high_risk_domains = intelligence["high_risk_domains_count"]
        composite_score = highest_score + event_count + high_risk_domains

        if composite_score >= 16:
            composite_risk = "CRITICAL"
        elif composite_score >= 12:
            composite_risk = "HIGH"
        elif composite_score >= 8:
            composite_risk = "MEDIUM"
        else:
            composite_risk = "LOW"

        cop["risk"] = {
            "overall_risk": overall_risk,
            "highest_event_score": highest_score,
            "assessed_events": event_count,
            "high_risk_domains": high_risk_domains,
            "composite_score": composite_score,
            "composite_risk": composite_risk
        }

        cop["analytical_judgment"] = (
            self._build_analytical_judgment(
                highest_score,
                event_count,
                high_risk_domains,
                composite_score,
                intelligence["commodity_exposure"]
            )
        )

        cop["executive_assessment"] = self._build_executive_assessment(cop)
        
        return cop


    def get_recent_events(self, limit=20):

        """
        Return recent intelligence events in a
        presentation-friendly format.
        """

        events = self.store.fetch_recent_events(limit)

        formatted_events = []

        for event in events:

            formatted_events.append({

                "headline": event[1],

                "source": event[2],

                "event_id": event[3],

                "category": event[4],

                "severity": event[5],

                "relevance": event[6],

                "keywords": event[7],

                "created_at": event[8]

            })

        return formatted_events


    def get_high_risk_events(self, min_score=5):

        """
        Return strategically significant events.
        """

        return self.store.fetch_high_relevance_events(
            min_score
        )
    
    def get_executive_metrics(self):

        """
        Build the high-level dashboard metrics.
        """

        events = self.store.fetch_recent_events(20)

        total_events = len(events)

        high_risk_events = 0

        confirmed_events = set()

        for event in events:

            if event[5] in ["high", "very_high"]:

                high_risk_events += 1

            confirmed_events.add(
                event[3]
            )

        return {

            "total_events": total_events,

            "high_risk_events": high_risk_events,

            "confirmed_events": len(
                confirmed_events
            )
        }
    def get_confidence_summary(self):

        events = self.store.fetch_recent_events(20)

        event_confirmations = {}

        event_relevance_scores = {}

        for event in events:

            event_code = event[3]

            source = event[2]

            relevance = event[6]

            if event_code not in event_confirmations:

                event_confirmations[event_code] = set()

            event_confirmations[event_code].add(source)

            if event_code not in event_relevance_scores:

                event_relevance_scores[event_code] = relevance

            else:

                event_relevance_scores[event_code] = max(
                    event_relevance_scores[event_code],
                    relevance
                )

        summary = {}

        for event_code, sources in event_confirmations.items():

            confirmation_count = len(sources)

            reliability_score = 0

            for source in sources:

                reliability_score += (
                    SOURCE_RELIABILITY.get(
                        source,
                        1
                    )
                )

            relevance_score = event_relevance_scores[
                event_code
            ]

            composite_score = (
                confirmation_count
                +
                reliability_score
                +
                relevance_score
            )

            if composite_score >= 18:

                confidence = "VERY HIGH"

            elif composite_score >= 12:

                confidence = "HIGH"

            elif composite_score >= 8:

                confidence = "MEDIUM"

            else:

                confidence = "LOW"

            summary[event_code] = {

                "sources": list(sources),

                "confirmation_count":
                    confirmation_count,

                "reliability_score":
                    reliability_score,

                "relevance_score":
                    relevance_score,

                "composite_score":
                    composite_score,

                "confidence":
                    confidence
            }

        return summary

    def get_risk_summary(self):

        """
        Build the national risk assessment summary.
        """
        return {}
    
    def _calculate_risk_level(self, score):
        """
        Convert a numerical score into a standardized
        operational risk level.
        """

        if score >= 13:
            return "CRITICAL"

        elif score >= 9:
            return "HIGH"

        elif score >= 5:
            return "MEDIUM"

        return "LOW"
    
    def _process_events(self, events, taxonomy):
        """
        Process detected events against the ontology and
        generate intelligence products.
        """
        domain_scores = {}
        commodity_exposures = {}
        risk_clusters = {}
        forecast_scenarios = {}

        strategic_dependencies = set()
        immediate_effects = set()
        delayed_effects = set()
        impact_areas = set()
        first_order_effects = set()
        second_order_effects = set()
        third_order_effects = set()
        high_confidence_indicators = set()
        medium_confidence_indicators = set()
        monitoring_indicators = set()

        for event in events:
            event_code = event[3]
            for ontology_event in taxonomy:
                if ontology_event["event_id"] == event_code:
                    event_score = event[6]
                    event_name = ontology_event.get("trigger_event", {}).get("name", "Unknown Event")

                    impact_domains = ontology_event.get("impact_domains", {})
                    cascade_effects = ontology_event.get("cascade_effects", {})
                    escalation_indicators = ontology_event.get("escalation_indicators", {})
                    crisis_cluster = ontology_event.get("crisis_cluster", {})

                    forecast_data = ontology_event.get(
                        "forecast_scenarios",
                        {}
                    )

                    event_impact_areas = ontology_event.get(
                        "impact_areas",
                        []
                    )

                    confidence_data = ontology_event.get(
                        "scenario_confidence",
                        {}
                    )

                    self._update_domain_intelligence(
                        impact_domains,
                        cascade_effects,
                        escalation_indicators,        
                        event_score,
                        domain_scores,
                        first_order_effects,
                        second_order_effects,
                        third_order_effects,
                        high_confidence_indicators,
                        medium_confidence_indicators,
                        monitoring_indicators
                    )

                    # Populates the clusters using your new helper method
                    self._update_risk_intelligence(
                        crisis_cluster,
                        event_name,
                        event_score,
                        risk_clusters
                    )

                    self._update_scenario_intelligence(
                        event_code,
                        event_name,
                        forecast_data,
                        confidence_data,
                        forecast_scenarios
                    )

                    pakistan_exposure = ontology_event.get("pakistan_exposure", {})
                    self._update_pakistan_exposure(
                        pakistan_exposure,
                        strategic_dependencies,
                        immediate_effects,
                        delayed_effects
                    )

                    commodity_exposure = ontology_event.get("commodity_exposure", {})  
                    self._update_commodity_exposure(
                        commodity_exposure,
                        commodity_exposures
                    )  

                    impact_areas.update(event_impact_areas)            
                                                                                                        
                    break

        # Calculate high risk domains for the composite score calculation
        high_risk_domains_count = sum(1 for score in domain_scores.values() if score >= 9)

        domain_assessment = {}

        for domain_name, score in domain_scores.items():

            domain_assessment[domain_name] = {

                "score": score,

                "risk_level": self._calculate_risk_level(score)

            }

        return {
            "commodity_exposure": commodity_exposures,
            "forecast": forecast_scenarios,
            "risk_clusters": risk_clusters,
            "high_risk_domains_count": high_risk_domains_count,
            "domain_scores": domain_scores,
            "domain_assessment": domain_assessment,

            "cascade_effects": {
                "first_order":sorted(first_order_effects),
                "second_order":sorted(second_order_effects),
                "third_order":sorted(third_order_effects)
            },

            "escalation_indicators": {
                "high_confidence": sorted(high_confidence_indicators),
                "medium_confidence": sorted(medium_confidence_indicators),
                "monitoring": sorted(monitoring_indicators)
            },

            "pakistan_exposure": {
                "strategic_dependencies": sorted(strategic_dependencies),
                "immediate_effects": sorted(immediate_effects),
                "delayed_effects": sorted(delayed_effects)
            },
            "impact_areas": sorted(impact_areas)  # Extracted area list
        }
    
    def _update_commodity_exposure(
        self,
        commodity_exposure,
        commodity_exposures
    ):

        """
        Update the national commodity exposure profile
        using a single ontology event.
        """

        for commodity, details in commodity_exposure.items():

            exposure_level = details.get(
                "exposure_level",
                "unknown"
            )

            current_level = commodity_exposures.get(
                commodity
            )

            if current_level is None:

                commodity_exposures[
                    commodity
                ] = exposure_level

            else:

                if (
                    EXPOSURE_RANK.get(
                        exposure_level,
                        0
                    )
                    >
                    EXPOSURE_RANK.get(
                        current_level,
                        0
                    )
                ):

                    commodity_exposures[
                        commodity
                    ] = exposure_level


    def _update_pakistan_exposure(
        self,
        pakistan_exposure,
        strategic_dependencies,
        immediate_effects,
        delayed_effects
    ):

        """
        Update Pakistan-specific exposure assessment
        using a single ontology event.
        """

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
    def _update_domain_intelligence(
        self,
        impact_domains,
        cascade_effects,
        escalation_indicators,
        event_score,
        domain_scores,
        first_order_effects,
        second_order_effects,
        third_order_effects,
        high_confidence_indicators,
        medium_confidence_indicators,
        monitoring_indicators
    ):

        """
        Update domain-level intelligence derived from
        a single ontology event.
        """

        for domain_name in impact_domains.keys():

            domain_scores[domain_name] = (
                domain_scores.get(
                    domain_name,
                    0
                )
                +
                event_score
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

    def _update_risk_intelligence(self, crisis_cluster, event_name, event_score, risk_clusters):
        """
        Group events into correlated threat/crisis clusters and aggregate scores.
        """
        cluster_name = crisis_cluster.get("cluster_name")
        if cluster_name:
            if cluster_name not in risk_clusters:
                risk_clusters[cluster_name] = {
                    "events": [],
                    "score": 0,
                    "risk_level": "LOW"
                }
            
            if event_name not in risk_clusters[cluster_name]["events"]:
                risk_clusters[cluster_name]["events"].append(event_name)
                
            risk_clusters[cluster_name]["score"] += event_score
            
            risk_clusters[cluster_name]["risk_level"] = (
                self._calculate_risk_level(
                    risk_clusters[cluster_name]["score"]
                )
            )

    def _update_scenario_intelligence(
        self,
        event_id,
        event_name,
        forecast_data,
        confidence_data,
        forecast_scenarios
    ):
        """
        Store scenario forecasts associated with a
        strategic event.
        """

        if event_id not in forecast_scenarios:

            forecast_scenarios[event_id] = {

                "event_name": event_name,

                "most_likely": forecast_data.get(
                    "most_likely",
                    {}
                ).get(
                    "description",
                    "Not Available"
                ),

                "severe_case": forecast_data.get(
                    "severe_case",
                    {}
                ).get(
                    "description",
                    "Not Available"
                ),

                "best_case": forecast_data.get(
                    "best_case",
                    {}
                ).get(
                    "description",
                    "Not Available"
                ),

                "confidence": confidence_data

            }

    def _build_analytical_judgment(
        self,
        highest_score,
        event_count,
        high_risk_domains,
        composite_score,
        commodity_exposure
    ):
        """
        Build analyst-readable justification for the
        overall strategic assessment.
        """

        judgment = []

        if highest_score >= 5:
            judgment.append(
                "Multiple high-relevance geopolitical events are currently active."
            )

        if high_risk_domains >= 3:
            judgment.append(
                f"{high_risk_domains} strategic domains are assessed at elevated risk."
            )

        if any(
            level.lower() in ("high", "very_high")
            for level in commodity_exposure.values()
        ):
            judgment.append(
                "Critical energy commodities remain exposed to regional disruption."
            )

        if composite_score >= 12:
            judgment.append(
                "Composite operational indicators support a HIGH strategic risk assessment."
            )

        return judgment

    def _build_executive_assessment(self, cop):
        primary_drivers = list(cop["risk_clusters"].keys())      
        highest_exposures = []

        for commodity, exposure in cop["commodity_exposure"].items():

            if exposure.lower() in ("high", "very_high"):

                if commodity == "lng":
                    display_name = "LNG"
                else:
                    display_name = commodity.replace("_", " ").title()

                highest_exposures.append((display_name, exposure))

        priority = {
            "very_high": 0,
            "high": 1
        }

        highest_exposures.sort(
            key=lambda item: priority[item[1]]
        )

        highest_exposures = [
            name for name, _ in highest_exposures
        ]

        priority_monitoring = cop["escalation_indicators"]["high_confidence"][:5]
        
        return {
            "risk_statement": (
                f"Current strategic energy risk is "
                f"{cop['risk']['overall_risk']}."
            ),
            "primary_drivers": primary_drivers,
            "highest_exposures": highest_exposures,
            "priority_monitoring": priority_monitoring,
        }
# if __name__ == "__main__":

#     engine = IntelligenceEngine()

#     print(
#         engine.get_risk_summary()
#     )
if __name__ == "__main__":
    engine = IntelligenceEngine()

    # cop = engine.build_common_operational_picture()
    # print(cop)
    cop = engine.build_common_operational_picture()

    print(cop["risk"])
    print(cop["commodity_exposure"])
    print(cop["pakistan_exposure"])
    print(cop["forecast"])
    print(cop["domain_scores"])
    print(cop["domain_assessment"])
    print(cop["cascade_effects"])
    print(cop["escalation_indicators"])
    print(cop["impact_areas"])