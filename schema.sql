-- Create TABLE admins
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create TABLE users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create TABLE credentials
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create TABLE blogs
CREATE TABLE blogs (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create TABLE blog_likes
CREATE TABLE blog_likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    blog_id INTEGER REFERENCES blogs ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for users
INSERT INTO users (username, name, created_at) 
VALUES ('hamedebadi', 'hamed', NOW());

-- Insert sample data for credentials
INSERT INTO credentials (user_id, password_hash, created_at) 
VALUES (1, 'hashed_password', NOW());

-- Insert sample data for blogs
INSERT INTO blogs (content, user_id, created_at) 
VALUES ('This is the first blog created by me to and you can create your own by clicking on creating button!', 1, NOW()),
       ('It''s crazy that we have to study math for computer science, I mean who even knew that fact, right?', 1, NOW()),
       ('I wish every course on computer science program was this interesting and easy!!!', 1, NOW());
