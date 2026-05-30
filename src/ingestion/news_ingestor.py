import feedparser

from src.analysis.event_classifier import EventClassifier
from src.storage.event_store import EventStore



class NewsIngestor:

    def __init__(self):

        self.feed_url = "https://www.aljazeera.com/xml/rss/all.xml"

        self.classifier = EventClassifier()

        self.store = EventStore()

    def fetch_headlines(self): # Simulated headline fetching for testing purposes

        simulated_headlines = [

            "Iran threatens closure of Strait of Hormuz",

            "War-risk insurance premiums surge in Gulf shipping routes",

            "Qatar LNG exports disrupted after terminal strike",

            "Oil tanker delays reported near Gulf transit corridor"
        ]

        return simulated_headlines

   # def fetch_headlines(self): # Actual headline fetching from RSS feed
     #   feed = feedparser.parse(self.feed_url)
        
        # print(feed.entries) # added for debugging to see the structure of feed.entries

     #   headlines = []

    #    for entry in feed.entries[:10]:

      #      headlines.append(entry.title)

     #   return headlines

    def process_headlines(self):

        headlines = self.fetch_headlines()

        classified_events = []

        for headline in headlines:

            print(f"\nChecking headline: {headline}")

            result = self.classifier.classify_event(headline)

            if result:

                print(f"Relevance Score: {result['relevance_score']}")

                print(f"Matched Keywords: {result['matched_keywords']}")

                if result["relevance_score"] >= 3:

                    if not self.store.event_exists(headline):

                        self.store.save_event(headline, result)

                        classified_events.append({
                            "headline": headline,
                            "classification": result
                        })

                    else:

                        print("Duplicate event skipped.")

                else:

                    print("Event rejected due to low relevance.")

            else:

                print("No classification result for headline.")

        return classified_events


if __name__ == "__main__":

    ingestor = NewsIngestor()

    events = ingestor.process_headlines()

    for event in events:

        print("\nHEADLINE:")
        print(event["headline"])

        print("\nCLASSIFICATION:")
        print(event["classification"])