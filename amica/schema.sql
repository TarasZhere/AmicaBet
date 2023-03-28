DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS bet;
DROP TABLE IF EXISTS creates;
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS voided;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  balance INTEGER DEFAULT 20
);

CREATE TABLE bet (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  descr TEXT NOT NULL,
  ticket INTEGER DEFAULT 20, 
  pool INTEGER DEFAULT 20
);

-- RELATIONAL SCHEMA
-- primary key is the combination of the two fereign keys
CREATE TABLE creates (
    bid INTEGER,
    uid INTEGER,
    PRIMARY KEY (uid, bid),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id)
);

-- RELETIONAL SCHEMA
CREATE TABLE challenges (
    bid INTEGER,
    uid INTEGER,
    PRIMARY KEY (uid, bid),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id)
);

-- RELETIONAL SCHEMA
CREATE TABLE voided (
    bid INTEGER,
    uid INTEGER,
    PRIMARY KEY (uid, bid),

    retained FLOAT NOT NULL,

    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id)
);

-- RELETIONAL SCHEMA
CREATE TABLE settled (
    bid INTEGER,
    uid INTEGER,
    PRIMARY KEY (uid, bid),

    winner FLOAT NOT NULL,

    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id)
);