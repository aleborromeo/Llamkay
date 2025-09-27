let indiceActual = 0;
const imagenes = document.querySelectorAll('.carousel-image');

function cambiarImagen(direccion) {
    imagenes[indiceActual].classList.remove('active');
    indiceActual = (indiceActual + direccion + imagenes.length) % imagenes.length;
    imagenes[indiceActual].classList.add('active');
}

// Opcional: cambio automático cada 5 segundos
setInterval(() => cambiarImagen(1), 5000);
