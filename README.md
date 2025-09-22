# 📊 FoodTrack DB

Un proyecto de base de datos para simular la gestión de operaciones de foodtrucks.

## ✨ Visión General

Este repositorio contiene el esquema de base de datos relacional inicial para **FoodTrack**, una plataforma diseñada para optimizar la gestión de las operaciones de foodtrucks en múltiples ubicaciones de una ciudad.

El objetivo principal es replicar un entorno de desarrollo profesional, utilizando tecnologías robustas como **Microsoft SQL Server** y aplicando rigurosas prácticas de **control de versiones con Git y GitHub** desde el inicio del proyecto. El diseño del esquema se centra en las entidades principales del negocio: foodtrucks, productos, pedidos, ubicaciones y el detalle de los ítems en cada pedido.

## 📦 Estructura del Repositorio

```
/foodtrack-db/
├── /python_scripts/
│   ├── cargar_datos.py

├── /scripts/
│   ├── 01_create_foodtrucks.sql
    ├── 02_create_products.sql
    ├── 03_create_orders.sql
    ├── 04_create_order_items.sql
    ├── 05_create_locations.sql
    ├── 06_add_comments_to_orders.sql
    └──  07_import_data.sql
├── /data/
│   ├── foodtrucks.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── locations.csv
└── README.md              # Documentación del proyecto.
```

## 🔗 Modelo Relacional

El diseño se basa en un modelo relacional normalizado, estableciendo claras relaciones entre las entidades del negocio. A continuación, se presenta una descripción del modelo y un esquema textual para su comprensión.

### **FoodTrucks**
- foodtruck_id (PK)
- name
- cuisine_type
- city

### **Products**
- product_id (PK)
- foodtruck_id (FK)
- name
- price
- stock

### **Locations**
- location_id (PK)
- foodtruck_id (FK)
- location_date
- zone

### **Orders**
- order_id (PK)
- foodtruck_id (FK)
- order_date
- status
- total
- comments (Evolución del esquema)

### **Order_Items** (Tabla de unión)
- order_item_id (PK)
- order_id (FK)
- product_id (FK)
- quantity

## 🚀 Instrucciones para la Configuración

Sigue estos pasos para replicar el entorno de la base de datos:

### 1. **Clonar el Repositorio:**
```bash
git clone https://github.com/dodo2003carl/foodtrack-db.git
```

### 2. **Configurar SQL Server:**
- Asegúrate de tener un servidor de Microsoft SQL Server en funcionamiento.
- Usa un cliente como DBeaver o SQL Server Management Studio para conectarte.
- Crea una nueva base de datos llamada `FoodTrackDB`.

### 3. **Crear el Esquema:**
- Abre el archivo `scripts/schema.sql`.
- Ejecuta el script para crear todas las tablas, claves y restricciones.

### 4. **Cargar los Datos:**
- Asegúrate de que los archivos `.csv` se encuentren en la ruta especificada.
- Abre el archivo `scripts/data_load.sql`.
- **Importante:** Modifica la ruta del archivo BULK INSERT para que apunte a la ubicación real de tus archivos `.csv`.
- Ejecuta el script para cargar los datos en las tablas.

### 5. **Verificar la Carga:**
- Ejecuta consultas de conteo de filas (`SELECT COUNT(*) FROM...`) para verificar que los datos se hayan importado correctamente en cada tabla.
