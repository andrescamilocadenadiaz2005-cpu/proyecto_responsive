# Guía: CRUD con vistas y formularios de Django (agregar / editar / eliminar desde el navegador)

> Esta vez el CRUD **no es la API JSON** (esa ya existe con Django REST
> Framework). Aquí vamos a crear páginas HTML normales, con formularios, para
> poder **agregar, editar y eliminar proveedores directamente desde el
> navegador**, sin Postman ni curl.

Trabajamos sobre la tabla **`Proveedor`**, que ya existe en el proyecto
(`backend/productos/models.py`, ya migrada a MySQL):

```python
class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
```

Las piezas que vamos a construir, en orden:

```
Formulario (forms.py)  →  Vistas (views.py)  →  Templates (HTML)  →  URLs
```

---

## Paso 1 — El formulario (`forms.py`)

Crear el archivo **`backend/productos/forms.py`**:

```python
from django import forms

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    """Formulario para crear/editar un Proveedor.

    ModelForm genera automaticamente un campo de formulario por cada
    campo del modelo que listemos en Meta.fields, con su validacion
    correspondiente (ej. email valida formato de correo).
    """

    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
```

> Los `widgets` solo le agregan clases de Bootstrap a cada campo para que se
> vea presentable. No son obligatorios para que el CRUD funcione.

---

## Paso 2 — Las plantillas HTML (templates)

Django busca las plantillas dentro de `<app>/templates/<app>/`. Crear la
carpeta y los 3 archivos:

```
backend/productos/templates/productos/base.html
backend/productos/templates/productos/proveedor_list.html
backend/productos/templates/productos/proveedor_form.html
backend/productos/templates/productos/proveedor_confirm_delete.html
```

**`base.html`** (plantilla base, para no repetir el `<html>` en cada página):
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Proveedores{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container py-4">
    {% block content %}{% endblock %}
  </div>
</body>
</html>
```

**`proveedor_list.html`** (la tabla con todos los proveedores — Read):
```html
{% extends "productos/base.html" %}

{% block title %}Proveedores{% endblock %}

{% block content %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Proveedores</h1>
    <a href="{% url 'proveedor-create' %}" class="btn btn-primary">+ Agregar proveedor</a>
  </div>

  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Nombre</th>
        <th>Telefono</th>
        <th>Email</th>
        <th>Activo</th>
        <th style="width: 220px;">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for proveedor in proveedores %}
        <tr>
          <td>{{ proveedor.nombre }}</td>
          <td>{{ proveedor.telefono }}</td>
          <td>{{ proveedor.email }}</td>
          <td>{{ proveedor.activo|yesno:"Si,No" }}</td>
          <td>
            <a href="{% url 'proveedor-update' proveedor.pk %}" class="btn btn-sm btn-outline-secondary">Editar</a>
            <a href="{% url 'proveedor-delete' proveedor.pk %}" class="btn btn-sm btn-outline-danger">Eliminar</a>
          </td>
        </tr>
      {% empty %}
        <tr>
          <td colspan="5" class="text-center text-muted">No hay proveedores registrados todavia.</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

**`proveedor_form.html`** (formulario reutilizado para Create y Update):
```html
{% extends "productos/base.html" %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
  <h1>{{ titulo }}</h1>

  <form method="post" class="mt-3" style="max-width: 500px;">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Guardar</button>
    <a href="{% url 'proveedor-list' %}" class="btn btn-link">Cancelar</a>
  </form>
{% endblock %}
```

> `{% csrf_token %}` es **obligatorio** en todo formulario con `method="post"`
> en Django. Es una protección de seguridad contra ataques CSRF. Sin esa
> línea, Django rechaza el POST con un error 403.

**`proveedor_confirm_delete.html`** (pantalla de confirmación — Delete):
```html
{% extends "productos/base.html" %}

{% block title %}Eliminar proveedor{% endblock %}

{% block content %}
  <h1>Eliminar proveedor</h1>
  <p>Estas seguro de eliminar a <strong>{{ proveedor.nombre }}</strong>?</p>

  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Si, eliminar</button>
    <a href="{% url 'proveedor-list' %}" class="btn btn-link">Cancelar</a>
  </form>
{% endblock %}
```

---

## Paso 3 — Las vistas (`views.py`)

Abrir `backend/productos/views.py`. Agregar estos imports arriba:

```python
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProveedorForm
from .models import Categoria, Producto, Proveedor
```

Y al final del archivo, las 4 funciones (una por cada operación del CRUD):

```python
# --- Vistas con formularios HTML (CRUD "clasico" de Django, sin la API) ---

def proveedor_list(request):
    """Lista todos los proveedores (Read)."""
    proveedores = Proveedor.objects.all()
    return render(request, 'productos/proveedor_list.html', {'proveedores': proveedores})


def proveedor_create(request):
    """Muestra el formulario vacio (GET) y crea el registro (POST) - Create."""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor-list')
    else:
        form = ProveedorForm()
    return render(request, 'productos/proveedor_form.html', {'form': form, 'titulo': 'Agregar proveedor'})


def proveedor_update(request, pk):
    """Muestra el formulario con los datos actuales (GET) y los actualiza (POST) - Update."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor-list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'productos/proveedor_form.html', {'form': form, 'titulo': 'Editar proveedor'})


def proveedor_delete(request, pk):
    """Pide confirmacion (GET) y elimina el registro (POST) - Delete."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor-list')
    return render(request, 'productos/proveedor_confirm_delete.html', {'proveedor': proveedor})
```

> Patrón a explicar en clase: **si la petición es GET, muestro el formulario;
> si es POST, valido y guardo**. Es el mismo patrón en `create` y en `update`,
> la única diferencia es si se le pasa `instance=proveedor` (edición) o no
> (creación nueva).

---

## Paso 4 — Las URLs

Abrir `backend/config/urls.py` y agregar el import y las 4 rutas nuevas
(fuera de `/api/`, porque estas son páginas HTML, no la API):

```python
from productos.views import (
    health_check,
    proveedor_create,
    proveedor_delete,
    proveedor_list,
    proveedor_update,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/', include('productos.urls')),

    # Vistas HTML con formularios (CRUD clasico, sin pasar por la API)
    path('proveedores/', proveedor_list, name='proveedor-list'),
    path('proveedores/nuevo/', proveedor_create, name='proveedor-create'),
    path('proveedores/<int:pk>/editar/', proveedor_update, name='proveedor-update'),
    path('proveedores/<int:pk>/eliminar/', proveedor_delete, name='proveedor-delete'),
]
```

---

## Paso 5 — Probarlo en el navegador

Con el backend corriendo (`python manage.py runserver`), abrir:

```
http://127.0.0.1:8000/proveedores/
```

Y desde ahí, todo se hace con clics:

1. **Listar** → la tabla aparece vacía la primera vez.
2. **Agregar** → botón "+ Agregar proveedor" → llenar el formulario → "Guardar"
   → vuelve a la lista y ya aparece la fila nueva.
3. **Editar** → botón "Editar" en una fila → el formulario aparece con los
   datos actuales cargados → cambiar algo → "Guardar".
4. **Eliminar** → botón "Eliminar" → pantalla de confirmación → "Sí, eliminar"
   → la fila desaparece de la lista.

## Paso 6 — Confirmar en MySQL

```sql
USE ferreteria_db;
SELECT * FROM productos_proveedor;
```

Cada clic en "Guardar" o "Sí, eliminar" hace un `INSERT`, `UPDATE` o `DELETE`
real contra esta tabla — se puede dejar esta consulta abierta en otra ventana
y refrescarla después de cada acción en el navegador, para que los
estudiantes vean el cambio en vivo.

---

## Puntos clave para explicar en clase

1. **Esto es un CRUD "clásico" de Django**, distinto del CRUD por API (JSON)
   que ya armamos antes. Aquí Django genera el HTML directamente (server-side
   rendering); en el otro, Django solo devuelve datos y el frontend (HTML/JS
   separado) es quien arma la pantalla.
2. **Un `ModelForm` ahorra código**: valida y guarda el modelo sin escribir
   `if`s campo por campo.
3. **El mismo template de formulario sirve para crear y editar** — la única
   diferencia es si el `ProveedorForm` recibe `instance=proveedor` o no.
4. **`{% csrf_token %}` siempre va en formularios POST** — es un tema
   importante de seguridad web para mencionar.
5. Relación con el CRUD anterior: la tabla es la misma (`Proveedor`), lo único
   que cambia es la "capa" que se construye encima: API (JSON) vs. Vistas +
   Templates (HTML).

## Ejercicio para que los estudiantes lo repitan solos

Pídeles que repliquen exactamente este mismo patrón (`forms.py` → `views.py`
→ templates → `urls.py`) para la tabla **`Categoria`**, que es la más
simple del proyecto (un solo campo: `nombre`).
