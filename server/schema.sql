DROP TABLE IF EXISTS requestStaus;
DROP TABLE IF EXISTS creates;
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS voided;
DROP TABLE IF EXISTS settled;


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
    status VARCHAR(12) CHECK( status IN ('pending','accepted','rejected', 'blocked') ) DEFAULT 1,

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

    PRIMARY KEY (uid)
);


-- BET
DROP TABLE IF EXISTS bet;
CREATE TABLE bet (
  Bid INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  descr TEXT NOT NULL,
  ticket INTEGER DEFAULT 20, 
  pool INTEGER DEFAULT 20
);

-- RELATIONAL SCHEMA
-- primary key is the combination of the two fereign keys
CREATE TABLE creates (
    Bid INTEGER,
    Uid INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Uid) REFERENCES user(Uid),
    FOREIGN KEY (Bid) REFERENCES bet(Bid),
    PRIMARY KEY (Uid, Bid)
);

