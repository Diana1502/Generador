// sections/section1.js

export function init() {
    console.log("INIT SECTION 1 OK -V10");

    const btnLimpiar = document.querySelector("#btnLimpiar");

    const inputNumExt = document.querySelector("#id_numExt_responsable");
    const inputNumInt = document.querySelector("#id_numInt_responsable");
    const inputcodigoPost = document.querySelector("#id_codigoPost_responsable");

    const selectEstado = document.querySelector("#id_entidadFed_responsable");
    const selectMunicipio = document.querySelector("#id_municipio_responsable");

    const urls = JSON.parse(document.body.dataset.urls);
    const urlMunicipios = urls.municipios;

    selectEstado.addEventListener("change", async (e) => {
        const estadoId = e.target.value;

        selectMunicipio.innerHTML = '<option>Cargando...</option>';

        try {
            const response = await fetch(`${urlMunicipios}?estado=${estadoId}`);
            const data = await response.json();

            selectMunicipio.innerHTML = '<option value="">Selecciona un municipio</option>';

            data.forEach((municipio) => {
                const option = document.createElement("option");
                option.value = municipio.id;
                option.textContent = municipio.nombre;

                selectMunicipio.appendChild(option);
            });

        } catch (error) {
            console.error(error);
            selectMunicipio.innerHTML = '<option>Error al cargar</option>';
        }
    });

    function limpiarFormulario() {
        document.querySelector("#id_acronSujetoObligado").value = "";
        document.querySelector("#id_unidadAdmin").value = "";
        document.querySelector("#id_acronUnidadAdmin").value = "";
        //
        document.querySelector("#id_calle_responsable").value = "";
        document.querySelector("#id_numExt_responsable").value = "";
        document.querySelector("#id_numInt_responsable").value = "";
        document.querySelector("#id_colonia_responsable").value = "";
        selectMunicipio.innerHTML = '<option>----</option>';
        document.querySelector("#id_codigoPost_responsable").value = "";
        document.getElementById("id_entidadFed_responsable").selectedIndex = 0;
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);


    function soloNumero(e) {  // MOVER PARA REDUCIR CDG
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
    }
    //     ==========================================
    //     SOLO NUMEROS
    //     ==========================================

    inputNumExt.addEventListener("input", soloNumero);
    inputNumInt.addEventListener("input", soloNumero);
    inputcodigoPost.addEventListener("input", soloNumero);
}