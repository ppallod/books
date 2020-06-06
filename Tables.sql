CREATE TABLE users (
    user_id SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(10) NOT NULL,
    password VARCHAR(10) NOT NULL
);

CREATE TABLE books (
    isbn VARCHAR(10) NOT NULL PRIMARY KEY,
    title VARCHAR(70) NOT NULL,
    author VARCHAR(30) NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE reviews (
    user_id INTEGER NOT NULL REFERENCES users(user_id), 
    isbn VARCHAR(10) NOT NULL REFERENCES books(isbn),
    rating INTEGER NOT NULL,
    review VARCHAR(1000) NOT NULL,
    PRIMARY KEY (user_id,isbn)
);