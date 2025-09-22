import pyodbc
import pandas as pd
import os
import sys
from datetime import datetime

def main():
    """
    Script completo para cargar datos en FoodTrack DB
    Maneja conexión, limpieza de tablas y carga de datos CSV
    """
    
    # Configuración de conexión
    server = 'localhost\\SQLEXPRESS'
    database = 'FoodTrackDB'
    
    # Variables de control
    conn = None
    cursor = None
    
    try:
        print("=" * 60)
        print("🚀 FOODTRACK DB - CARGADOR DE DATOS")
        print("=" * 60)
        print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Conectar a SQL Server
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )
        cursor = conn.cursor()
        print("✅ Conexión exitosa a SQL Server")

        # Verificar estructura de directorios
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        
        print(f"📂 Script ubicado en: {script_dir}")
        print(f"📂 Buscando datos en: {os.path.abspath(data_dir)}")
        
        if not os.path.exists(data_dir):
            print("❌ Directorio 'data' no encontrado")
            print("   Creando estructura recomendada...")
            os.makedirs(data_dir, exist_ok=True)
            print("   Por favor, coloca los archivos CSV en la carpeta 'data'")
            return
        
        archivos_csv = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        print(f"📁 Archivos CSV encontrados: {archivos_csv}")

        # Crear tabla de errores si no existe
        create_error_table(cursor, conn)
        
        # Limpiar tablas existentes
        clean_tables(cursor, conn)
        
        # Cargar datos desde CSV
        load_all_data(cursor, conn, data_dir)
        
        # Mostrar resumen final
        show_final_summary(cursor)
        
        print("\n✅ Proceso completado exitosamente")
        
    except pyodbc.Error as db_error:
        print(f"❌ Error de base de datos: {db_error}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        sys.exit(1)
        
    finally:
        # Cerrar conexiones
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print(f"⏰ Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

def create_error_table(cursor, conn):
    """Crear tabla para registro de errores"""
    try:
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='failed_inserts')
        CREATE TABLE failed_inserts (
            id INT IDENTITY(1,1) PRIMARY KEY,
            tabla VARCHAR(100),
            datos VARCHAR(500),
            error VARCHAR(500),
            fecha DATETIME DEFAULT GETDATE()
        )
        ''')
        conn.commit()
        print("✅ Tabla de errores verificada")
    except Exception as e:
        print(f"⚠️ Error creando tabla de errores: {e}")

def clean_tables(cursor, conn):
    """Limpiar todas las tablas antes de la nueva carga"""
    print("\n🧹 LIMPIANDO TABLAS EXISTENTES...")
    
    try:
        # Método 1: Deshabilitar FK y usar TRUNCATE
        print("   Método 1: Deshabilitando restricciones FK...")
        cursor.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'")
        
        # Limpiar tablas
        tables_to_clean = ['failed_inserts', 'order_items', 'locations', 'orders', 'products', 'foodtrucks']
        for table in tables_to_clean:
            cursor.execute(f"TRUNCATE TABLE {table}")
        
        # Rehabilitar restricciones
        cursor.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL'")
        conn.commit()
        print("✅ Tablas limpiadas con TRUNCATE")
        
    except Exception as truncate_error:
        print(f"⚠️ Error con TRUNCATE: {truncate_error}")
        print("   Método 2: Usando DELETE...")
        
        try:
            # Plan B: DELETE
            delete_queries = [
                "DELETE FROM order_items",
                "DELETE FROM locations", 
                "DELETE FROM orders",
                "DELETE FROM products",
                "DELETE FROM foodtrucks",
                "DELETE FROM failed_inserts"
            ]
            
            for query in delete_queries:
                cursor.execute(query)
            
            # Reiniciar contadores IDENTITY
            identity_reset = [
                "DBCC CHECKIDENT ('order_items', RESEED, 0)",
                "DBCC CHECKIDENT ('locations', RESEED, 0)",
                "DBCC CHECKIDENT ('orders', RESEED, 0)", 
                "DBCC CHECKIDENT ('products', RESEED, 0)",
                "DBCC CHECKIDENT ('foodtrucks', RESEED, 0)",
                "DBCC CHECKIDENT ('failed_inserts', RESEED, 0)"
            ]
            
            for query in identity_reset:
                try:
                    cursor.execute(query)
                except:
                    pass  # Ignorar si la tabla no tiene IDENTITY
            
            conn.commit()
            print("✅ Tablas limpiadas con DELETE")
            
        except Exception as delete_error:
            print(f"❌ Error también con DELETE: {delete_error}")
            print("⚠️ Continuando sin limpiar tablas...")

def load_all_data(cursor, conn, data_dir):
    """Cargar todos los datos en el orden correcto"""
    print("\n📥 CARGANDO DATOS...")
    
    # Definir orden y configuración de carga
    load_config = [
        {
            'table': 'foodtrucks',
            'file': 'foodtrucks.csv',
            'columns': 'foodtruck_id, name, cuisine_type, city'
        },
        {
            'table': 'products', 
            'file': 'products.csv',
            'columns': 'product_id, foodtruck_id, name, price, stock'
        },
        {
            'table': 'orders',
            'file': 'orders.csv', 
            'columns': 'order_id, foodtruck_id, order_date, status, total'
        },
        {
            'table': 'locations',
            'file': 'locations.csv',
            'columns': 'location_id, foodtruck_id, location_date, zone'
        },
        {
            'table': 'order_items',
            'file': 'order_items.csv',
            'columns': 'order_item_id, order_id, product_id, quantity'
        }
    ]
    
    # Cargar cada tabla
    for config in load_config:
        load_csv_data(cursor, conn, data_dir, config)

def load_csv_data(cursor, conn, data_dir, config):
    """Cargar datos de un archivo CSV específico"""
    table_name = config['table']
    csv_file = config['file'] 
    columns = config['columns']
    
    try:
        file_path = os.path.join(data_dir, csv_file)
        
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {csv_file}")
            return
            
        # Leer CSV
        df = pd.read_csv(file_path, encoding='utf-8')
        total_rows = len(df)
        print(f"\n📊 {table_name.upper()}: {total_rows} registros en {csv_file}")
        
        if total_rows == 0:
            print(f"⚠️ Archivo vacío: {csv_file}")
            return
        
        # Limpiar datos
        df = df.fillna('')
        
        # Contadores
        success_count = 0
        error_count = 0
        
        # Insertar registro por registro
        for index, row in df.iterrows():
            try:
                # Preparar valores
                values = []
                for value in row:
                    if pd.isna(value) or value == '':
                        values.append(None)
                    elif isinstance(value, (int, float)) and pd.notna(value):
                        values.append(value)
                    else:
                        values.append(str(value).strip())
                
                # Crear query de inserción
                placeholders = ', '.join(['?' for _ in values])
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Ejecutar inserción
                cursor.execute(query, tuple(values))
                conn.commit()
                success_count += 1
                
            except Exception as insert_error:
                error_count += 1
                
                # Registrar error
                error_msg = str(insert_error)[:450]
                data_str = str(tuple(values))[:450]
                
                try:
                    cursor.execute(
                        "INSERT INTO failed_inserts (tabla, datos, error) VALUES (?, ?, ?)",
                        (table_name, data_str, error_msg)
                    )
                    conn.commit()
                except:
                    pass  # Si no se puede registrar el error, continuar
        
        # Mostrar resultados
        if success_count > 0:
            print(f"   ✅ {success_count} registros insertados exitosamente")
        if error_count > 0:
            print(f"   ❌ {error_count} registros fallaron")
            
    except Exception as e:
        print(f"❌ Error cargando {csv_file}: {e}")

def show_final_summary(cursor):
    """Mostrar resumen final de la carga"""
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL DE CARGA")
    print("=" * 60)
    
    try:
        cursor.execute('''
        SELECT tabla, registros FROM (
            SELECT 'foodtrucks' as tabla, COUNT(*) as registros, 1 as orden FROM foodtrucks
            UNION ALL SELECT 'products', COUNT(*), 2 FROM products
            UNION ALL SELECT 'orders', COUNT(*), 3 FROM orders  
            UNION ALL SELECT 'order_items', COUNT(*), 4 FROM order_items
            UNION ALL SELECT 'locations', COUNT(*), 5 FROM locations
            UNION ALL SELECT 'failed_inserts', COUNT(*), 6 FROM failed_inserts
        ) t ORDER BY orden
        ''')
        # También agregar un plan alternativo por si hay problemas con subqueries
        results = cursor.fetchall()
        
        # Si no hay resultados, intentar consultas individuales
        if not results:
            individual_queries = [
                ("foodtrucks", "SELECT COUNT(*) FROM foodtrucks"),
                ("products", "SELECT COUNT(*) FROM products"),
                ("orders", "SELECT COUNT(*) FROM orders"),
                ("order_items", "SELECT COUNT(*) FROM order_items"),  
                ("locations", "SELECT COUNT(*) FROM locations"),
                ("failed_inserts", "SELECT COUNT(*) FROM failed_inserts")
            ]
            
            results = []
            for table_name, query in individual_queries:
                try:
                    cursor.execute(query)
                    count = cursor.fetchone()[0]
                    results.append((table_name, count))
                except Exception as e:
                    print(f"Error contando {table_name}: {e}")
                    results.append((table_name, 0))
        total_records = 0
        total_errors = 0
        
        for table, count in results:
            if table == 'failed_inserts':
                total_errors = count
                status = "❌" if count > 0 else "✅"
                print(f"{status} {table:15}: {count:4} errores")
            else:
                total_records += count
                print(f"📊 {table:15}: {count:4} registros")
        
        print("-" * 60)
        print(f"📈 TOTAL REGISTROS: {total_records}")
        print(f"{'❌' if total_errors > 0 else '✅'} TOTAL ERRORES  : {total_errors}")
        
        if total_errors > 0:
            print("\n🔍 Para ver detalles de errores ejecuta:")
            print("   SELECT TOP 10 * FROM failed_inserts ORDER BY fecha DESC")
            
        # Mostrar algunas validaciones básicas
        show_data_validation(cursor)
        
    except Exception as e:
        print(f"❌ Error generando resumen: {e}")

def show_data_validation(cursor):
    """Mostrar validaciones básicas de los datos cargados"""
    print("\n🔍 VALIDACIONES BÁSICAS:")
    print("-" * 40)
    
    validations = [
        ("Foodtrucks únicos", "SELECT COUNT(DISTINCT foodtruck_id) FROM foodtrucks"),
        ("Productos con precio", "SELECT COUNT(*) FROM products WHERE price > 0"),
        ("Órdenes completadas", "SELECT COUNT(*) FROM orders WHERE status = 'completed'"),
        ("Items en órdenes", "SELECT SUM(quantity) FROM order_items")
    ]
    
    for desc, query in validations:
        try:
            cursor.execute(query)
            result = cursor.fetchone()[0]
            print(f"✓ {desc:20}: {result}")
        except:
            print(f"✗ {desc:20}: Error en validación")

if __name__ == "__main__":
    main()