import sqlite3


class EventStore:

    def __init__(self):

        self.connection = sqlite3.connect(
            "data/geopolitical_events.db"
        )

        self.cursor = self.connection.cursor()

        self.create_events_table()

        self.create_articles_table()

    def count_events(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM events
        """)

        return self.cursor.fetchone()[0]

    def create_events_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            headline TEXT,
            
            source TEXT,

            matched_event TEXT,

            event_category TEXT,

            severity TEXT,

            relevance_score INTEGER,

            matched_keywords TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

    def create_articles_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            source TEXT,

            url TEXT UNIQUE,

            published_at TEXT,

            summary TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

    def event_exists(self, headline):
        """
        Check whether an event headline has already been stored
        to prevent duplicate intelligence records.
        """

        self.cursor.execute("""
        SELECT 1
        FROM events
        WHERE headline = ?
        """, (headline,))

        result = self.cursor.fetchone()

        return result is not None
    
    def article_exists(self, url):

        self.cursor.execute("""
        SELECT 1
        FROM articles
        WHERE url = ?
        """, (url,))

        result = self.cursor.fetchone()

        return result is not None
    
    def count_articles(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM articles
        """)

        return self.cursor.fetchone()[0]

    def save_event(self, headline, source, classification):

        self.cursor.execute("""
        INSERT INTO events (
            headline,
            source,
            matched_event,
            event_category,
            severity,
            relevance_score,
            matched_keywords
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            headline,

            source,

            classification["matched_event"],

            classification["event_category"],

            classification["severity"],

            classification["relevance_score"],

            ", ".join(classification["matched_keywords"])
        ))

        self.connection.commit()

        print(f"Saved event: {headline}")

    def save_article(
        self,
        title,
        source,
        url,
        published_at,
        summary
    ):

        self.cursor.execute("""
        INSERT INTO articles (
            title,
            source,
            url,
            published_at,
            summary
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            source,
            url,
            published_at,
            summary
        ))

        self.connection.commit()

    def fetch_all_events(self):

        """
        Retrieve the complete historical intelligence record
        stored in the event database.
        """
        self.cursor.execute("""
        SELECT
            id,
            headline,
            matched_event,
            event_category,
            severity,
            relevance_score,
            matched_keywords,
            created_at
        FROM events
        ORDER BY id DESC
        """)

        events = self.cursor.fetchall()

        return events
    
    def fetch_recent_events(self, limit=10):

        """Retrieve the most recently detected intelligence events.
        Returns events ordered by timestamp (newest first).
        """

        self.cursor.execute("""
        SELECT
            id,
            headline,
            source,
            matched_event,
            event_category,
            severity,
            relevance_score,
            matched_keywords,
            created_at
        FROM events
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()
    
    def fetch_high_relevance_events(self, min_score=5):
        """
        Retrieve strategically significant events above a specified
        relevance threshold. Results are ranked by relevance score.
        """

        self.cursor.execute("""
        SELECT
            id,
            headline,
            source,
            matched_event,
            event_category,
            severity,
            relevance_score,
            matched_keywords,
            created_at
        FROM events
        WHERE relevance_score >= ?
        ORDER BY relevance_score DESC,
                 created_at DESC
        """, (min_score,))

        return self.cursor.fetchall()

if __name__ == "__main__":

    store = EventStore()

    events = store.fetch_high_relevance_events(5) # Demonstrate fetching events with relevance score of 5 or higher

    # events = store.fetch_all_events() # Fetch all events in the database
    # events = store.fetch_recent_events(5) # Fetch the 5 most recent events
    
    for event in events:

        print(event)