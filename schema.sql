DROP TABLE IF EXISTS presidents;
DROP TABLE IF EXISTS vice_presidents;

CREATE TABLE presidents (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  party VARCHAR,
  year_elected INTEGER,
  is_alive BOOLEAN,
  vice_president_id INTEGER
);

CREATE TABLE vice_presidents (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  president_id INTEGER
);
