CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE
);
