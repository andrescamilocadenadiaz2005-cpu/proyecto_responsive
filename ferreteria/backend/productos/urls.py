from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, ProductoViewSet
from .views import (
    proveedor_list, 
    proveedor_create, 
    proveedor_update
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

]