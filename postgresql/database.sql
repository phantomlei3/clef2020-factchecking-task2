CREATE TABLE claims(
    vclaim_id INT PRIMARY KEY,
    vclaim TEXT,
    title VARCHAR(255)
);

CREATE TABLE tweets(
    tweet_id INT PRIMARY KEY,
    tweet_content TEXT
);

CREATE TABLE train_pairs(
    tweet_id INT,
    vclaim_id INT
);

CREATE TABLE dev_pairs(
    tweet_id INT,
    vclaim_id INT
);
