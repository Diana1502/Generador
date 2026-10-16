// sections/section9.js

export function init() {
    console.log("INIT SECTION 9 OK - v11");

    const btnLimpiar = document.querySelector("#btnLimpiar");


    // ==========================================
    // HELPERS
    // ==========================================

    function limpiarFormulario() {
        const contenedor = document.getElementById("id_modificaciones");
        const checkboxes = contenedor.querySelectorAll("input[type='checkbox']");

        checkboxes.forEach(cb => cb.checked = false);
        document.querySelector("#id_url").value = "";
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

 }