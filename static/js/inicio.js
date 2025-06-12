let charts = {};

function destruirGrafico(idCanvas) {
    if (charts[idCanvas]) {
        charts[idCanvas].destroy();
    }
}

async function cargarGraficos() {
    try {
        const resFinanzas = await fetch(`/api/finanzas`);
        const data = await resFinanzas.json();

        const ingresos = parseFloat(data.ingresos);
        const gastos = parseFloat(data.gastos);
        const beneficio = parseFloat(data.beneficio);
        const margen = parseFloat(data.margen_beneficio);

        destruirGrafico('graficoBarras');
        charts['graficoBarras'] = new Chart(document.getElementById('graficoBarras').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Totales'],
                datasets: [
                    {
                        label: 'Ingresos',
                        data: [ingresos],
                        backgroundColor: '#27ae60'
                    },
                    {
                        label: 'Gastos',
                        data: [gastos],
                        backgroundColor: '#c0392b'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#fff' } } },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' } }
                }
            }
        });

        destruirGrafico('graficoLineas');
        charts['graficoLineas'] = new Chart(document.getElementById('graficoLineas').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Totales'],
                datasets: [
                    {
                        label: 'Beneficio neto',
                        data: [beneficio],
                        borderColor: '#2980b9',
                        backgroundColor: 'rgba(41, 128, 185, 0.2)',
                        fill: true
                    },
                    {
                        label: 'Margen de beneficio (%)',
                        data: [margen],
                        borderColor: '#f1c40f',
                        backgroundColor: 'rgba(241, 196, 15, 0.2)',
                        fill: true,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: '#fff' } } },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' }, position: 'left' },
                    y1: {
                        position: 'right',
                        ticks: { color: '#fff' },
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });
    } catch (err) {
        console.error('Error cargando finanzas:', err);
    }
}

async function cargarProductos(categoriaSeleccionada = "") {
    try {
        const response = await fetch('/api/tabla_productos');
        const productos = await response.json();

        const tablaBody = document.querySelector('#tabla-productos tbody');
        tablaBody.innerHTML = '';

        const categorias = new Set();

        productos.forEach(producto => {
            categorias.add(producto.categoria);

            if (categoriaSeleccionada && producto.categoria !== categoriaSeleccionada) return;

            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${producto.nombre}</td>
                <td>${producto.descripcion}</td>
                <td>${parseFloat(producto.precio).toFixed(2)} €</td>
                <td>${producto.stock}</td>
                <td>${producto.categoria}</td>
            `;
            tablaBody.appendChild(fila);
        });

        const selectCategoria = document.getElementById('filtroCategoria');
        if (selectCategoria && selectCategoria.children.length <= 1) {
            categorias.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                selectCategoria.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

async function cargarVentas() {
    try {
        const res = await fetch('/api/ventas');
        const ventas = await res.json();
        const tbody = document.querySelector('#tabla-ventas tbody');
        tbody.innerHTML = '';

        ventas.forEach(venta => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${new Date(venta.fecha).toLocaleDateString()}</td>
                <td>${venta.cliente}</td>
                <td>${venta.empleado}</td>
                <td>${parseFloat(venta.total).toFixed(2)} €</td>
            `;
            tr.addEventListener('click', () => mostrarDetallesVenta(venta.id_venta));
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error al cargar ventas:', error);
    }
}

async function mostrarDetallesVenta(id_venta) {
    try {
        const res = await fetch(`/api/ventas/detalles?id=${id_venta}`);
        const detalles = await res.json();
        const detallesBody = document.querySelector('#tabla-detalles-body');
        detallesBody.innerHTML = '';

        detalles.forEach(d => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${d.producto}</td>
                <td>${d.cantidad}</td>
                <td>${parseFloat(d.precio_unitario).toFixed(2)} €</td>
                <td>${parseFloat(d.subtotal).toFixed(2)} €</td>
            `;
            detallesBody.appendChild(tr);
        });

        document.getElementById('detalles-venta').style.display = 'block';
    } catch (error) {
        console.error('Error al cargar detalles de venta:', error);
    }
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        targetSection.style.display = 'block';

        if (sectionId === 'section1') {
            cargarGraficos();
        } else if (sectionId === 'section2') {
            cargarProductos();
        } else if (sectionId === 'section3') {
            cargarVentas();
        }
    }
}

// Evento DOM cargado
document.addEventListener('DOMContentLoaded', () => {
    showSection('section1');  // Mostrar la primera sección por defecto

    const selectCategoria = document.getElementById('filtroCategoria');
    if (selectCategoria) {
        selectCategoria.addEventListener('change', () => {
            const categoriaSeleccionada = selectCategoria.value;
            cargarProductos(categoriaSeleccionada);
        });
    }
});
