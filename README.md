# Sistema de Gestión de Inventario "El Gran Poeta"

Sistema integral para la gestión de inventario, bodegas y ventas para la librería "El Gran Poeta". Este proyecto combina un backend robusto en **Django** con un frontend moderno en **React**, permitiendo una administración eficiente de productos, usuarios y movimientos de stock.

---

## 🚀 Características Principales

*   **Gestión de Inventario**: Control total sobre libros, editoriales y categorización de productos.
*   **Gestión de Bodegas**: Administración de múltiples bodegas y control de stock por ubicación.
*   **Movimientos de Stock**: Registro y trazabilidad de transferencias de productos entre bodegas.
*   **Roles de Usuario**: Perfiles diferenciados para Jefes de Bodega y Bodegueros.
*   **Reportes**: Generación de informes de stock y movimientos.

---

## 🛠 Tecnologías Utilizadas

*   **Backend**: Python, Django, Django REST Framework.
*   **Frontend**: React, Vite, Bootstrap.
*   **Base de Datos**: SQLite (Por defecto para desarrollo).

---

## 💻 Instalación y Configuración

Sigue estos pasos para iniciar el proyecto en tu entorno local.

### Prerrequisitos
*   Node.js y npm
*   Python 3.8+

### 1. Configuración del Backend (Django)

1.  Navega a la carpeta del backend (asumiendo que estás en la raíz del repositorio):
    ```bash
    cd Gestor_Libreria
    ```

2.  Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4.  Realiza las migraciones de base de datos:
    ```bash
    python manage.py migrate
    ```

5.  Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```
    El backend estará corriendo en `http://127.0.0.1:8000/`.

### 2. Configuración del Frontend (React)

1.  Navega a la carpeta del frontend (desde la raíz o en una nueva terminal):
    ```bash
    cd Gestor_Libreria/frontend
    ```

2.  Instala las dependencias de Node:
    ```bash
    npm install
    ```

3.  Inicia el servidor de desarrollo:
    ```bash
    npm run dev
    ```
    La aplicación estará disponible típicamente en `http://localhost:5173/`.

---

## 👥 Roles y Vistas de Usuario

El sistema cuenta con interfaces adaptadas a los distintos roles dentro de la librería.

### 👑 Jefe de Bodega
Tiene acceso completo al sistema de administración.
*   **Dashboard**: Vista general con estadísticas clave y accesos rápidos.
*   **Gestión de Usuarios**: Crear, editar y eliminar cuentas de usuarios (Jefes y Bodegueros).
*   **Bodegas**: Crear y administrar las distintas bodegas físicas de la empresa.
*   **Productos**: Catálogo maestro de libros y editoriales.
*   **Informes**: Acceso a reportes detallados de inventario y auditoría de movimientos.

### 📦 Bodeguero
Centrado en la operativa diaria del almacén.
*   **Movimientos**: Interfaz para registrar entradas, salidas y transferencias de productos.
*   **Consultas**: Verificar disponibilidad de stock en las bodegas asignadas.
*   **Validaciones**: Confirmar recepción de mercancía.

---

## 📦 Módulos del Sistema

### 1. Usuarios (`/Usuarios`)
Módulo de seguridad y administración de personal. Maneja la autenticación, roles y permisos de acceso al sistema. Permite registrar nuevos empleados y asignarles sus funciones correspondientes.

### 2. Bodegas (`/Bodegas`)
Permite la creación lógica de los espacios de almacenamiento. Cada bodega tiene un identificador único y se le pueden asignar productos. Es fundamental para la trazabilidad de la mercancía.

### 3. Productos (`/Libros`, `/Editoriales`)
El corazón del inventario.
*   **Libros**: Fichas detalladas con ISBN, título, autor, precio y stock actual.
*   **Editoriales**: Gestión de proveedores/editoriales para categorizar los libros.

### 4. Movimientos (`/Movimientos`)
Registra cada cambio en el stock. Ya sea una nueva compra (entrada), una venta (salida) o una reorganización interna (transferencia). Cada movimiento genera un comprobante digital para auditoría.

### 5. Informes
Herramientas de inteligencia de negocios para visualizar:
*   Stock total valorizado.
*   Productos con bajo stock (alertas).
*   Historial de movimientos por fecha o usuario.

---

## 📄 Licencia
Este proyecto fue desarrollado con fines educativos para el curso "Taller de Aplicaciones" de INACAP.
