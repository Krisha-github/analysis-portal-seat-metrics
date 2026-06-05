CREATE DATABASE IF NOT EXISTS josaa_portal;
USE josaa_portal;

DROP TABLE IF EXISTS seat_allotment;

CREATE TABLE seat_allotment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    round_no INT,
    institute VARCHAR(255),
    academic_program VARCHAR(255),
    quota VARCHAR(50),
    seat_type VARCHAR(50),
    gender VARCHAR(50),
    opening_rank INT,
    closing_rank INT
);