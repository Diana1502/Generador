// sections/section11.js

export function init() {
    console.log("INIT SECTION 11 - v18");

    const btnLimpiar = document.querySelector("#btnLimpiar");


    // ==========================================
    // HELPERS
    // ==========================================

    function limpiarFormulario() {
        document.getElementById("id_desicNotHuman").checked = false;
        document.getElementById("id_usoNube").checked = false;
        document.getElementById("id_encargadosTrat").checked = false;
        document.getElementById("id_remisiones").checked = false;
        document.getElementById("id_menorEdad").checked = false;
        document.getElementById("id_biometricos").checked = false;
        document.getElementById("id_evalImpacto").checked = false;
        document.querySelector("#id_observaciones").value = "";
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

 }