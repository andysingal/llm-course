create database rahulshettyacademy;
use rahulshettyacademy;

CREATE TABLE RegistrationDetails (
    id_number VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    occupation VARCHAR(100),
    gender VARCHAR(10),
    password VARCHAR(255), -- Storing passwords in plain text is insecure in a real application
    is_18_or_older BOOLEAN
);

CREATE TABLE UserNames (
    id_number VARCHAR(50) PRIMARY KEY,
    email VARCHAR(200),
    FOREIGN KEY (id_number) REFERENCES RegistrationDetails(id_number)
);

-- Inserting data into RegistrationDetails table
INSERT INTO RegistrationDetails (id_number, first_name, last_name, phone_number, occupation, gender, password, is_18_or_older) VALUES
('USER001', 'John', 'Doe', '123-456-7890', 'Engineer', 'Male', '12345', TRUE),
('USER002', 'Jane', 'Smith', '987-654-3210', 'Teacher', 'Female', '12345', TRUE),
('USER003', 'Peter', 'Jones', '555-123-4567', 'Student', 'Male', '12345', FALSE),
('USER004', 'Alice', 'Brown', '111-222-3333', 'Doctor', 'Female', '12345', TRUE),
('USER005', 'David', 'Wilson', '444-555-6666', 'Artist', 'Male', '12345', TRUE);

-- Inserting data into UserNames table
INSERT INTO UserNames (id_number, email) VALUES
('USER001', 'JohnDoe434@gmail.com'),
('USER002', 'JaneSmithgdfgf@gmail.com'),
('USER003', 'PeterJones5454@gmail.com'),
('USER004', 'AliceB3232wn@gmail.com'),
('USER005', 'DavidW24lson@gmail.com');

CREATE TABLE Customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    age INT
);

-- Table: Orders
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT, -- Added auto-increment for easier insertion
    customer_id INT,
    subject VARCHAR(100),
    company VARCHAR(100),
    order_date DATE, -- Added an order date for potential grouping/filtering
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);


INSERT INTO Customers (id, name, city, age) VALUES
(1, 'Alice Smith', 'New York', 30),
(2, 'Bob Johnson', 'Los Angeles', 25),
(3, 'Charlie Brown', 'Chicago', 35),
(4, 'David Lee', 'New York', 28),
(5, 'Eve Williams', 'Houston', 32),
(6, 'Frank Miller', 'Los Angeles', 40);



INSERT INTO Orders (customer_id, subject, company, order_date) VALUES
(1, 'Laptop', 'Tech Solutions Inc.', '2024-01-15'),
(1, 'Software License', 'Global Software Corp', '2024-02-20'),
(2, 'Marketing Services', 'Ad Agency Pro', '2024-03-10'),
(3, 'Consulting Services', 'Business Growth Ltd.', '2024-04-01'),
(3, 'Training Program', 'EduTech Systems', '2024-05-05'),
(4, 'Web Development', 'Creative Web Design', '2024-06-12'),
(5, 'Cloud Storage', 'Data Secure Cloud', '2024-07-25'),
(2, 'Graphic Design', 'Visual Arts Studio', '2024-08-18'),
(1, 'Technical Support', 'Tech Solutions Inc.', '2024-09-01'),
(6, 'Hardware Upgrade', 'Computer Parts Plus', '2024-10-10');





-- Get the names of customers who have placed at least one order
SELECT name
FROM Customers
WHERE id IN (SELECT DISTINCT customer_id FROM Orders);


-- Find companies that have placed more than one order
SELECT company, COUNT(*) AS total_orders
FROM Orders
GROUP BY company
HAVING COUNT(*) > 1;


select * from RegistrationDetails;
select * from UserNames;

SELECT
    rd.id_number,
    rd.first_name,
    rd.last_name,
    un.email,
    rd.phone_number,
    rd.occupation,
    rd.gender,
    rd.is_18_or_older
FROM
    RegistrationDetails rd
JOIN
    UserNames un ON rd.id_number = un.id_number;





