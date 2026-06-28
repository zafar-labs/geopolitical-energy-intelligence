from src.storage.event_store import EventStore

SOURCE_RELIABILITY = {

    "BBC News": 5,

    "NYT > World News": 5,

    "Reuters World News": 5,

    "Associated Press": 5,

    "Simulated News Source": 1
}


class IntelligenceEngine:

    def __init__(self):

        self.store = EventStore()


    def get_recent_events(self, limit=20):

        """
        Return recent intelligence events for any
        presentation layer (dashboard, reports, API).
        """

        return self.store.fetch_recent_events(limit)


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
    
if __name__ == "__main__":
    engine = IntelligenceEngine()
    confidence = engine.get_confidence_summary()
    print(confidence)