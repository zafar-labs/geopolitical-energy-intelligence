import yaml


class EventClassifier:

    def __init__(self, taxonomy_path="config/event_taxonomy.yaml"):

        with open(taxonomy_path, "r") as file:
            self.taxonomy = yaml.safe_load(file)

    def classify_event(self, headline):

        headline_lower = headline.lower()

        best_match = None

        highest_score = 0

        matched_keywords = []

        keyword_weights = {
            "high_confidence": 5,
            "medium_confidence": 3,
            "contextual": 1
        }

        MINIMUM_RELEVANCE_SCORE = 5

        for event in self.taxonomy["events"]:

            score = 0

            current_matches = []

            detection_keywords = event.get("detection_keywords", {})

            for category, keywords in detection_keywords.items():

                weight = keyword_weights.get(category, 0)

                for keyword in keywords:

                    if keyword.lower() in headline_lower:

                        score += weight

                        current_matches.append(keyword)

            if score > highest_score:

                highest_score = score

                matched_keywords = current_matches

                best_match = {
                    "matched_event": event["event_id"],
                    "event_category": event["event_category"],
                    "severity": event["severity"],
                    "trigger_event": event["trigger_event"]["name"],
                    "relevance_score": score,
                    "matched_keywords": matched_keywords,
                    "impact_domains": event.get("impact_domains", {})
                }

        if highest_score >= MINIMUM_RELEVANCE_SCORE:

            return best_match
        if highest_score > 0:

            print(
                f"\nNEAR MISS:"
            )

            print(
                f"Score: {highest_score}"
            )

            print(
                f"Headline: {headline}"
            )

            print(
                f"Keywords: {matched_keywords}"
            )

        return None


if __name__ == "__main__":

    classifier = EventClassifier()

    sample_headline = "Iran threatens closure of Strait of Hormuz"

    result = classifier.classify_event(sample_headline)

    print(result)