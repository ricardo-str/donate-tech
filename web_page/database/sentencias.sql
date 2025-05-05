-- Crear usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;

-- Ver permisos
SHOW GRANTS FOR 'cc5002'@'localhost';