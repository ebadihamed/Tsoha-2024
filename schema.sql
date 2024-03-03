Create TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blogs(
    id SERIAL PRIMARY KEY,
    content text,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blog_likes(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    blog_id INTEGER REFERENCES blogs,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, name, created_at) VALUES ("hamedebadi", "hamed", NOW());
INSERT INTO credentials (user_id, password_hash, created_at) VALUES (1, 12345, NOW());
INSERT INTO blogs (content, user_id, created_at) VALUES ("This is the first blog created by me to and you can create your own by clicking on creating button!", 1, NOW());
INSERT INTO blogs (content, user_id, created_at) VALUES ("It's crazy that we have to study math for computer science, I mean who even knew that fact, right?", 1, NOW());
INSERT INTO blogs (content, user_id, created_at) VALUES ("I wish every course on computer science program was this interesting and easy!!!", 1, NOW());