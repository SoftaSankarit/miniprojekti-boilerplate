

CREATE TABLE type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE reference (
    id SERIAL PRIMARY KEY,
    type_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    year INT,
    publisher VARCHAR(100),
    howpublished VARCHAR(100),
    institution VARCHAR(200),
    journal VARCHAR(100),
    volume VARCHAR(50),
    number INT,
    organization VARCHAR(100),
    school VARCHAR(100),
    series VARCHAR(100),
    issue VARCHAR(50),
    edition VARCHAR(100),
    chapter VARCHAR(50),
    pages VARCHAR(50),
    url VARCHAR(500),
    key VARCHAR(100),
    month VARCHAR(50),
    note TEXT, 
    misc_details TEXT,
    doi VARCHAR(150),
    FOREIGN KEY (type_id) REFERENCES type (id)
);

INSERT INTO type (name) VALUES
('Book'),
('Article'),
('Misc'),
('ConferencePaper'),
('Thesis'),
('Report'),
('Webpage'),
('Patent'),
('Software'),
('Standard'),
('Dataset'),
('Manual'),
('Presentation'),
('Encyclopedia');