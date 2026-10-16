// ui/navigation.js

export function initNavigation() {

    const links = document.querySelectorAll(".nav-link");

    const current = parseInt(document.body.dataset.section);
    const max = parseInt(document.body.dataset.seccionActual);

    links.forEach((link) => {

        const section = parseInt(link.dataset.section);

        // limpiar clases
        link.classList.remove("active", "disabled");

        // ACTIVAR sección actual
        if (section === current) {
            link.classList.add("active");
        }

        // DESBLOQUEAR secciones disponibles
        else if (section <= max) {
            link.classList.remove("disabled");
        }

        // BLOQUEAR secciones bloqueadas
        else {
            link.classList.add("disabled");

            // bloquear click
            link.addEventListener("click", (e) => {
                e.preventDefault();
            });
        }

    });
}

// Constantes ESTADOS
const MOSTRAR = false;  // habilitado (disabled = false)
const OCULTAR = true;   // deshabilitado (disabled = true)

    // Función genérica para cambiar estado
export function cambiarEstadoBtn(boton, estado) {
        boton.disabled = estado;
        console.log(`Cambio estado de ${boton.id}`);
    }