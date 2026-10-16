// sections/section8.js

export function init() {
    console.log("INIT SECTION 8 OK - v10");

    const btnLimpiar = document.querySelector("#btnLimpiar");


    // ==========================================
    // HELPERS
    // ==========================================

    function limpiarFormulario() {
        document.querySelector("#id_manifestacion").value = "";
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

 }