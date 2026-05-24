import feedparser

from src.analysis.event_classifier import EventClassifier


class NewsIngestor:

    def __init__(self):

        self.feed_url = "https://www.aljazeera.com/xml/rss/all.xml"

        self.classifier = EventClassifier()

    def fetch_headlines(self):

        feed = feedparser.parse(self.feed_url)
        
        # print(feed.entries) # added for debugging to see the structure of feed.entries

        headlines = []

        for entry in feed.entries[:10]:

            headlines.append(entry.title)

        return headlines

    def process_headlines(self):

        headlines = self.fetch_headlines()

        classified_events = []

        for headline in headlines:

            print(f"\nChecking headline: {headline}") # added for debugging to see which headline is being processed

            result = self.classifier.classify_event(headline)

            if result["matched_event"]:

                classified_events.append({
                    "headline": headline,
                    "classification": result
                })

        return classified_events


if __name__ == "__main__":

    ingestor = NewsIngestor()

    events = ingestor.process_headlines()

    for event in events:

        print("\nHEADLINE:")
        print(event["headline"])

        print("\nCLASSIFICATION:")
        print(event["classification"])