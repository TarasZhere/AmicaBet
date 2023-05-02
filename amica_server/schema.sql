DROP TABLE IF EXISTS requestStaus;
DROP TABLE IF EXISTS creates;
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS voided;
DROP TABLE IF EXISTS settled;


-- USER
DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  balance INTEGER DEFAULT 20
);

-- REQUEST STATUS
DROP TABLE IF EXISTS requestStaus;
CREATE TABLE requestStaus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status VARCHAR(10) UNIQUE
);

INSERT INTO requestStaus (status)
VALUES ('pending'), ('blocked'), ('rejected'), ('accepted');

-- FREIND REQUEST: relation
DROP TABLE IF EXISTS friendRequest;
CREATE TABLE friendRequest (
    rs_id INTEGER DEFAULT 1, -- default is on pending
    sender_uid INTEGER,
    receiver_uid INTEGER,

    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sender_uid) REFERENCES user(id),
    FOREIGN KEY (receiver_uid) REFERENCES user(id),
    FOREIGN KEY (rs_id) REFERENCES requestStaus(id),

    PRIMARY KEY (sender_uid, receiver_uid, rs_id)
);


-- PROFILE INFO
DROP TABLE IF EXISTS profileInfo;
CREATE TABLE profileInfo (
    uid INTEGER,
    FOREIGN KEY (uid) REFERENCES user(id),
    -- adding more information

    PRIMARY KEY (uid)
);


-- BET
DROP TABLE IF EXISTS bet;
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id),
    PRIMARY KEY (uid, bid)
);

-- RELETIONAL SCHEMA
CREATE TABLE challenges (
    bid INTEGER,
    uid INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id),
    PRIMARY KEY (uid, bid)
);

-- RELETIONAL SCHEMA
CREATE TABLE voided (
    bid INTEGER,
    uid INTEGER,

    retained FLOAT NOT NULL,

    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id),

    PRIMARY KEY (uid, bid)
);

-- RELETIONAL SCHEMA
CREATE TABLE settled (
    bid INTEGER,
    uid INTEGER,

    winner FLOAT NOT NULL,

    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (bid) REFERENCES bet(id),
    PRIMARY KEY (uid, bid)
);