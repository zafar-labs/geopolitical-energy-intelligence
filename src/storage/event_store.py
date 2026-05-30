import sqlite3


class EventStore:

    def __init__(self, db_path="data/geopolitical_events.db"):

        self.connection = sqlite3.connect(db_path)

        self.cursor = self.connection.cursor()

        self.create_events_table()

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

    def event_exists(self, headline):

        self.cursor.execute("""
        SELECT 1
        FROM events
        WHERE headline = ?
        """, (headline,))

        result = self.cursor.fetchone()

        return result is not None

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

    def fetch_all_events(self):
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


if __name__ == "__main__":

    store = EventStore()

    events = store.fetch_all_events()

    for event in events:

        print(event)