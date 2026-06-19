import feedparser

from src.storage.event_store import EventStore

RSS_FEEDS = [

    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
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

    articles = fetch_articles()

    saved_count = 0

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

    print(
        f"Articles Found: {len(articles)}"
    )

    print(
        f"Articles Saved: {saved_count}"
    )

    print(
        f"Database Articles: "
        f"{store.count_articles()}"
    )

    print("\nSample Articles:\n")

    for article in articles[:5]:

        print("TITLE:")
        print(article["title"])

        print("SOURCE:")
        print(article["source"])

        print("URL:")
        print(article["url"])
        print()