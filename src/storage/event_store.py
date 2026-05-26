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

            matched_event TEXT,

            event_category TEXT,

            severity TEXT,

            relevance_score INTEGER,

            matched_keywords TEXT
        )
        """)

        self.connection.commit()

    def save_event(self, headline, classification):

        self.cursor.execute("""
        INSERT INTO events (
            headline,
            matched_event,
            event_category,
            severity,
            relevance_score,
            matched_keywords
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            headline,

            classification["matched_event"],

            classification["event_category"],

            classification["severity"],

            classification["relevance_score"],

            ", ".join(classification["matched_keywords"])
        ))

        self.connection.commit()

        print(f"Saved event: {headline}")


if __name__ == "__main__":

    store = EventStore()