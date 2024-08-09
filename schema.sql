CREATE TABLE lkbooks (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    reading_started BOOLEAN,
    reading_completed BOOLEAN,
    book_language TEXT,
    stars INTEGER
);
