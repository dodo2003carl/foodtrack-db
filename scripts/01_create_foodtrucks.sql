-- Tabla para los foodtrucks
CREATE TABLE FoodTrucks (
    foodtruck_id INT PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    cuisine_type NVARCHAR(255),
    city NVARCHAR(255)
);
