// sections/section3.js
import { showMessage } from "../ui/messages.js";

export function init() {
    console.log("INIT SECTION 3");

    const btnAgregar = document.querySelector("#btnAgregar");
    const btnModificar = document.querySelector("#btnModificar");
    const btnLimpiar = document.querySelector("#btnLimpiar");
    const tabla = document.querySelector("#tablaFundamentosInv");

//     ==========================================
//     LIMPIAR FORMULARIO
//     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);


//     ==========================================
//     AGREGAR
//     ==========================================

    btnAgregar.addEventListener(
        "click",
        async () => {
            const basePath = window.location.pathname.split("/seccion/")[0];

            const response =
                await fetch(
                    basePath + "/datos/",
                    {
                        method: "POST",
                        headers: {
                            "X-CSRFToken":
                                getCSRFToken()
                        },
                        body: obtenerDatos()
                    }
                );

            const data = await response.json();

            if (!data.success) {
                alert("Error");
                return;
            }

            agregarFila(data);
            limpiarFormulario();
        }
    );
//
//     ==========================================
//     MODIFICAR - guardar datos
//     ==========================================

    btnModificar.addEventListener(
        "click",
        async (e) => {
            const id = e.target.dataset.id;

            const response =
                await fetch(
                    `/datos/${id}/`,
                    {
                        method: "PUT",
                        headers: {
                            "X-CSRFToken": getCSRFToken()
                        },
                        body: JSON.stringify(obtenerDatosJSON())
                    }
                );

            const data = await response.json();

            if (!response.ok || !data.success) {
                alert(data.error ||"Error al actualizar el registro");
                return;
            }

            actualizarFila(data);
            limpiarFormulario();
            cambiarEstadoBtn(btnModificar,OCULTAR);
            cambiarEstadoBtn(btnAgregar,MOSTRAR);
        }
    );

//     ==========================================
//     ELIMINAR y MODIFICAR - cargar datos
//     ==========================================

    tabla.addEventListener(
        "click",
        async (e) => {

            if (    // ELIMINAR
                e.target.classList.contains(
                    "btnEliminar"
                )
            ) {
                const id = e.target.dataset.id;

                const response =
                    await fetch(
                        `/datos/${id}/`,
                        {
                            method: "DELETE",
                            headers: {

                                "X-CSRFToken":
                                    getCSRFToken()
                            }
                        }
                    );

                const data = await response.json();

                if (data.success) {
                    document.querySelector(`#fundamentoInv-${id}`).remove();
                }
            }
            else if (   // MODIFICAR
                e.target.classList.contains(
                    "btnEditar"
                )
            ) {
                const id = e.target.dataset.id;

                const response =
                    await fetch(
                        `/datos/${id}/`,
                        {
                            method: "GET",
                            headers: {

                                "X-CSRFToken":
                                    getCSRFToken()
                            }
                        }
                    );

                const data = await response.json();

                if (data.success) {
                    console.log("Exito al cargar para editar");
                    limpiarFormulario();
                    cargarDatosEnFormulario(data);
                    cambiarEstadoBtn(btnModificar,MOSTRAR);
                    cambiarEstadoBtn(btnAgregar,OCULTAR);
                }
            }
            else {
                return;
            }
        }
    );

//     ==========================================
//     HELPERS
//     ==========================================
    function obtenerDatos() {
        const formData = new FormData();

        const dato = document.querySelector("#dato").value;
        const datosSensibles = document.querySelector("#datosSensibles").value;
        const obtencionDatos = document.querySelector("#obtencionDatos").value;
        const medioObtencion = document.querySelector("#medioObtencion").value;

        formData.append("dato",dato);
        formData.append("datosSensibles",datosSensibles);
        formData.append("obtencionDatos",obtencionDatos);
        formData.append("medioObtencion",medioObtencion);

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        return formData;
    }
    function obtenerDatosJSON() {
        const dato = document.querySelector("#dato").value;
        const datosSensibles = document.querySelector("#datosSensibles").value;
        const obtencionDatos = document.querySelector("#obtencionDatos").value;
        const medioObtencion = document.querySelector("#medioObtencion").value;

        return {
            dato: dato,
            datosSensibles: datosSensibles,
            obtencionDatos: obtencionDatos,
            medioObtencion: medioObtencion
        };
    }

    function agregarFila(data) {
        // Construir datosSensibles
        const sensibleHtml = data.datosSensibles
        ? "Sensible"
        : "-";

        // Construir Obtencion
        const obtencionHtml = data.consentimiento
        ? `Sí <br> ${data.tipoConsentimiento}`
        : "No";

        // Agregar fila a la tabla
        const tabla = document.getElementById("tablaFundamentosInv");
        tabla.innerHTML += `
            <tr id="fundamentoInv-${data.id}">
                <td>
                    ${data.dato}
                </td>
                <td>
                    ${sensibleHtml}
                </td>
                <td>
                    ${data.obtencionDatos}
                    <br>
                    ${data.medioObtencion}
                </td>
                <td>
                    <button
                        class="btn btn-danger btnEliminar"
                        data-id="${data.id}">
                        Eliminar
                    </button>
                    <br><br>
                    <button
                        class="btn btn-warning btnEditar"
                        data-id="${data.id}">
                        Editar
                    </button>
                </td>
            </tr>
        `;
    }

    function actualizarFila(data) {
        // Buscar fila
        const fila = document.querySelector(
                    `#fundamentoInv-${data.id}`
                );

        // Construir datosSensibles
        const sensibleHtml = data.datosSensibles
        ? "Sensible"
        : "-";

        // Construir Obtencion
        const obtencionHtml = data.consentimiento
        ? `Sí <br> ${data.tipoConsentimiento}`
        : "No";

        // Actualizar fila de la tabla
        fila.innerHTML = `
            <tr id="fundamentoInv-${data.id}">
                <td>
                    ${data.dato}
                </td>
                <td>
                    ${sensibleHtml}
                </td>
                <td>
                    ${data.obtencionDatos}
                    <br>
                    ${data.medioObtencion}
                </td>
                <td>
                    <button
                        class="btn btn-danger btnEliminar"
                        data-id="${data.id}">
                        Eliminar
                    </button>
                    <br><br>
                    <button
                        class="btn btn-warning btnEditar"
                        data-id="${data.id}">
                        Editar
                    </button>
                </td>
            </tr>
        `;
    }


// =============== LOGICA BOTONES
    // Constantes globales
    const MOSTRAR = false;  // habilitado (disabled = false)
    const OCULTAR = true;   // deshabilitado (disabled = true)

    // Función genérica para cambiar estado
    function cambiarEstadoBtn(boton, estado) {
        boton.disabled = estado;
        console.log(`Cambio estado de ${boton.id}`);
    }
    cambiarEstadoBtn(btnModificar,OCULTAR);
// ===============

    function cargarDatosEnFormulario(data){
        console.log(data);
        console.log(data.datosSensibles);

        btnModificar.dataset.id = data.id;

        document.querySelector("#dato").value = data.dato;
        document.querySelector("#datosSensibles").value = data.datosSensibles;
        document.querySelector("#obtencionDatos").value = data.obtencionDatos;
        document.querySelector("#medioObtencion").value = data.medioObtencion;
    }

    function limpiarFormulario() {
        document.querySelector("#dato").value = "";
        document.querySelector("#datosSensibles").value = "---";
        document.querySelector("#obtencionDatos").value = "-----";
        document.querySelector("#medioObtencion").value = "----";
    }

    function getCSRFToken() {
        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        )?.value;
    }
}
