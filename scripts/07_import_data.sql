-- Script de importación de datos para FoodTrackDB
-- Usamos INSERTs manuales por seguridad y compatibilidad

-- 1. Insertar foodtrucks
INSERT INTO foodtrucks (foodtruck_id, name, cuisine_type, city)
VALUES 
(1, 'Taco Loco', 'Mexicana', 'Ciudad de México'),
(2, 'Burger Bros', 'Americana', 'Buenos Aires');

-- 2. Insertar products  
INSERT INTO products (product_id, foodtruck_id, name, price, stock)
VALUES 
(101, 1, 'Taco al pastor', 50, 100),
(102, 1, 'Quesadilla', 40, 80),
(103, 2, 'Cheeseburger', 70, 120),
(104, 2, 'Papas fritas', 30, 150);

-- 3. Insertar orders
INSERT INTO orders (order_id, foodtruck_id, order_date, status, total, comentarios)
VALUES 
(1001, 1, '2023-09-01', 'entregado', 90, NULL),
(1002, 2, '2023-09-01', 'pendiente', 100, NULL);

-- 4. Insertar order_items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity)
VALUES 
(1, 1001, 101, 1),
(2, 1002, 103, 1),
(3, 1002, 104, 1);

-- 5. Insertar locations
INSERT INTO locations (location_id, foodtruck_id, location_date, zone)
VALUES 
(1, 1, '2023-09-01', 'Centro'),
(2, 2, '2023-09-01', 'Parque');

-- Verificación
SELECT 'Datos insertados correctamente' as resultado;
