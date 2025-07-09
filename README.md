# 🌱 AgroPedidos - Sistema de Gestión de Pedidos Agrícolas

## 🧾 Descripción General

**AgroPedidos** es una aplicación de escritorio desarrollada en Python que facilita la gestión integral de pedidos de productos agrícolas. El sistema está diseñado para pequeñas y medianas empresas del sector agrícola que necesitan administrar su inventario, procesar pedidos de clientes y generar reportes de ventas de manera eficiente.

La aplicación cuenta con dos tipos de usuarios: **Administradores** (que gestionan productos, inventario y ventas) y **Clientes** (que pueden explorar el catálogo y realizar pedidos). Resuelve el problema de la gestión manual de inventarios agrícolas, automatizando procesos de compra, control de stock y generación de reportes.

**Tipo de aplicación:** Aplicación de escritorio con interfaz gráfica moderna (GUI Desktop)

## 🛠️ Tecnologías Utilizadas

### **Lenguaje Principal**
- **Python 3.x** - Lenguaje de programación principal

### **Interfaz Gráfica**
- **CustomTkinter** - Framework moderno para interfaces gráficas de escritorio
- **Tkinter** - Biblioteca estándar de Python para GUI (base de CustomTkinter)
- **PIL/Pillow** - Procesamiento y manipulación de imágenes

### **Base de Datos**
- **MySQL** - Sistema de gestión de base de datos relacional
- **SQLAlchemy** - ORM (Object-Relational Mapping) para Python
- **mysql-connector-python** - Conector directo para MySQL

### **Manejo de Datos**
- **pandas** - Análisis y manipulación de datos, exportación a Excel
- **openpyxl** - Lectura y escritura de archivos Excel con estilos
- **xml.etree.ElementTree** - Procesamiento y generación de archivos XML

### **Seguridad**
- **hashlib** - Encriptación de contraseñas con SHA-256

## 📁 Estructura del Proyecto

```
AgroPedidos/
├── 📁 models/                    # Modelos de datos (Entidades ORM)
│   ├── usuario.py               # Modelo de usuarios (Cliente/Admin)
│   ├── product.py               # Modelo de productos agrícolas
│   ├── order.py                 # Modelo de pedidos
│   ├── order_item.py            # Modelo de items de pedido
│   ├── notification.py          # Modelo de notificaciones
│   └── enums.py                 # Enumeraciones (métodos de pago, estados)
├── 📁 views/                     # Interfaz de usuario (Capa de presentación)
│   ├── login.py                 # Vista de autenticación
│   ├── register_view.py         # Vista de registro de usuarios
│   ├── product_catalog.py       # Catálogo de productos (Cliente)
│   ├── catalogo_admin_view.py   # Catálogo de productos (Admin)
│   ├── cart_modal.py            # Modal del carrito de compras
│   ├── gestion_productos_view.py # Gestión CRUD de productos
│   ├── inventario_view.py       # Vista de inventario y reportes
│   ├── ventas_view.py           # Vista de ventas y exportación
│   ├── detalle_pedido_view.py   # Detalle de pedidos individuales
│   ├── agregar_producto_view.py # Formulario agregar producto
│   ├── editar_producto_view.py  # Formulario editar producto
│   ├── product_card.py          # Componente tarjeta de producto
│   ├── search_bar.py            # Componente barra de búsqueda
│   └── header_user.py           # Componente encabezado de usuario
├── 📁 services/                  # Lógica de negocio (Capa de servicios)
│   ├── auth_service.py          # Servicio de autenticación
│   ├── product_service.py       # Servicio de productos
│   └── order_service.py         # Servicio de pedidos
├── 📁 config/                    # Configuración y conexiones
│   └── connection.py            # Configuración de base de datos
├── 📁 utils/                     # Utilidades compartidas
│   └── security.py              # Funciones de seguridad y encriptación
├── 📁 resources/                 # Recursos estáticos
│   └── images/                  # Imágenes de productos y logos
├── main.py                      # Punto de entrada de la aplicación
├── seed_products.py             # Script para poblar productos iniciales
├── create_user.py               # Script para crear usuarios iniciales
├── requirements.txt             # Dependencias del proyecto
├── diagram_class.puml           # Diagrama de clases UML
├── architecture.txt             # Documentación de arquitectura
└── README.md                    # Documentación del proyecto
```

## ✨ Funcionalidades Principales

### **👤 Para Clientes:**
- **Autenticación segura** - Login y registro con contraseñas encriptadas
- **Catálogo de productos** - Exploración visual de productos agrícolas disponibles
- **Búsqueda inteligente** - Filtrado de productos por nombre
- **Carrito de compras** - Gestión de productos seleccionados con validación de stock
- **Procesamiento de pedidos** - Múltiples métodos de pago (Tarjeta/Yape)
- **Validación en tiempo real** - Control de stock durante la compra

### **🔧 Para Administradores:**
- **Panel de administración** - Interfaz dedicada para gestión completa
- **Gestión de productos** - CRUD completo (Crear, Leer, Actualizar, Eliminar)
- **Control de inventario** - Monitoreo de stock con alertas visuales
- **Gestión de ventas** - Visualización y seguimiento de todos los pedidos
- **Reportes y exportación** - Generación de reportes en Excel y XML
- **Análisis de datos** - Estados de stock (Disponible, Bajo, Agotado)

### **📊 Características Técnicas:**
- **Actualización en tiempo real** - Stock actualizado automáticamente
- **Interfaz moderna** - Diseño intuitivo con CustomTkinter
- **Validaciones robustas** - Control de datos de entrada y stock
- **Exportación múltiple** - Reportes en formatos Excel y XML
- **Gestión de imágenes** - Soporte para imágenes de productos
- **Arquitectura escalable** - Patrón de capas bien definido

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- Python 3.8 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

### **Paso 1: Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd AgroPedidos
```

### **Paso 2: Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 3: Configurar base de datos**
1. Crear base de datos MySQL:
```sql
CREATE DATABASE agropedidos_db;
```

2. Configurar conexión en `config/connection.py`:
```python
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "agropedidos_db"
```

### **Paso 4: Poblar datos iniciales**
```bash
# Crear usuarios de prueba
python create_user.py

# Poblar productos de prueba
python seed_products.py
```

### **Paso 5: Ejecutar la aplicación**
```bash
python main.py
```

## 👥 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| Daniel | daramosss | Cliente |

## 🏗️ Arquitectura del Sistema

El proyecto implementa una **Arquitectura en Capas (Layered Architecture)** con las siguientes características:

- **Capa de Presentación** (`views/`) - Manejo de la interfaz de usuario
- **Capa de Servicios** (`services/`) - Lógica de negocio y validaciones  
- **Capa de Modelos** (`models/`) - Entidades de dominio y acceso a datos
- **Capa de Configuración** (`config/`, `utils/`) - Configuración y utilidades

### **Patrones de Diseño Implementados:**
- **Factory Method** - Creación de instancias de productos
- **Observer Pattern** - Actualización automática de stock
- **Strategy Pattern** - Múltiples métodos de pago
- **Facade Pattern** - Simplificación de operaciones complejas
- **Repository Pattern** - Abstracción del acceso a datos

## 📖 Uso del Sistema

### **Inicio de Sesión**
1. Ejecutar `python main.py`
2. Ingresar credenciales en la pantalla de login
3. El sistema redirige según el rol del usuario

### **Flujo Cliente**
1. **Explorar catálogo** - Ver productos disponibles
2. **Buscar productos** - Usar la barra de búsqueda
3. **Agregar al carrito** - Seleccionar productos y cantidades
4. **Procesar pago** - Elegir método de pago y completar pedido

### **Flujo Administrador**
1. **Gestionar productos** - Crear, editar o eliminar productos
2. **Monitorear inventario** - Revisar niveles de stock
3. **Procesar ventas** - Ver detalles de pedidos
4. **Generar reportes** - Exportar datos en Excel/XML

## 🔧 Dependencias Detalladas

```txt
pandas              # Análisis de datos y exportación Excel
openpyxl           # Manipulación avanzada de archivos Excel
customtkinter      # Framework moderno de interfaz gráfica
sqlalchemy         # ORM para manejo de base de datos
pillow             # Procesamiento de imágenes
mysql-connector-python  # Conector MySQL nativo
```

## 🤝 Equipo de Desarrollo

- **Romero Collazos, Juan Bladimir**
- **Ramos Marrufo, Daniel David**  
- **Fupuy Chanamé, Jorge Hugo**
- **Burga Rodríguez, Janluvi Gabdiel**

## 📋 Próximas Mejoras

- [ ] Implementación de sistema de notificaciones
- [ ] Módulo de reportes avanzados con gráficos
- [ ] API REST para integración con otros sistemas
- [ ] Aplicación móvil complementaria
- [ ] Sistema de usuarios con roles personalizados
- [ ] Integración con sistemas de pago reales
- [ ] Módulo de facturación electrónica

## 📄 Licencia

Este proyecto fue desarrollado como parte de un curso académico de Lenguajes de Programación.

---

**Desarrollado con ❤️ usando Python y tecnologías modernas para el sector agrícola**