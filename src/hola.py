import sqlite3

# Nombre de la base de datos
db_path = "attendance_retry.db"

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Nombre de la tabla a eliminar
table_name = "pending_attendance"

# Eliminar la tabla si existe
cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

# Confirmar los cambios y cerrar conexión
conn.commit()
conn.close()

print(f"La tabla '{table_name}' ha sido eliminada correctamente.")
