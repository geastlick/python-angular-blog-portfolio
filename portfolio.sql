-- create the database
DROP DATABASE IF EXISTS blog_portfolio;
CREATE DATABASE blog_portfolio;
-- connect via psql
\c blog_portfolio

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;


---
--- CREATE tables
---
CREATE TABLE users (
    id          SERIAL NOT NULL,
    username    VARCHAR(30) NOT NULL,
    password    VARCHAR(128) NOT NULL,
    name        VARCHAR(128) NOT NULL,
    email       VARCHAR(255),
    avatar      BYTEA,
    block_until TIMESTAMP(6),
    CONSTRAINT user_pk  PRIMARY KEY (id),
    CONSTRAINT user_uq1 UNIQUE (username),
    CONSTRAINT user_uq2 UNIQUE (email)
);

CREATE TABLE blog_category (
    id          SERIAL NOT NULL,
    name        VARCHAR(40) NOT NULL,
    description TEXT NOT NULL,
    CONSTRAINT category_pk  PRIMARY KEY (id),
    CONSTRAINT category_uq1 UNIQUE (name)
);

CREATE TABLE blog (
    id          BIGSERIAL NOT NULL,
    title       VARCHAR(250) NOT NULL,
    category_id BIGINT NOT NULL,
    description TEXT NOT NULL,
    author      INT NOT NULL,
    published   TIMESTAMP(6),
    CONSTRAINT blog_pk PRIMARY KEY (id),
    CONSTRAINT blog_fk1 FOREIGN KEY (author) REFERENCES users (id),
    CONSTRAINT blog_fk2 FOREIGN KEY (category_id) REFERENCES blog_category (id)
);

CREATE TABLE blog_entry (
    id          BIGSERIAL NOT NULL,
    entry       TEXT NOT NULL,
    blog_id     BIGINT NOT NULL,
    published   TIMESTAMP(6),
    CONSTRAINT blog_entry_pk PRIMARY KEY (id),
    CONSTRAINT blog_entry_fk1 FOREIGN KEY (blog_id) REFERENCES blog (id)

);

CREATE TABLE comment (
    id              BIGSERIAL NOT NULL,
    entry           TEXT NOT NULL,
    user_id         INTEGER NOT NULL,
    blog_entry_id   BIGINT,
    parent_id       BIGINT,
    CONSTRAINT comment_pk PRIMARY KEY (id),
    CONSTRAINT comment_uq1 UNIQUE (blog_entry_id, user_id),
    CONSTRAINT comment_uq2 UNIQUE (parent_id, user_id),
    CONSTRAINT comment_fk1 FOREIGN KEY (blog_entry_id) REFERENCES blog_entry (id),
    CONSTRAINT comment_fk2 FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT comment_fk3 FOREIGN KEY (parent_id) REFERENCES comment (id),
    CONSTRAINT comment_ck1 CHECK ((blog_entry_id IS NOT NULL OR parent_id IS NOT NULL) AND
                                  (blog_entry_id IS NULL OR parent_id IS NULL))
);

CREATE TABLE rating (
  id              SERIAL NOT NULL,
  emoji           BYTEA NOT NULL,
  description     VARCHAR(10) NOT NULL,
  CONSTRAINT rating_pk PRIMARY KEY (id)
);

CREATE TABLE blog_rating (
    blog_id    BIGINT NOT NULL,
    user_id    INTEGER NOT NULL,
    rating_id  INTEGER NOT NULL,
    CONSTRAINT blog_rating_pk PRIMARY KEY (blog_id, user_id),
    CONSTRAINT blog_rating_fk1 FOREIGN KEY (blog_id) REFERENCES blog (id),
    CONSTRAINT blog_rating_fk2 FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT blog_rating_fk3 FOREIGN KEY (rating_id) REFERENCES rating (id)
);

CREATE TABLE blog_entry_rating (
    blog_entry_id BIGINT NOT NULL,
    user_id       INTEGER NOT NULL,
    rating_id     INTEGER NOT NULL,
    CONSTRAINT blog_entry_rating_pk PRIMARY KEY (blog_entry_id, user_id),
    CONSTRAINT blog_entry_rating_fk1 FOREIGN KEY (blog_entry_id) REFERENCES blog_entry (id),
    CONSTRAINT blog_entry_rating_fk2 FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT blog_entry_rating_fk3 FOREIGN KEY (rating_id) REFERENCES rating (id)
);

CREATE TABLE comment_rating (
    comment_id BIGINT NOT NULL,
    user_id    INTEGER NOT NULL,
    rating_id  INTEGER NOT NULL,
    CONSTRAINT comment_rating_pk PRIMARY KEY (comment_id, user_id),
    CONSTRAINT comment_rating_fk1 FOREIGN KEY (comment_id) REFERENCES comment (id),
    CONSTRAINT comment_rating_fk2 FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT comment_rating_fk3 FOREIGN KEY (rating_id) REFERENCES rating (id)
);

CREATE TABLE follow_author (
    author     INTEGER NOT NULL,
    follower   INTEGER NOT NULL,
    CONSTRAINT follow_author_pk PRIMARY KEY (author, follower),
    CONSTRAINT follow_author_fk1 FOREIGN KEY (author) REFERENCES users (id),
    CONSTRAINT follow_author_fk2 FOREIGN KEY (follower) REFERENCES users (id)
);

CREATE TABLE follow_blog (
    blog       INTEGER NOT NULL,
    follower   INTEGER NOT NULL,
    CONSTRAINT follow_blog_pk PRIMARY KEY (blog, follower),
    CONSTRAINT follower_blog_fk1 FOREIGN KEY (blog) REFERENCES blog (id),
    CONSTRAINT follower_blog_fk2 FOREIGN KEY (follower) REFERENCES users (id)
);
