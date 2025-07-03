from services.auth_service import create_usuario

# Crea un admin
create_usuario("admin", "admin123", "Administrador")

# Crea un cliente
create_usuario("Daniel", "daramosss", "Cliente")

print("✅ Usuarios creados correctamente.")
