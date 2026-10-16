// sections/section4.js
import { showMessage } from "../ui/messages.js";

export function init() {
    console.log("INIT SECTION 4 OK - v11");

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
                    basePath + "/fundamentoLegal/",
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
            const id = e.target.dataset.id; // REVISAR

            const response =
                await fetch(
                    `/fundamentoLegal/${id}/`,
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
                        `/fundamentoLegal/${id}/`,
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
                        `/fundamentoLegal/${id}/`,
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

        const ley = document.querySelector("#ley").value;
        const especificacion = document.querySelector("#especificacion").value;


        formData.append("ley",ley);
        formData.append("especificacion",especificacion);

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        return formData;
    }
    function obtenerDatosJSON() {
        const ley = document.querySelector("#ley").value;
        const especificacion = document.querySelector("#especificacion").value;

        return {
            ley: ley,
            especificacion: especificacion
        };
    }

    function agregarFila(data) {

        // Agregar fila a la tabla
        const tabla = document.getElementById("tablaFundamentosInv");
        tabla.innerHTML += `
            <tr id="fundamentoInv-${data.id}">
                <td>
                    <p>${data.ley}</p>
                </td>
                <td>
                    <p>${data.especificacion}</p>
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

        // Actualizar fila de la tabla
        fila.innerHTML = `
            <tr id="fundamentoInv-${data.id}">
                <td>
                    <p>${data.ley}</p>
                </td>
                <td>
                    <p>${data.especificacion}</p>
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
        console.log(data.tipoConsent);

        btnModificar.dataset.id = data.id;

        document.querySelector("#ley").value = data.ley;
        document.querySelector("#especificacion").value = data.especificacion;
    }

    function limpiarFormulario() {
         document.querySelector("#ley").value = "";
         document.querySelector("#especificacion").value = "";
    }

    function getCSRFToken() {
        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        )?.value;
    }
}
