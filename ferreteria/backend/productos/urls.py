from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, ProductoViewSet
from .views import (
    proveedor_list, 
    proveedor_create, 
    proveedor_update,
    proveedor_delete,
    categoria_list,
    categoria_create,
    categoria_update,
    categoria_delete
)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),

    #cosas de proveedores
    path('proveedores/', proveedor_list, name='proveedor_list'),
    path('proveedores/create/', proveedor_create, name='proveedor_create'),
    path('proveedores/update/<int:pk>/', proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', proveedor_delete, name='proveedor_delete'),

    #rutas de categorias
    path('categorias/', categoria_list, name='categoria_list'),
    path('categorias/create/', categoria_create, name='categoria_create'),
    path('categorias/update/<int:pk>/', categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', categoria_delete, name='categoria_delete')
]