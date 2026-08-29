// URL base del backend Django. Cambia el host/puerto si tu API corre en otro lugar.
const API_BASE_URL = 'http://127.0.0.1:8000/api';

const grid = document.getElementById('productosGrid');
const statusBox = document.getElementById('apiStatus');

function mostrarEstado(mensaje, tipo = 'info') {
  statusBox.textContent = mensaje;
  statusBox.className = `alert alert-${tipo}`;
}

function tarjetaProducto(producto) {
  const imagen = producto.imagen
    ? producto.imagen
    : 'https://via.placeholder.com/400x180?text=Sin+imagen';

  return `
    <div class="col-12 col-sm-6 col-lg-4">
      <div class="card card-producto shadow-sm">
        <img src="${imagen}" class="card-img-top" alt="${producto.nombre}">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${producto.nombre}</h5>
          <p class="card-text text-muted small">${producto.categoria_nombre || 'Sin categoría'}</p>
          <p class="card-text flex-grow-1">${producto.descripcion || ''}</p>
          <div class="d-flex justify-content-between align-items-center">
            <span class="fw-bold">$${producto.precio}</span>
            <span class="badge bg-secondary">Stock: ${producto.stock}</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

async function cargarProductos() {
  try {
    const respuesta = await fetch(`${API_BASE_URL}/productos/`);
    if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`);

    const datos = await respuesta.json();
    const productos = Array.isArray(datos) ? datos : datos.results;

    if (!productos || productos.length === 0) {
      mostrarEstado('No hay productos cargados todavía. Agrégalos desde /admin/ en el backend.', 'warning');
      return;
    }

    grid.innerHTML = productos.map(tarjetaProducto).join('');
    statusBox.classList.add('d-none');
  } catch (error) {
    mostrarEstado(
      `No se pudo conectar con el backend (${API_BASE_URL}). Verifica que Django esté corriendo. Detalle: ${error.message}`,
      'danger'
    );
  }
}

document.addEventListener('DOMContentLoaded', cargarProductos);
