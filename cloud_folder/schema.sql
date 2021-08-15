DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS point_cloud;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT  NOT NULL
);

CREATE TABLE point_cloud (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cloudname TEXT NOT NULL,
    description TEXT NOT NULL,
    image BLOB,
    FOREIGN KEY (author_id) REFERENCES user (id)
);