INSERT INTO book (id, isbn, title, author, publisher, request)
VALUES
(1, '978-1593279127', 'Practical Binary Analysis: Build Your Own Linux Tools for Binary Instrumentation, Analysis, and Disassembly', 'Dennis Andriesse', 'No Starch Press', 0),
(2, '1782167102', 'Learning Linux Binary Analysis', "Ryan 'elfmaster' O'Neil", 'PACKT', 0),
(3, '978-1491991732', 'Flask Web Development', 'Miguel Grinberg', "O'Reilly", 0),
(4, '978-3103974829', 'Permanent Record', 'Edward Snowden', "S. Fischer", 1),
(5, '978-1593272203', 'The Linux Programming Interface', 'Michael Kerrisk', "No Starch Press", 1);

INSERT INTO comments (text, book_id) VALUES 
('Tolles buch 10 von 10.', 1), 
('Nicht so mein Fall', 1), 
('Sehr schöne Schreibweise', 5), 
('Ersten drei Kapitel alleine rechtfertigen schon den Preis', 5), 
('Ich bin ein Hacker', 4), 
('OMG so guuuut', 3);
