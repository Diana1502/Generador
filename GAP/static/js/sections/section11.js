// sections/section11.js

export function init() {
    console.log("INIT SECTION 11 13102026");

    const btnLimpiar = document.querySelector("#btnLimpiar");


    // ==========================================
    // HELPERS
    // ==========================================

    function limpiarFormulario() {
        document.querySelector("#id_portabilidad").value = "";
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

 }