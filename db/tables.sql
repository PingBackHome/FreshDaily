-- freshdaily.sql

-- Maak de 'tickets' tabel aan
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    subject TEXT,
    created_at TEXT,
    status INTEGER,
    responder_id INTEGER,
    priority INTEGER,
    agent TEXT
);
