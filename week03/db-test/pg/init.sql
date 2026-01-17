-- Clean up existing objects if they exist
DROP VIEW IF EXISTS order_summary;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- Create Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0
);

-- Create Orders Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, cancelled
    total_amount DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Order Items Table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Create View: Order Summary
CREATE VIEW order_summary AS
SELECT 
    o.id AS order_id,
    u.username,
    o.total_amount,
    o.status,
    o.created_at,
    COUNT(oi.id) as items_count
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.username, o.total_amount, o.status, o.created_at;

-- Insert Sample Data using generate_series for volume
INSERT INTO users (username, email) 
SELECT 
    'user_' || s, 
    'user_' || s || '@example.com'
FROM generate_series(1, 50) AS s;

INSERT INTO products (name, price, stock_quantity)
SELECT 
    'Product ' || s,
    (random() * 100 + 10)::decimal(10,2),
    (random() * 100)::int
FROM generate_series(1, 20) AS s;

INSERT INTO orders (user_id, status, total_amount)
SELECT 
    (floor(random() * 50) + 1)::int,
    CASE (floor(random() * 3))::int 
        WHEN 0 THEN 'pending' 
        WHEN 1 THEN 'completed' 
        ELSE 'cancelled' 
    END,
    (random() * 500 + 20)::decimal(10,2)
FROM generate_series(1, 100) AS s;

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT 
    (floor(random() * 100) + 1)::int,
    (floor(random() * 20) + 1)::int,
    (floor(random() * 5) + 1)::int,
    (random() * 100 + 10)::decimal(10,2)
FROM generate_series(1, 200) AS s;
