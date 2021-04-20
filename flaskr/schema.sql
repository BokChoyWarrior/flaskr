DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  likes INTEGER DEFAULT 0,
  deleted INTEGER DEFAULT 0,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE likes (
  user_id INTEGER,
  post_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user (id)
  FOREIGN KEY (post_id) REFERENCES posts (id)
  PRIMARY KEY (user_id, post_id)
)