-- Insertion de l’administrateur
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
'Admin',
'HBnB',
'admin@hbnb.io',
'$2b$12$F0cMKcD8gF0uF2c1vZofGe0jMlRVNK7GEf3EJzRgWX4FHFkVYr.MK',
TRUE
);

-- Insertion des commodités initiales
INSERT INTO amenities (id, name) VALUES
('7b3e3737-ef53-4f13-8c38-6031e27d42ff', 'WiFi'),
('126eb780-f845-4ef8-8a68-e90b25534860', 'Swimming Pool'),
('b5c86946-44bb-4765-9db2-0ae21f190b47', 'Air Conditioning');

