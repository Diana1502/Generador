// sections/section5.js

export function init() {
    console.log("INIT SECTION 6 OK -V20");

    const btnLimpiar = document.querySelector("#btnLimpiar");

    const inputNumExt = document.querySelector("#id_numExt_unidadresp");
    const inputNumInt = document.querySelector("#id_numInt_unidadresp");
    const inputcodigoPost = document.querySelector("#id_codigoPost_unidadresp");
    const inputTelefono = document.querySelector("#id_telefono");
    const inputExtension = document.querySelector("#id_extension");

    const selectEstado = document.querySelector("#id_entidadFed_unidadresp");
    const selectMunicipio = document.querySelector("#id_municipio_unidadresp");
    const urls = JSON.parse(document.body.dataset.urls);
    const urlMunicipios = urls.municipios;

    const mismaDireccion = document.querySelector("#mismaDireccion");
    const direccion = document.getElementById("direccionResponsable");


    async function cargarMunicipios(estadoId) {
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
            console.log("Se cargaron los municipios");

        } catch (error) {
            console.error(error);
            selectMunicipio.innerHTML = '<option>Error al cargar</option>';
        }
    }

    selectEstado.addEventListener("change", (e) => {
        cargarMunicipios(e.target.value);
    });


    function limpiarFormulario() {
        document.querySelector("#id_procARCO").value = "";
        const contenedor = document.getElementById("id_medPresentacion");
        const checkboxes = contenedor.querySelectorAll("input[type='checkbox']");

        checkboxes.forEach(cb => cb.checked = false);

        document.querySelector("#id_unidadResp").value = "";
        document.querySelector("#id_correo").value = "";
        document.querySelector("#id_telefono").value = "";

        limpiardireccion();
    }
    function limpiardireccion() {
        document.querySelector("#id_calle_unidadresp").value = "";
        document.querySelector("#id_numExt_unidadresp").value = "";
        document.querySelector("#id_numInt_unidadresp").value = "";
        document.querySelector("#id_colonia_unidadresp").value = "";
        selectMunicipio.innerHTML = '<option>----</option>';
        document.querySelector("#id_codigoPost_unidadresp").value = "";
        selectEstado.selectedIndex = 0;
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

    function soloNumero(e) {
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
    }
    function soloExtension(e) {
        e.target.value = e.target.value.replace(/[^0-9 ]/g, '');
    }
    //     ==========================================
    //     SOLO NUMEROS
    //     ==========================================

    inputNumExt.addEventListener("input", soloNumero);
    inputNumInt.addEventListener("input", soloNumero);
    inputcodigoPost.addEventListener("input", soloNumero);
    inputTelefono.addEventListener("input", soloNumero);
    inputExtension.addEventListener("input", soloExtension);


    mismaDireccion.addEventListener("change", async function () {

        if (this.checked) {
            console.log("copiar dirección");
            limpiardireccion();

            document.getElementById("id_calle_unidadresp").value =
                direccion.dataset.calle;

            document.getElementById("id_numExt_unidadresp").value =
                direccion.dataset.numext;

            document.getElementById("id_numInt_unidadresp").value =
                direccion.dataset.numint;

            document.getElementById("id_colonia_unidadresp").value =
                direccion.dataset.colonia;

            document.getElementById("id_codigoPost_unidadresp").value =
                direccion.dataset.codigopostal;

            selectEstado.value = direccion.dataset.estado;

            // Cargar municipios del estado seleccionado
            await cargarMunicipios(direccion.dataset.estado);

            selectMunicipio.value = direccion.dataset.municipio;

        } else {
            limpiardireccion();
        }
    });
}