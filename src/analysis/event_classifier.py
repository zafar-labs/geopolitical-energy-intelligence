import yaml


class EventClassifier:

    def __init__(self, taxonomy_path="config/event_taxonomy.yaml"):

        with open(taxonomy_path, "r") as file:
            self.taxonomy = yaml.safe_load(file)

    def classify_event(self, headline):

        headline_lower = headline.lower()

        for event in self.taxonomy["events"]:

            keywords = event.get("detection_keywords", [])

            for keyword in keywords:

                if keyword.lower() in headline_lower:

                    return {
                        "matched_event": event["event_id"],
                        "event_category": event["event_category"],
                        "severity": event["severity"],
                        "trigger_event": event["trigger_event"]["name"]
                    }

        return {
            "matched_event": None,
            "event_category": None,
            "severity": None,
            "trigger_event": None
        }


if __name__ == "__main__":

    classifier = EventClassifier()

    sample_headline = "Iran threatens closure of Strait of Hormuz"

    result = classifier.classify_event(sample_headline)

    print(result)