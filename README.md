# 🧮 Sistema de Ventas y Cálculo de Comisiones — *minicore*

![Django](https://img.shields.io/badge/Django-5.2.x-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render)

> **minicore** es una aplicación web desarrollada con **Django** que permite registrar ventas, gestionar vendedores y calcular automáticamente las comisiones obtenidas en función de reglas de negocio configurables.

🌐 **Demo en producción:**  
👉 [https://minicore-project.onrender.com](https://minicore-project.onrender.com)

---

## 🧠 Descripción General

El sistema está diseñado para llevar el control de ventas individuales y calcular comisiones basadas en metas de venta.  
Ofrece un panel simple y funcional donde se pueden:

- Registrar vendedores y ventas.
- Configurar reglas de comisión (% por meta de venta alcanzada).
- Calcular automáticamente las comisiones dentro de un rango de fechas.
- Visualizar el resumen de resultados por vendedor.

---

## 🏗️ Arquitectura

La aplicación sigue una arquitectura **Django MVC** (Model–Template–View), con una capa de servicio para manejar la lógica de negocio.

```
📦 minicore_project/
 ┣ 📂 gestorventas/
 ┃ ┣ 📜 admin.py 
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 forms.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 services.py
 ┃ ┣ 📜 views.py
 ┃ ┣ 📜 tests.py
 ┃ ┗ 📂 templates/
 ┣ 📂 minicore_project/
 ┃ ┣ 📜 asgi.py
 ┃ ┣ 📜 settings.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 wsgi.py
 ┣ 📜 manage.py
 ┣ 📜 procfile.py
 ┣ 📜 db.sqlite3
 ┗ 📜 requirements.txt
```

---

## ⚙️ Tecnologías utilizadas

| Componente | Versión | Descripción |
|-------------|----------|-------------|
| **Python** | 3.11+ | Lenguaje principal |
| **Django** | 5.2.x | Framework backend |
| **SQLite** | — | Base de datos |
| **Bootstrap 5** | — | Framework CSS para UI |
| **WhiteNoise** | 6.x | Servir archivos estáticos en producción |
| **Gunicorn** | 23.x | Servidor WSGI para despliegue |
| **Render.com** | — | Plataforma de hosting en la nube |

---

## 🚀 Despliegue en producción

El proyecto está actualmente desplegado en Render:
> 🌍 **https://minicore-project.onrender.com**

Para reproducirlo localmente:

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Vik-tor39/minicore_project.git
cd minicore_project
```
### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4️⃣ Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5️⃣ Cargar el servidor
```bash
python manage.py runserver
```
Ahora se podrá acceder en:
👉 http://localhost:8000

---

## 💰 Lógica de Cálculo de Comisiones
- El usuario selecciona un rango de fechas y (opcionalmente) un vendedor.
- Se suman las ventas realizadas en ese periodo.
- Se identifica la regla de comisión más alta cuya meta sea menor o igual al total de ventas.
- Se aplica el porcentaje de comisión definido en esa regla:
   
    ```python
    bono = ventas_totales * (porcentaje_comision / 100)
    ```
- El sistema genera una tabla resumen con: Nombre del vendedor
    - Ventas totales
    - Meta alcanzada
    - % de comisión
    - Bono final calculado

--- 

## 🧑‍💻 Rutas principales

| Ruta | Descripción |
|-------------|-------------|
| **/** | Página de inicio |
| **/admin/** | Panel administrativo de django |
| **/registrar_venta/** | Formulario para registrar ventas |
| **/calcular_comisiones/** | Cálculo de comisiones por vendedor |
| **/ventas_exito/** | Confirmación de registro exitoso |

---

## 🧱 Estructura de los modelos
```python
class VendedorModel(models.Model):
    nombreVendedor = models.CharField(...)
    apellidoVendedor = models.CharField(...)

class VentasModel(models.Model):
    vendedorId = models.ForeignKey(VendedorModel)
    cantidadVenta = models.DecimalField(...)
    fechaVenta = models.DateField(...)

class ReglasModel(models.Model):
    metaVenta = models.DecimalField(...)
    cantidadComision = models.DecimalField(...) 
```

---

## 🛠️ Archivos clave del despliegue
> procfile
```makefile
web: gunicorn minicore_project.wsgi
```
> requirements.txt
```php
asgiref==3.10.0
dj-database-url==3.0.1
Django==5.2.7
gunicorn==23.0.0
packaging==25.0
psycopg2-binary==2.9.11
sqlparse==0.5.3
tzdata==2025.2
whitenoise==6.11.0
```

---

## 🎥 Video demostrativo
[![Ver demostración breve del proyecto](https://img.youtube.com/vi/GJ4i0VVl1cw/hqdefault.jpg)](https://www.youtube.com/watch?v=GJ4i0VVl1cw)

---

## 👤 Autor

**Víctor Suquilanda**  
📧 Ing. Software Student | Proyecto Minicore  
📅 Año: 2025    

---