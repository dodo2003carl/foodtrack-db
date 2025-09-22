-- Tabla para los pedidos
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    foodtruck_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    status NVARCHAR(50) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    comments NVARCHAR(MAX), -- Columna agregada para la evolución del esquema
    FOREIGN KEY (foodtruck_id) REFERENCES FoodTrucks(foodtruck_id)
);