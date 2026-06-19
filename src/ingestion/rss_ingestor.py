import feedparser

from src.storage.event_store import EventStore

DEBUG_MODE = False

if DEBUG_MODE:

    print("\nTEXT BEING CLASSIFIED:")
    print(article_text)
    print("-" * 80)

near_misses = []

RSS_FEEDS = [

    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml"
]


def fetch_articles():

    articles = []

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        print("Feed URL:", feed_url)
        print("Feed Title:", feed.feed.get("title"))
        print("Entries:", len(feed.entries))
        print()

        for entry in feed.entries:

            article = {

                "title": entry.get(
                    "title",
                    ""
                ),

                "source": feed.feed.get(
                    "title",
                    "Unknown"
                ),

                "url": entry.get(
                    "link",
                    ""
                ),

                "published_at": entry.get(
                    "published",
                    ""
                ),

                "summary": entry.get(
                    "summary",
                    ""
                )
            }

            articles.append(article)

    return articles


if __name__ == "__main__":

    store = EventStore()

    from src.analysis.event_classifier import EventClassifier

    classifier = EventClassifier()

    articles = fetch_articles()

    saved_count = 0

    events_detected = 0

    for article in articles:

        if not store.article_exists(
            article["url"]
        ):

            store.save_article(
                article["title"],
                article["source"],
                article["url"],
                article["published_at"],
                article["summary"]
            )

            saved_count += 1

        article_text = (
            article["title"]
            + " "
            + article["summary"]
        )

        
        classification = (
            classifier.classify_event(
                article_text
            )
        )

        if classification:
            if not store.event_exists(
                article["title"]
            ):
                store.save_event(
                    article["title"],
                    article["source"],
                    classification
                )

                events_detected += 1

                print(
                    f"\nDetected Event: {classification.get('matched_event')}"
                )

                print(
                    f"Score: {classification.get('relevance_score')}"
                )

                print(
                    f"Matched Keywords: {classification.get('matched_keywords')}"
                )

                print(
                    f"Headline: {article['title']}"
                )

    print(f"Articles Found: {len(articles)}")
    print(f"Articles Saved: {saved_count}")
    print(f"Events Detected: {events_detected}")
    print(f"Database Articles: {store.count_articles()}")

    print("\nSample Articles:\n")
    for article in articles[:5]:
        print("TITLE:")
        print(article["title"])
        print("SOURCE:")
        print(article["source"])
        print("URL:")
        print(article["url"])
        print()