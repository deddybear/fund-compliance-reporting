CREATE TABLE audit_event
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_type TEXT NOT NULL,

    status TEXT NOT NULL,

    trigger_name TEXT NOT NULL,

    message TEXT,

    payload TEXT,

    created_at TEXT NOT NULL
);