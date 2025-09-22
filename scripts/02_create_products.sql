-- Tabla para los productos
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    foodtruck_id INT NOT NULL,
    name NVARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    FOREIGN KEY (foodtruck_id) REFERENCES FoodTrucks(foodtruck_id)
);