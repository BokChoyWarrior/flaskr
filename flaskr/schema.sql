-- legacy table names
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS categories;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  picture TEXT NOT NULL DEFAULT "default.jpg"
);

CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category INTEGER,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  likes INTEGER DEFAULT 1,
  deleted INTEGER DEFAULT 0,
  FOREIGN KEY (author_id) REFERENCES users (id)
  FOREIGN KEY (category) references categories (id)
);

CREATE TABLE post_likes (
  user_id INTEGER,
  post_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users (id)
  FOREIGN KEY (post_id) REFERENCES posts (id)
  PRIMARY KEY (user_id, post_id)
);

CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  comment_thread TEXT NOT NULL,
  deleted INTEGER DEFAULT 0,
  -- 1 like from the user
  likes INTEGER DEFAULT 1,
  FOREIGN KEY (author_id) REFERENCES users (id)
  FOREIGN KEY (post_id) REFERENCES posts (id)

);

CREATE TABLE comment_likes (
  user_id INTEGER,
  comment_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES users (id)
  FOREIGN KEY (comment_id) REFERENCES comments (id)
  PRIMARY KEY (user_id, comment_id)
);