"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from productos.views import (
    health_check,
    proveedor_create,
    proveedor_delete,
    proveedor_list,
    proveedor_update,
    categoria_list,
    categoria_create,
    categoria_update,
    categoria_delete,

    #clientes
    cliente_list,
    cliente_create,
    cliente_update,
    cliente_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/', include('productos.urls')),

    # Vistas HTML con formularios (CRUD clasico, sin pasar por la API)
    path('proveedores/', proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', proveedor_delete, name='proveedor_delete'),

    #rutas de categorias
    path('categorias/', categoria_list, name='categoria_list'),
    path('categorias/nuevo/', categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', categoria_delete, name='categoria_delete'),

    #rutas de clientes
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
