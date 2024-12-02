-- Luo type-taulu
CREATE TABLE type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Luo reference-taulu
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
    address VARCHAR(200),
    FOREIGN KEY (type_id) REFERENCES type (id)
);

-- Lisää aloitustiedot type-tauluun
INSERT INTO type (name) VALUES
('article')
-- ('book'),
-- ('booklet'),
-- ('conference'),
-- ('inbook'),
-- ('incollection'),
-- ('inproceedings'),
-- ('manual'),
-- ('mastersthesis'),
-- ('misc'),
-- ('phdthesis'),
-- ('proceedings'),
-- ('techreport'),
-- ('unpublished')