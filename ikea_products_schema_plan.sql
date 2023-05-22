create database if not exists ikea_products;

use ikea_products;

CREATE TABLE IF NOT EXISTS product_categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    price DECIMAL NOT NULL,
    image VARCHAR(300) NOT NULL,
    other_colors BOOLEAN,
    short_description VARCHAR(200),
    designer VARCHAR(100),
    depth FLOAT,
    height FLOAT,
    width FLOAT,
    category_id INT,
    FOREIGN KEY (category_id)
        REFERENCES product_categories (category_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_reviews (
    product_review_id INT PRIMARY KEY AUTO_INCREMENT,
    num_stars INT NOT NULL,
    product_id INT,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    customer_pass VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_product_review (
    customer_id INT,
    product_review_id INT,
    PRIMARY KEY (customer_id , product_review_id),
    FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_review_id)
        REFERENCES product_reviews (product_review_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customer_products (
    customer_id INT,
    product_id INT,
    product_quantity INT NOT NULL,
    PRIMARY KEY (customer_id , product_id),
    FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);