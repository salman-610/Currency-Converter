

CREATE DATABASE IF NOT EXISTS currency_converter;

USE currency_converter;

CREATE TABLE IF NOT EXISTS conversion_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    exchange_rate DECIMAL(20, 8) NOT NULL,
    converted_amount DECIMAL(15, 2) NOT NULL,
    converted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
