-- Tabla para las ubicaciones
CREATE TABLE Locations (
    location_id INT PRIMARY KEY,
    foodtruck_id INT NOT NULL,
    location_date DATE NOT NULL,
    zone NVARCHAR(255),
    FOREIGN KEY (foodtruck_id) REFERENCES FoodTrucks(foodtruck_id)
);
