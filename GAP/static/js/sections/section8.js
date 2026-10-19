// sections/section8.js

export function init() {
    console.log("INIT SECTION 8");

    const btnAgregar = document.querySelector("#btnAgregar");
    const btnModificar = document.querySelector("#btnModificar");
    const btnLimpiar = document.querySelector("#btnLimpiar");
    const tabla = document.querySelector("#tablaTercerosInv")

    // ==========================================
    // AGREGAR
    // ==========================================

    btnAgregar.addEventListener(
        "click",
        async () => {
            const basePath = window.location.pathname.split("/seccion/")[0];

            const response =
                await fetch(
                    basePath + "/transferencia/",
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

            location.reload();
//            agregarFila(data);
//            limpiarFormulario();
        }
    );

    // ==========================================
    // MODIFICAR - guardar datos
    // ==========================================

    btnModificar.addEventListener(
        "click",
        async (e) => {
            const id = e.target.dataset.id; // REVISAR

            const response =
                await fetch(
                    `/transferencia/${id}/`,
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

            location.reload();
        }
    );

    // ==========================================
    // ELIMINAR y MODIFICAR - cargar datos
    // ==========================================

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
                        `/transferencia/${id}/`,
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
                    document.querySelector(`#terceroInv-${id}`).remove();
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
                        `/transferencia/${id}/`,
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

    // ==========================================
    // HELPERS
    // ==========================================
    function obtenerDatos() {
        const formData = new FormData();

        const destinatario = document.querySelector("#destinatario").value;
        const consentimiento = document.querySelector("#consentimiento").value;
        const tipoConsentimiento = document.querySelector("#tipoConsentimiento").value;

        const finalidades = [];

        document.querySelectorAll(".finalidadCheck:checked").forEach(fn => {
            finalidades.push(fn.value);
        });

        formData.append("destinatario",destinatario);
        formData.append("consentimiento",consentimiento);
        formData.append("tipoConsentimiento",tipoConsentimiento);

        finalidades.forEach(id => {
            formData.append(
                "finalidades[]",
                id
            );
        });

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        return formData;
    }

    function obtenerDatosJSON() {
        const destinatario = document.querySelector("#destinatario").value;
        const consentimiento = document.querySelector("#consentimiento").value;
        const tipoConsentimiento = document.querySelector("#tipoConsentimiento").value;

        const finalidades = [];

        document.querySelectorAll(".finalidadCheck:checked").forEach(fn => {
            finalidades.push(fn.value);
        });

        return {
            destinatario: destinatario,
            consentimiento: consentimiento,
            tipoConsentimiento: tipoConsentimiento,
            finalidades: finalidades
        };
    }

    function agregarFila(data) {
        // Construir badges de finalidades
        const finalidades = data.finalidades.map(f => `
            <span class="badge bg-secondary me-1">
                ${f}
            </span>
        `).join("");

        // Construir consentimiento y tipoConsentimiento
        const consentimientoHtml = data.consentimiento
        ? "Sí"
        : "No";

        // Agregar fila a la tabla
        const tabla = document.getElementById("tablaTercerosInv");
        tabla.innerHTML += `
            <tr id="terceroInv-${data.id}">
                <td>
                    <p>${data.destinatario}</p>
                    <p>${data.tipoConsentimiento}</p>
                </td>
                <td>
                    ${finalidades}
                </td>
                <td>
                    ${consentimientoHtml}
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
                    `#terceroInv-${data.id}`
                );

        // Construir badges de finalidades
        const finalidades = data.finalidades.map(f => `
            <span class="badge bg-secondary me-1">
                ${f}
            </span>
        `).join("");

        // Construir consentimiento y tipoConsentimiento
        const consentimientoHtml = data.consentimiento
        ? "Sí"
        : "No";

        // Actualizar fila de la tabla
        fila.innerHTML = `
            <tr id="terceroInv-${data.id}">
                <td>
                    ${data.destinatario}
                    <br>
                    ${data.tipoConsentimiento}
                </td>
                <td>
                    ${finalidades}
                </td>
                <td>
                    ${consentimientoHtml}
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

        document.querySelector("#destinatario").value = data.destinatario;
        document.querySelector("#consentimiento").value = String(data.consentimiento);
        document.querySelector("#tipoConsentimiento").value = data.tipoConsentimiento;

        document.querySelectorAll('.finalidadCheck').forEach(input => {
            const fila = input.closest('.row');
            const labelText = fila.querySelector('label').textContent.trim();

            // Verificar si la finalidad está en el JSON
            const existe = data.finalidades.flat().includes(labelText);

            // console.log("finalidades:", data.finalidades);
            // console.log("Finalidad:", labelText);
            // console.log("¿Existe en JSON?:", existe);

            input.checked = existe;
        });
    }

    function limpiarFormulario() {
        document.querySelector("#destinatario").value = "";
        document.querySelector("#consentimiento").value = "";
        document.querySelector("#tipoConsentimiento").value = "";
        document.querySelectorAll(".finalidadCheck").forEach(cb => {
            cb.checked = false;
        });
    }

    //     ==========================================
    //     LIMPIAR FORMULARIO
    //     ==========================================

    btnLimpiar.addEventListener("click", limpiarFormulario);

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