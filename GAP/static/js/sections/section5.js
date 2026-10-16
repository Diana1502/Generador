// sections/section5.js
import { showMessage } from "../ui/messages.js";

export function init() {
    console.log("INIT SECTION 5");

    const btnAgregar = document.querySelector("#btnAgregar");
    const btnModificar = document.querySelector("#btnModificar");
    const btnLimpiar = document.querySelector("#btnLimpiar");
    const tabla = document.querySelector("#tablaFinalidadesInv")

    // Secciones
    const selectNecesaria = document.getElementById('necesaria');
    const divNecesaria = document.getElementById("divInnecesaria");
    const selectConsentimiento = document.getElementById('reqConsentimiento');
    const divConsentimiento = document.getElementById("divConsentimiento");
    const selectOtro = document.getElementById('tipoConsentimiento');
    const divOtro = document.getElementById("divOtro");

   selectNecesaria.addEventListener('change', (event) => {
       // Convertimos la cadena de texto "true"/"false" a un booleano real
       const esNecesaria = event.target.value === 'true';

       if (esNecesaria) {
           console.log('El usuario seleccionó Sí');
           divNecesaria.style.display = "none";
       } else {
          console.log('El usuario seleccionó No');
          divNecesaria.style.display = "block";
       }
   });

   selectConsentimiento.addEventListener('change', (event) => {
       // Convertimos la cadena de texto "true"/"false" a un booleano real
       const esConsentimiento = event.target.value === 'true';

       if (esConsentimiento) {
           console.log('El usuario seleccionó Si');
           divConsentimiento.style.display = "block";
       } else {
          console.log('El usuario seleccionó No');
          divConsentimiento.style.display = "none";
       }
   });

   selectOtro.addEventListener('change', (event) => {
       // Convertimos la cadena de texto "true"/"false" a un booleano real
       const esOtro = event.target.value === 'W';

       if (esOtro) {
           console.log('El usuario seleccionó Si');
           divOtro.style.display = "block";
       } else {
          console.log('El usuario seleccionó No');
          divOtro.style.display = "none";
       }
   });


//     ==========================================
//     AGREGAR
//     ==========================================

    btnAgregar.addEventListener(
        "click",
        async () => {
            const basePath = window.location.pathname.split("/seccion/")[0];

            const response =
                await fetch(
                    basePath + "/finalidad/",
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
                    `/finalidad/${id}/`,
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
                        `/finalidad/${id}/`,
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
                    document.querySelector(`#finalidadInv-${id}`).remove();
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
                        `/finalidad/${id}/`,
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
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

//     ==========================================
//     HELPERS
//     ==========================================
    function obtenerDatos() {
        const formData = new FormData();

        const finalidad = document.querySelector("#finalidad").value;
        const necesaria = document.querySelector("#necesaria").value;
        const reqConsentimiento = document.querySelector("#reqConsentimiento").value;
        const tipoConsentimiento = document.querySelector("#tipoConsentimiento").value;
        const finPrincipal = document.querySelector("#finPrincipal").value;


        formData.append("finalidad",finalidad);
        formData.append("necesaria",necesaria);
        formData.append("reqConsentimiento",reqConsentimiento);
        formData.append("tipoConsentimiento",tipoConsentimiento);
        formData.append("finPrincipal",finPrincipal);

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        return formData;
    }

    function obtenerDatosJSON() {
        const finalidad = document.querySelector("#finalidad").value;
        const necesaria = document.querySelector("#necesaria").value;
        const reqConsentimiento = document.querySelector("#reqConsentimiento").value;
        const tipoConsentimiento = document.querySelector("#tipoConsentimiento").value;
        const finPrincipal = document.querySelector("#finPrincipal").value;

        return {
            finalidad: finalidad,
            necesaria: necesaria,
            reqConsentimiento: reqConsentimiento,
            tipoConsentimiento: tipoConsentimiento,
            finPrincipal: finPrincipal
        };
    }

    function agregarFila(data) {
        // Construir Necesaria
        const necesariaHtml = data.necesaria
        ? "Necesaria"
        : "-";

        // Construir Consentimiento
        const consentimientoHtml = data.reqConsentimiento
        ? "Requiere consentimiento"
        : "No";

        // Construir finPrincipal
        const principalHtml = data.finPrincipal
        ? "Finalidad primaria"
        : "Finalidad secundaria";

        //Construir tipoFinalidad - BagdesHTML
        const BadgesHTML = data.finPrincipal
        ? '<span class="badge bg-success me-1">Principal</span>'
        : '<span class="badge bg-secondary me-1">Secundaria</span>';

        // Agregar fila a la tabla
        const tabla = document.getElementById("tablaFinalidadesInv");
        tabla.innerHTML += `
            <tr id="finalidadInv-${data.id}">
                <td>
                    ${data.finalidad}
                    <br>
                    ${BadgesHTML}
                </td>
                <td>
                    <p>${necesariaHtml}</p>
                </td>
                <td>
                    <p>${consentimientoHtml}</p>
                    ${data.tipoConsentimiento}
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
        console.log(data);
        // Buscar fila
        const fila = document.querySelector(
                    `#datoInv-${data.id}`
                );

         // Construir Necesaria
        const necesariaHtml = data.necesaria
        ? "Necesaria"
        : "No";

        // Construir Consentimiento
        const consentimientoHtml = data.reqConsentimiento
        ? "Requiere consentimiento"
        : "No";

        // Construir finPrincipal
        // Determinar la clase y el texto según el booleano
        const BadgesHTML = data.finPrincipal
        ? '<span class="badge bg-success me-1">Principal</span>'
        : '<span class="badge bg-secondary me-1">Secundaria</span>';

        // Actualizar fila de la tabla

        fila.innerHTML += `
            <tr id="finalidadInv-${data.id}">
                <td>
                    ${data.finalidad}
                    <br>
                    ${BadgesHTML}
                </td>
                <td>
                    <p>${necesariaHtml}</p>
                </td>
                <td>
                    <p>${consentimientoHtml}</p>
                    ${data.tipoConsentimiento}
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

    function cargarDatosEnFormulario(data){
        console.log(data);
        console.log(data.tipoConsentimiento);

        btnModificar.dataset.id = data.id;

        document.querySelector("#finalidad").value = data.finalidad;
        document.querySelector("#necesaria").value = data.necesaria;
        document.querySelector("#reqConsentimiento").value = data.reqConsentimiento;
        document.getElementById("tipoConsentimiento").value = data.tipoConsentimiento;
        document.querySelector("#finPrincipal").value = data.finPrincipal;
    }

    function limpiarFormulario() {
        document.querySelector("#finalidad").value = "";
        document.querySelector("#necesaria").value = "---";
        document.querySelector("#reqConsentimiento").value = "----";
        document.querySelector("#tipoConsentimiento").value = "----";
        document.querySelector("#finPrincipal").value = "---";
    }

    function getCSRFToken() {
        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        )?.value;
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
}
