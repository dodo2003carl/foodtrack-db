-- Agregar columna comentarios a la tabla orders
-- Este cambio permite que los clientes dejen comentarios en sus pedidos

ALTER TABLE orders
ADD comentarios VARCHAR(255) NULL;  -- NULL permite que sea opcional

-- Explicación:
-- ALTER TABLE → Comando para modificar una tabla existente
-- ADD → Agrega una nueva columna
-- VARCHAR(255) → Tipo de texto hasta 255 caracteres
-- NULL → La columna puede estar vacía (no es obligatoria)
