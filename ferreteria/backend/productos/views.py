from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProveedorForm, CategoriaForm, ClienteForm
from .models import Categoria, Producto, Proveedor, Cliente



from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']



@api_view(['GET'])
def health_check(request):
    """Endpoint simple para verificar que la API esta funcionando."""
    return Response({'status': 'ok', 'app': 'ferreteria-backend'})

#----------------------------
# FUNCIONES CRUD DE PROVEEDOR
#----------------------------

def proveedor_list(request):
    proveedores = Proveedor.objects.all()

    #return render(request, 'proveedor_list.html', {'proveedores': proveedores})

    return render(request, 'productos/proveedor_list.html', {'proveedores': proveedores})


def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'productos/proveedor_form.html', {'form': form})

def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'productos/proveedor_form.html', {'form': form})

def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'productos/proveedor_confirm_delete.html', {'proveedor': proveedor})

#-------------------------------------
# FUNCIONES CRUD DE LA TABLA CATEGORIA
#-------------------------------------
def categoria_list(request):
    categorias = Categoria.objects.all()

    return render(request, 'productos/categoria_list.html', {'categorias' : categorias})

def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'productos/categoria_form.html', {'form': form})


def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/categoria_form.html', {'form': form})

def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'productos/categoria_confirm_delete.html', {'categoria': categoria})

#------------------------------------------------------------------------------------------------
# FUNCIONES CRUD DE LA TABLA CLIENTE (EL DEL GIM, AUNQUE ESTO ES UNA FERRETERIA JEJEJEJEJE -°_°-)
#------------------------------------------------------------------------------------------------
def cliente_list(request):
    clientes = Cliente.objects.all()

    plan_filtro = request.GET.get('plan')

    if plan_filtro:
        clientes = clientes.filter(plan=plan_filtro)

    return render(request, 'clientes/cliente_list.html', {'clientes' : clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})


def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})