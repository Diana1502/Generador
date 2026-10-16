// sections/section2.js

export function init() {
    console.log("INIT SECTION 2 13102026");

    const btnLimpiar = document.querySelector("#btnLimpiar");


    // ==========================================
    // HELPERS
    // ==========================================

    function limpiarFormulario() {
        document.querySelector("#id_nombreTratamiento").value = "";
        document.querySelector("#id_descTratamiento").value = "";
        document.querySelector("#id_objTratamiento").value = "";
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

 }