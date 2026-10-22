// sections/section7.js

export function init() {
    console.log("INIT SECTION 7 13/10/2026");

    const btnLimpiar = document.querySelector("#btnLimpiar");

    const inputNumExt = document.querySelector("#id_numExt_ut");
    const inputNumInt = document.querySelector("#id_numInt_ut");
    const inputcodigoPost = document.querySelector("#id_codigoPost_ut");
    const inputTelefono = document.querySelector("#id_telefono");
    const inputExtension = document.querySelector("#id_extension");

    const selectEstado = document.querySelector("#id_entidadFed_ut");
    const selectMunicipio = document.querySelector("#id_municipio_ut");
    const urls = JSON.parse(document.body.dataset.urls);
    const urlMunicipios = urls.municipios;

    const mismaDireccion = document.querySelector("#mismaDireccion");
    const direccion = document.getElementById("direccionResponsable");
    const mismaDireccion1 = document.querySelector("#mismaDireccion1");
    const direccion1 = document.getElementById("direccionResponsable1");

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

    selectEstado.addEventListener("change", async (e) => {
        cargarMunicipios(e.target.value);
    });

    function limpiarFormulario() {
        document.querySelector("#id_telefono").value = "";
        document.querySelector("#id_correo").value = "";
        document.querySelector("#id_paginaWeb").value = "";

        document.querySelector("#id_horarioInicio").value = "00:00";
        document.querySelector("#id_horarioFin").value = "00:00";

        limpiardireccion();
    }
    function limpiardireccion() {
        document.querySelector("#id_calle_ut").value = "";
        document.querySelector("#id_numExt_ut").value = "";
        document.querySelector("#id_numInt_ut").value = "";
        document.querySelector("#id_colonia_ut").value = "";
        selectMunicipio.innerHTML = '<option>----</option>';
        document.querySelector("#id_codigoPost_ut").value = "";
        selectEstado.selectedIndex = 0;
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

    flatpickr("#id_horarioInicio", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
    });
    flatpickr("#id_horarioFin", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
    });

    function soloNumero(e) {
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
    }
    //     ==========================================
    //     SOLO NUMEROS
    //     ==========================================

    inputNumExt.addEventListener("input", soloNumero);
    inputNumInt.addEventListener("input", soloNumero);
    inputcodigoPost.addEventListener("input", soloNumero);
    inputTelefono.addEventListener("input", soloNumero);

    function soloExtension(e) {
        e.target.value = e.target.value.replace(/[^0-9 ]/g, '');
    }
    inputExtension.addEventListener("input", soloExtension);


    mismaDireccion.addEventListener("change", async function () {

        if (this.checked) {
            if (mismaDireccion1) {
                mismaDireccion1.checked = false;
            }
            console.log("copiar dirección");
            // console.log(direccion.value);
            limpiardireccion();

            document.getElementById("id_calle_ut").value =
                direccion.dataset.calle;

            document.getElementById("id_numExt_ut").value =
                direccion.dataset.numext;

            document.getElementById("id_numInt_ut").value =
                direccion.dataset.numint;

            document.getElementById("id_colonia_ut").value =
                direccion.dataset.colonia;

            document.getElementById("id_codigoPost_ut").value =
                direccion.dataset.codigopostal;

            selectEstado.value = direccion.dataset.estado;

            // Cargar municipios del estado seleccionado
            await cargarMunicipios(direccion.dataset.estado);

            selectMunicipio.value = direccion.dataset.municipio;

        } else {
            limpiardireccion();
        }
    });
    mismaDireccion1.addEventListener("change", async function () {

        if (this.checked) {
            mismaDireccion.checked = false;
            console.log("copiar dirección1");
            limpiardireccion();

            document.getElementById("id_calle_ut").value =
                direccion1.dataset.calle;

            document.getElementById("id_numExt_ut").value =
                direccion1.dataset.numext;

            document.getElementById("id_numInt_ut").value =
                direccion1.dataset.numint;

            document.getElementById("id_colonia_ut").value =
                direccion1.dataset.colonia;

            document.getElementById("id_codigoPost_ut").value =
                direccion1.dataset.codigopostal;

            selectEstado.value = direccion1.dataset.estado;

            // Cargar municipios del estado seleccionado
            await cargarMunicipios(direccion1.dataset.estado);

            selectMunicipio.value = direccion1.dataset.municipio;

        } else {
            limpiardireccion();
        }
    });
}