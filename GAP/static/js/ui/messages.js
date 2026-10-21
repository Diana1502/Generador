// ui/messages.js

export function initMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 3000);
    });
}

export function showMessage(message, type = "error") {
    const container = document.getElementById("message-container");

    if (!container) return;

    const msg = document.createElement("div");
    msg.className = `alert alert-${type}`;
    msg.textContent = message;

    container.appendChild(msg);

    setTimeout(() => {
        msg.remove();
    }, 3000);
}


document.addEventListener("DOMContentLoaded", function () {

    const modalElement = document.getElementById("modalDisclaimer");
    const modal = new bootstrap.Modal(modalElement);

    const btnConfirmar = document.getElementById("confirmarDescarga");

    let urlDescarga = null;

    // Detectar clic en botones dinámicos
    document.addEventListener("click", function (event) {

        const boton = event.target.closest(".btn-descargar-word");

        if (!boton) return;

        event.preventDefault();

        urlDescarga = boton.href;

        modal.show();
    });

    // Confirmar descarga
    btnConfirmar.addEventListener("click", function () {

        if (!urlDescarga) return;

        const url = urlDescarga;
        urlDescarga = null;

        modal.hide();

        // Iniciar descarga sin abandonar la página
        const enlace = document.createElement("a");
        enlace.href = url;
        enlace.style.display = "none";

        document.body.appendChild(enlace);
        enlace.click();
        enlace.remove();
    });

    // Limpiar al cerrar el modal
    modalElement.addEventListener("hidden.bs.modal", function () {
        urlDescarga = null;
    });

});