CREATE DATABASE IF NOT EXISTS school;
USE school;

CREATE TABLE IF NOT EXISTS students (
    roll_no INT PRIMARY KEY,
    name VARCHAR(50),
    class VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS marks (
    roll_no INT,
    subject VARCHAR(30),
    marks INT,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
);


