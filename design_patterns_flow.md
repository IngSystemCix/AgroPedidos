# 🎯 Análisis de Patrones de Diseño en AgroPedidos

## 📑 Índice
- [1. Patrones Creacionales](#1-patrones-creacionales)
- [2. Patrones Estructurales](#2-patrones-estructurales)
- [3. Patrones de Comportamiento](#3-patrones-de-comportamiento)
- [4. Patrones Arquitectónicos](#4-patrones-arquitectónicos)
- [5. Diagramas de Flujo](#5-diagramas-de-flujo)
- [6. Métricas y Análisis](#6-métricas-y-análisis)

---

## 1. Patrones Creacionales

### 1.1 Factory Method Pattern

**📍 Ubicación Principal:** `services/product_service.py`

**🔍 Implementación:**
```python
class Product:
    def __init__(self, row):
        self.id, self.name, self.price, self.unit, self.stock, self.image_url = row

def get_all_products():
    # ... código de base de datos ...
    return [Product(row) for row in rows]  # Factory Method
```

**📊 Archivos Involucrados:**
- `services/product_service.py` (Factory principal)
- `views/product_catalog.py` (Consumidor)
- `views/catalogo_admin_view.py` (Consumidor)
- `views/inventario_view.py` (Consumidor)

**🌊 Flujo de Ejecución:**
1. Vista solicita productos → `get_all_products()`
2. Servicio consulta BD → obtiene raw data
3. Factory Method → `Product(row)` para cada fila
4. Retorna lista de objetos Product tipados
5. Vista consume objetos con interfaz uniforme

**🎯 Ventajas Implementadas:**
- ✅ Encapsula creación de objetos Product
- ✅ Consistencia en la estructura de datos
- ✅ Fácil extensión para nuevos tipos de productos

---

### 1.2 Builder Pattern (Parcial)

**📍 Ubicación Principal:** `views/cart_modal.py`, `views/agregar_producto_view.py`

**🔍 Implementación:**
```python
class CartModal(CTkToplevel):
    def __init__(self, master, carrito, total, reset_callback, usuario):
        # ... inicialización ...
        self.render_ui()  # Builder step 1
        
    def render_ui(self):
        # ... construcción base ...
        self.render_items()    # Builder step 2
        self.render_inputs()   # Builder step 3
```

**📊 Archivos Involucrados:**
- `views/cart_modal.py` (Builder complejo)
- `views/agregar_producto_view.py` (Builder de formularios)
- `views/editar_producto_view.py` (Builder de formularios)
- `views/login.py` (Builder simple)

**🌊 Flujo de Ejecución:**
1. Constructor inicializa estado base
2. `render_ui()` → estructura principal
3. `render_items()` → componentes dinámicos
4. `render_inputs()` → inputs específicos por contexto
5. UI completa y funcional

**🎯 Ventajas Implementadas:**
- ✅ Construcción paso a paso de UIs complejas
- ✅ Separación clara de responsabilidades de construcción
- ✅ Reutilización de pasos de construcción

---

## 2. Patrones Estructurales

### 2.1 Facade Pattern

**📍 Ubicación Principal:** `services/auth_service.py`, `services/product_service.py`

**🔍 Implementación:**
```python
# auth_service.py - Facade de autenticación
def authenticate(username: str, password: str):
    # Simplifica: hash_password + BD query + validation
    hashed = hash_password(password)
    conn = get_connection()
    # ... lógica compleja simplificada ...
    return usuario

# product_service.py - Facade de productos  
def add_product(name, price, unit, stock, image_url, usuario_id):
    # Simplifica: validación + BD insert + manejo errores
    conn = get_connection()
    # ... operación compleja simplificada ...
```

**📊 Archivos Involucrados:**
- `services/auth_service.py` (Facade principal)
- `services/product_service.py` (Facade principal)
- `services/order_service.py` (Facade principal)
- `config/connection.py` (Subsistema)
- `utils/security.py` (Subsistema)

**🌊 Flujo de Ejecución:**
1. Vista llama método Facade simple
2. Facade coordina múltiples subsistemas
3. Manejo de BD + validación + seguridad
4. Retorna resultado simplificado
5. Vista recibe respuesta uniforme

**🎯 Ventajas Implementadas:**
- ✅ Simplifica operaciones complejas multi-sistema
- ✅ Oculta complejidad de BD y validaciones
- ✅ API uniforme para las vistas

---

### 2.2 Composite Pattern

**📍 Ubicación Principal:** Todas las vistas en `views/`

**🔍 Implementación:**
```python
class ProductCatalogView(ctk.CTkFrame):  # Composite
    def create_widgets(self):
        HeaderUser(self, ...)          # Component
        SearchBar(self, ...)           # Component
        # ... más componentes ...
        ProductCard(...)               # Component (leaf)
```

**📊 Archivos Involucrados:**
- `views/product_catalog.py` (Composite principal)
- `views/header_user.py` (Component)
- `views/search_bar.py` (Component)
- `views/product_card.py` (Leaf)
- `views/cart_modal.py` (Composite secundario)

**🌊 Flujo de Ejecución:**
1. Vista principal (Composite) se inicializa
2. Crea componentes hijos (Components/Leafs)
3. Cada componente maneja su propia lógica
4. Composite coordina interacciones entre componentes
5. Estructura jerárquica de UI funcional

**🎯 Ventajas Implementadas:**
- ✅ Estructura jerárquica clara de UI
- ✅ Reutilización de componentes
- ✅ Fácil mantenimiento por modularidad

---

### 2.3 Decorator Pattern (Técnico)

**📍 Ubicación Principal:** `models/` con SQLAlchemy

**🔍 Implementación:**
```python
class Order(Base):
    __tablename__ = "Order"  # Decorator implícito
    id = Column(Integer, primary_key=True)  # Decorator
    usuario_id = Column(Integer, ForeignKey("Usuario.id"))  # Decorator
```

**📊 Archivos Involucrados:**
- `models/order.py` (Decoradores SQLAlchemy)
- `models/product.py` (Decoradores SQLAlchemy)
- `models/usuario.py` (Decoradores SQLAlchemy)
- `models/order_item.py` (Decoradores SQLAlchemy)

**🌊 Flujo de Ejecución:**
1. Definición de clase con decoradores SQLAlchemy
2. Column() agrega funcionalidad de mapeo BD
3. ForeignKey() agrega funcionalidad de relaciones
4. Base agrega funcionalidad ORM
5. Objeto con comportamiento extendido sin modificar código original

---

## 3. Patrones de Comportamiento

### 3.1 Observer Pattern

**📍 Ubicación Principal:** `views/product_catalog.py`

**🔍 Implementación:**
```python
class ProductCatalogView(ctk.CTkFrame):
    def start_stock_updater(self):
        self.update_stocks()  # Observar cambios
        self.after(500, self.start_stock_updater)  # Auto-re-observación
        
    def update_stocks(self):
        updated_products = get_all_products()  # Consultar estado
        for card in self.product_cards:
            card.update_stock_display(new_stock)  # Notificar cambios
```

**📊 Archivos Involucrados:**
- `views/product_catalog.py` (Observer + Subject)
- `views/product_card.py` (Observer)
- `services/product_service.py` (Data source)

**🌊 Flujo de Ejecución:**
1. `start_stock_updater()` inicia ciclo de observación
2. Cada 500ms consulta estado actual del stock
3. Compara con estado anterior
4. Notifica cambios a ProductCards
5. ProductCards actualizan su display
6. Ciclo se repite automáticamente

**🎯 Ventajas Implementadas:**
- ✅ Actualización automática de UI en tiempo real
- ✅ Desacoplamiento entre fuente de datos y UI
- ✅ Respuesta reactiva a cambios de estado

---

### 3.2 Strategy Pattern

**📍 Ubicación Principal:** `views/cart_modal.py`

**🔍 Implementación:**
```python
def render_inputs(self, *_):
    if self.metodo_pago.get() == "Tarjeta":
        # Estrategia de Tarjeta
        self.tarjeta_inputs["numero"] = CTkEntry(...)
        self.tarjeta_inputs["fecha"] = CTkEntry(...)
        self.tarjeta_inputs["cvv"] = CTkEntry(...)
    else:
        # Estrategia de Yape
        self.yape_inputs["numero"] = CTkEntry(...)
        self.yape_inputs["codigo"] = CTkEntry(...)

def validar_datos(self):
    if self.metodo_pago.get() == "Tarjeta":
        # Algoritmo de validación para tarjeta
        # ... validación específica ...
    else:
        # Algoritmo de validación para Yape
        # ... validación específica ...
```

**📊 Archivos Involucrados:**
- `views/cart_modal.py` (Context + Strategies)
- `models/enums.py` (Strategy identifiers)

**🌊 Flujo de Ejecución:**
1. Usuario selecciona método de pago (Strategy)
2. `render_inputs()` aplica estrategia de UI correspondiente
3. Usuario ingresa datos según estrategia
4. `validar_datos()` aplica algoritmo de validación específico
5. `guardar_pedido()` usa estrategia seleccionada

**🎯 Ventajas Implementadas:**
- ✅ Algoritmos intercambiables sin modificar código cliente
- ✅ Fácil adición de nuevos métodos de pago
- ✅ Validaciones específicas por estrategia

---

### 3.3 Command Pattern

**📍 Ubicación Principal:** Múltiples vistas con callbacks

**🔍 Implementación:**
```python
# product_card.py
class ProductCard:
    def __init__(self, parent, product, row, col, add_to_cart_callback):
        # ... 
        CTkButton(
            command=lambda: add_to_cart_callback(product, quantity)  # Command
        )

# product_catalog.py
def agregar_al_carrito(self, producto, cantidad):  # Command implementation
    # ... lógica de agregar al carrito ...
```

**📊 Archivos Involucrados:**
- `views/product_card.py` (Command invoker)
- `views/product_catalog.py` (Command receiver)
- `views/cart_modal.py` (Command receiver)
- Múltiples callbacks en diferentes vistas

**🌊 Flujo de Ejecución:**
1. Vista crea callback (Command object)
2. Pasa callback a componente hijo
3. Componente almacena referencia al comando
4. Evento trigger ejecuta comando
5. Comando se ejecuta en contexto original

**🎯 Ventajas Implementadas:**
- ✅ Desacoplamiento entre invoker y receiver
- ✅ Callbacks reutilizables
- ✅ Flexibilidad en manejo de eventos

---

### 3.4 State Pattern (Implícito)

**📍 Ubicación Principal:** `main.py`

**🔍 Implementación:**
```python
def show_view(self, view_name):
    if self.usuario.rol == "Administrador":  # State check
        views = {
            "catalogo": CatalogoAdminView,      # Admin state behavior
            "gestion": GestionProductosView,
            "inventario": InventarioView,
            # ...
        }
    else:  # Cliente state
        views = {
            "catalogo": ProductCatalogView      # Client state behavior
        }
```

**📊 Archivos Involucrados:**
- `main.py` (State context)
- `models/usuario.py` (State data)
- `views/catalogo_admin_view.py` (Admin state)
- `views/product_catalog.py` (Client state)

**🌊 Flujo de Ejecución:**
1. Usuario autenticado con rol específico (State)
2. `show_view()` verifica estado actual del usuario
3. Selecciona conjunto de vistas según estado
4. Instancia vista apropiada para el estado
5. Comportamiento diferente según estado del usuario

---

### 3.5 Template Method Pattern

**📍 Ubicación Principal:** Todas las vistas que heredan de CTkFrame

**🔍 Implementación:**
```python
# Template en clases base
class SomeView(ctk.CTkFrame):
    def __init__(self, master, usuario, navigate):  # Template step 1
        super().__init__(master)
        self.configure_base()                       # Template step 2  
        self.create_widgets()                       # Template step 3 (abstract)
        
    def create_widgets(self):  # Abstract method - implementado por subclases
        raise NotImplementedError
```

**📊 Archivos Involucrados:**
- `views/login.py` (Template implementation)
- `views/product_catalog.py` (Template implementation)
- `views/cart_modal.py` (Template implementation)
- Todas las vistas con `create_widgets()`

**🌊 Flujo de Ejecución:**
1. Constructor base ejecuta template común
2. `configure()` → configuración estándar
3. `create_widgets()` → implementación específica por subclase
4. Patrón común de inicialización garantizado
5. Flexibilidad en implementación específica

---

## 4. Patrones Arquitectónicos

### 4.1 Repository Pattern (Simplificado)

**📍 Ubicación Principal:** `services/`

**🔍 Implementación:**
```python
# Abstracto repository en services
def get_all_products():      # Repository method
def get_product_by_id():     # Repository method  
def add_product():           # Repository method
def update_product():        # Repository method
def delete_product():        # Repository method
```

**📊 Archivos Involucrados:**
- `services/product_service.py` (Product repository)
- `services/auth_service.py` (User repository)
- `services/order_service.py` (Order repository)
- `config/connection.py` (Data access)

**🌊 Flujo de Ejecución:**
1. Vista solicita datos → Repository method
2. Repository maneja acceso a BD
3. Abstrae detalles de SQL y conexión
4. Retorna objetos de dominio
5. Vista consume datos sin conocer implementación

---

### 4.2 MVC Pattern (Variante)

**📍 Ubicación:** Arquitectura general

**🔍 Implementación:**
- **Model:** `models/` (Entidades de dominio)
- **View:** `views/` (Interfaces de usuario)  
- **Controller:** `services/` + navegación en `main.py`

**📊 Archivos Involucrados:**
- Models: `models/usuario.py`, `models/product.py`, `models/order.py`
- Views: Todos los archivos en `views/`
- Controllers: Todos los archivos en `services/` + `main.py`

**🌊 Flujo de Ejecución:**
1. Vista captura entrada usuario
2. Llama a Controller (service)
3. Controller procesa lógica de negocio
4. Controller interactúa con Model
5. Controller retorna resultado a Vista
6. Vista actualiza presentación

---

### 4.3 Dependency Injection (Manual)

**📍 Ubicación Principal:** Constructores en `views/`

**🔍 Implementación:**
```python
class ProductCatalogView(ctk.CTkFrame):
    def __init__(self, master, usuario, navigate):  # DI
        self.usuario = usuario      # Injected dependency
        self.navigate = navigate    # Injected dependency
```

**📊 Archivos Involucrados:**
- `main.py` (DI container)
- Todas las vistas (DI consumers)
- `services/` (DI consumers)

**🌊 Flujo de Ejecución:**
1. `main.py` actúa como DI container
2. Crea dependencias (usuario, navigate function)
3. Inyecta en constructores de vistas
4. Vistas usan dependencias sin crearlas
5. Flexibilidad y testabilidad mejorada

---

## 5. Diagramas de Flujo

### 5.1 Flujo Principal de Autenticación

```
Usuario → LoginView → auth_service.authenticate()
    ↓
security.hash_password() → BD Query → Usuario Object
    ↓
main.start_main_app() → create_menu() → show_view()
    ↓
State Pattern: Admin vs Cliente → Vista específica
```

### 5.2 Flujo de Agregar al Carrito

```
ProductCard → Command(add_to_cart_callback)
    ↓
ProductCatalogView.agregar_al_carrito()
    ↓
Strategy: Validación de stock → Actualización carrito
    ↓
Observer: update UI → mostrar_boton_carrito()
```

### 5.3 Flujo de Realizar Pedido

```
CartModal → Strategy Pattern: Método pago
    ↓
render_inputs() → validar_datos()
    ↓
Repository: guardar_pedido() → BD Transaction
    ↓
Observer: reset_carrito() → UI Update
```

---

## 6. Métricas y Análisis

### 6.1 Distribución de Patrones

| Categoría | Cantidad | Archivos Principales |
|-----------|----------|---------------------|
| Creacionales | 2 | `services/`, `views/cart_modal.py` |
| Estructurales | 3 | `services/`, `views/`, `models/` |
| Comportamiento | 5 | `views/`, `main.py` |
| Arquitectónicos | 3 | Toda la aplicación |

### 6.2 Complejidad por Patrón

| Patrón | Complejidad | Implementación | Beneficio |
|--------|-------------|----------------|-----------|
| Factory Method | Baja | Completa | Alto |
| Observer | Media | Completa | Alto |
| Strategy | Media | Completa | Medio |
| Facade | Baja | Completa | Alto |
| Composite | Media | Completa | Alto |
| State | Baja | Implícita | Medio |
| Template Method | Baja | Completa | Medio |
| Command | Baja | Completa | Medio |

### 6.3 Calidad de Implementación

**✅ Fortalezas:**
- Patrones bien implementados y funcionales
- Separación clara de responsabilidades
- Código reutilizable y mantenible
- Arquitectura escalable

**⚠️ Áreas de Mejora:**
- Algunos patrones podrían ser más explícitos
- Repository pattern podría usar interfaces
- Factory pattern podría ser más abstracto
- Falta documentación de patrones en código

### 6.4 Recomendaciones

1. **Documentar Patrones:** Agregar comentarios explicando patrones
2. **Interfaces Explícitas:** Crear interfaces para Repository pattern
3. **Abstract Factory:** Considerar para creación de familias de objetos
4. **Visitor Pattern:** Para operaciones complejas en estructuras de datos

---

## ✅ Conclusión

AgroPedidos implementa **13 patrones de diseño** de manera efectiva, demostrando una arquitectura madura y bien estructurada. Los patrones están distribuidos equilibradamente entre las tres categorías principales, con una implementación sólida que beneficia la mantenibilidad, escalabilidad y legibilidad del código.

**Calificación de Patrones: 9.0/10**

La aplicación muestra un uso consistente y apropiado de patrones de diseño, contribuyendo significativamente a la calidad arquitectónica general del proyecto.

---

**📅 Fecha de Análisis:** Julio 9, 2025  
**👨‍💻 Analista:** Juan Bladimir Romero Collazos  
**🔍 Metodología:** Análisis estático de código + Inspección arquitectónica
