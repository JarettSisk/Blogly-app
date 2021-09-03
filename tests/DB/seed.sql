-- Blogly database seed for initial setup.

-- Drop statement commented out to avoid formatting the DB
-- DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

-- Connect to the new db
\c blogly;

-- Creat the users table
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT,
    image_url TEXT NOT NULL DEFAULT 'https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80'
);

INSERT INTO users
(first_name, last_name, image_url)
VALUES
('Jarett', 'Sisk', 'https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80'),

('Abby', 'Schults', 'https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80'),

('Rob', 'Finly', 'https://images.unsplash.com/photo-1586861256632-f273baec5254?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1050&q=80'),

('Joann', 'Hopkins', 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80')