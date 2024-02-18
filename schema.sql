Create TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE blogs(
    id SERIAL PRIMARY KEY,
    content text,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE blog_likes(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    blog_id INTEGER REFERENCES blogs,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

