-- --------------------------------------------
-- Datos de prueba
-- --------------------------------------------

-- Categorías
INSERT INTO categories (name, description) VALUES
('Tortas',   'Tortas artesanales con pan telera'),
('Bebidas',  'Aguas, refrescos y jugos'),
('Extras',   'Complementos y guarniciones'),
('Postres',  'Dulces y postres caseros');

-- Productos
INSERT INTO products (category_id, name, description, price) VALUES
(1, 'Torta de Milanesa',   'Milanesa de res con jitomate, lechuga y aguacate', 65.00),
(1, 'Torta de Pierna',     'Pierna de cerdo deshebrada con chipotle',           60.00),
(1, 'Torta de Jamón',      'Jamón con queso, crema y jalapeño',                 55.00),
(2, 'Agua de Horchata',    'Agua fresca de arroz con canela, 500ml',            25.00),
(2, 'Refresco',            'Coca-Cola, Pepsi o Sprite 355ml',                   20.00),
(3, 'Papas a la Francesa', 'Porción de papas fritas con sal',                   30.00),
(4, 'Flan Napolitano',     'Flan casero con cajeta',                            35.00);

-- Usuario administrador (contraseña: admin123 — se hasheará desde la API)
-- Por ahora insertamos el hash directamente para pruebas
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@torteria.com', '$2b$12$placeholder_hash_cambiar_desde_api', 'admin');