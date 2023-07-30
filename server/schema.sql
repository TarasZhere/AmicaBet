-- USER
DROP TABLE IF EXISTS user;
CREATE TABLE user (
  Uid INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  balance INTEGER DEFAULT 20
);

INSERT INTO user (email, password, fname, lname, balance) VALUES
('gw@president.com', 'defaultPassword', 'George', 'Washington', NULL),
('ja@president.com', 'defaultPassword', 'John', 'Adams', NULL),
('tj@president.com', 'defaultPassword', 'Thomas', 'Jefferson', NULL);

-- FREIND REQUEST: relation
DROP TABLE IF EXISTS friendRequest;
CREATE TABLE friendRequest (
    sender_Uid INTEGER,
    receiver_Uid INTEGER,
    status VARCHAR(12) CHECK( status IN ('pending','accepted','rejected', 'blocked') ) DEFAULT 'pending',

    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sender_Uid) REFERENCES user(Uid),
    FOREIGN KEY (receiver_Uid) REFERENCES user(Uid),

    PRIMARY KEY (sender_Uid, receiver_Uid)
);


-- PROFILE INFO
DROP TABLE IF EXISTS profileInfo;
CREATE TABLE profileInfo (
    uid INTEGER,
    FOREIGN KEY (uid) REFERENCES user(id),
    -- adding more information
    -- add information about user
    phone_number TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT,
    ratio FLOAT, -- expresses the total number of bets divided by the number of bets won
    PRIMARY KEY (uid)
);


-- BET
DROP TABLE IF EXISTS bet;
CREATE TABLE bet (
    Bid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status VARCHAR(12) CHECK( status IN ('pending','running','rejected', 'closed') ) DEFAULT 'pending',
    ticket INTEGER NOT NULL DEFAULT 20
);

-- RELATIONAL SCHEMA
-- primary key is the combination of the two fereign keys
DROP TABLE IF EXISTS invite;
CREATE TABLE invite (
    Bid INTEGER NOT NULL,
    Uid INTEGER NOT NULL,
    invited_Uid INTEGER NOT NULL,
    status VARCHAR(12) CHECK( status IN ('pending','accepted','rejected') ) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (Uid) REFERENCES user(Uid),
    FOREIGN KEY (invited_Uid) REFERENCES user(Uid),
    FOREIGN KEY (Bid) REFERENCES bet(Bid),

    PRIMARY KEY (Bid, Uid)
);

-- RELATIONAL SCHEMA
-- primary key is the combination of the two fereign keys
DROP TABLE IF EXISTS win;
CREATE TABLE win (
    Bid INTEGER NOT NULL,
    Uid INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (Uid) REFERENCES user(Uid),
    FOREIGN KEY (Bid) REFERENCES bet(Bid),
    PRIMARY KEY (Uid, Bid)
);

-- RELATIONAL SCHEMA
-- primary key is the combination of the two fereign keys
DROP TABLE IF EXISTS vote;
CREATE TABLE vote (
    Bid INTEGER NOT NULL,
    Uid INTEGER NOT NULL,
    voted_Uid INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (voted_Uid) REFERENCES user(Uid),

    FOREIGN KEY (Uid) REFERENCES user(Uid),
    FOREIGN KEY (Bid) REFERENCES bet(Bid),
    PRIMARY KEY (Uid, Bid)
);