DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS bet;
DROP TABLE IF EXISTS createdby;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  balance INTEGER DEFAULT 20
);

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   uid INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );

CREATE TABLE bet (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  descr TEXT NOT NULL,
  ticket INTEGER DEFAULT 20
);

-- primary key is the combination of the two fereign keys
CREATE TABLE createdby (
  bid INTEGER,
  uid INTEGER,

  FOREIGN KEY (uid) REFERENCES user (id),
  FOREIGN KEY (bid) REFERENCES bet (id)
);