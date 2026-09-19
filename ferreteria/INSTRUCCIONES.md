==================================================================
 PROYECTO FERRETERIA - BACKEND (DJANGO) + FRONTEND (HTML/CSS/JS)
==================================================================

ESTADO ACTUAL
-------------
Ya quedo todo instalado, configurado y CORRIENDO en esta maquina:
  - Backend Django:  http://127.0.0.1:8000/
  - Frontend:        http://127.0.0.1:5500/

Si reinicias el computador o cierras las terminales, los servidores
se detienen. Mas abajo esta como volver a levantarlos.


ESTRUCTURA DE CARPETAS
-----------------------
ferreteria/
|
|-- backend/                   -> Proyecto Django (API REST)
|   |-- venv/                  -> Entorno virtual de Python (NO subir a git)
|   |-- config/                -> Configuracion del proyecto Django
|   |   |-- settings.py
|   |   |-- urls.py
|   |-- productos/             -> App de ejemplo (modelos, API, admin)
|   |   |-- models.py          -> Modelos Categoria y Producto
|   |   |-- serializers.py     -> Serializers de DRF
|   |   |-- views.py           -> ViewSets + health check
|   |   |-- urls.py            -> Rutas de la app
|   |   |-- admin.py           -> Registro en el panel /admin
|   |-- manage.py
|   |-- requirements.txt       -> Dependencias de Python
|   |-- .env                   -> Variables de entorno (NO subir a git)
|   |-- .env.example           -> Plantilla de variables de entorno
|   |-- .gitignore
|   |-- db.sqlite3             -> Base de datos (se crea automaticamente)
|
|-- frontend/                  -> Sitio estatico responsivo (Bootstrap 5)
|   |-- index.html
|   |-- css/
|   |   |-- style.css
|   |-- js/
|   |   |-- app.js             -> Consume la API de Django (fetch)
|   |-- img/                   -> Coloca aqui tus imagenes
|
|-- INSTRUCCIONES.txt          -> Este archivo


BACKEND: QUE SE HIZO
---------------------
1. Se creo un entorno virtual en backend/venv
2. Se instalaron:
   - Django 6.1
   - djangorestframework  (API REST)
   - django-cors-headers  (permite que el frontend consuma la API)
   - django-filter        (filtros en la API, ej: ?categoria=1)
   - python-decouple       (variables de entorno via .env)
   - Pillow                (necesario para subir imagenes de productos)
3. Se creo el proyecto Django "config" y la app "productos" con:
   - Modelo Categoria (id, nombre)
   - Modelo Producto (nombre, descripcion, precio, stock, categoria,
     imagen, activo, fechas)
4. Se configuro CORS, archivos media (imagenes subidas) y DRF.
5. Se corrieron las migraciones (makemigrations + migrate).
6. Se creo un superusuario para entrar al panel de administracion:
       usuario:  admin
       correo:   admin@ferreteria.com
       clave:    admin1234
   *** CAMBIA ESTA CLAVE cuando el proyecto sea real ***


ENDPOINTS DISPONIBLES (backend)
--------------------------------
  http://127.0.0.1:8000/admin/                -> Panel de administracion
  http://127.0.0.1:8000/api/health/            -> Verifica que la API responde
  http://127.0.0.1:8000/api/productos/         -> Lista/crea productos (GET, POST)
  http://127.0.0.1:8000/api/productos/<id>/    -> Detalle/edita/borra un producto
  http://127.0.0.1:8000/api/categorias/        -> Lista/crea categorias

  Filtros de ejemplo:
  http://127.0.0.1:8000/api/productos/?categoria=1
  http://127.0.0.1:8000/api/productos/?search=martillo


COMO VOLVER A LEVANTAR EL BACKEND (si se cerro la terminal)
-------------------------------------------------------------
1. Abrir PowerShell en la carpeta:
   cd "C:\Users\Admin\Desktop\clases desarrollo movil\proyecto_responsive\ferreteria\backend"

2. Activar el entorno virtual:
   .\venv\Scripts\Activate.ps1

   (si da error de permisos de ejecucion de scripts, correr una vez:
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
    y confirmar con "S")

3. Levantar el servidor:
   python manage.py runserver

4. Dejar esa ventana abierta. El backend queda en:
   http://127.0.0.1:8000/


COMO VOLVER A LEVANTAR EL FRONTEND
------------------------------------
Opcion A (rapida, con Python, en otra terminal):
   cd "C:\Users\Admin\Desktop\clases desarrollo movil\proyecto_responsive\ferreteria\frontend"
   python -m http.server 5500

   Abrir en el navegador: http://127.0.0.1:5500/

Opcion B (con la extension "Live Server" de VS Code):
   Clic derecho sobre frontend/index.html -> "Open with Live Server"

IMPORTANTE: no abras index.html haciendo doble clic (file://...), porque
el navegador bloquea las peticiones a la API por CORS. Sirvelo siempre
con un servidor (Opcion A o B) en el puerto 5500 (o 3000/5501, y luego
agrega ese puerto en backend/.env, variable CORS_ALLOWED_ORIGINS).


SI QUIERES REINSTALAR TODO DESDE CERO
----------------------------------------
1. cd backend
2. python -m venv venv
3. .\venv\Scripts\Activate.ps1
4. pip install -r requirements.txt
5. copy .env.example a .env  (y ajusta los valores si hace falta)
6. python manage.py migrate
7. python manage.py createsuperuser   (te pedira usuario/correo/clave)
8. python manage.py runserver


AGREGAR PRODUCTOS DE PRUEBA
-----------------------------
1. Ve a http://127.0.0.1:8000/admin/
2. Entra con admin / admin1234
3. Crea una Categoria (ej: "Herramientas manuales")
4. Crea un Producto asociado a esa categoria
5. Recarga http://127.0.0.1:5500/ y el producto debe aparecer
   automaticamente en la seccion "Nuestros productos" (el frontend
   ya consume la API en frontend/js/app.js).


NOTAS / SIGUIENTES PASOS (a criterio tuyo)
---------------------------------------------
- El frontend es HTML + CSS + JS puro (Bootstrap 5 via CDN) para que
  puedas seguir agregando paginas/secciones facilmente. Si prefieres
  usar React, Vue o similar, la carpeta frontend/ es el lugar donde
  debe vivir ese proyecto (backend y frontend quedan totalmente
  separados e independientes).
- Antes de subir esto a produccion: cambia SECRET_KEY, DEBUG=False,
  ALLOWED_HOSTS y la contrasena del superusuario en backend/.env.
- No subir a git: backend/venv/, backend/.env, backend/db.sqlite3,
  backend/media/  (ya estan en el .gitignore).
==================================================================
