CREATE DATABASE job_portal;
USE job_portal;

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    description TEXT,
    employer VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

select *from jobs;