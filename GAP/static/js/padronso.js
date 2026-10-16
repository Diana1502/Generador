//import { initMessages } from './ui/messages.js';

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('selects-container');
    const inputFinal = document.getElementById('elemento_final_id');
    const btnEnviar = document.getElementById('btn-enviar');
    const inputBuscador = document.getElementById('input-buscador');
    const inputOcultoB = document.getElementById('elemento_final1_id');
    const btnEnviarBuscador = document.getElementById('btn-enviar-buscador')
    const listaResultados = document.getElementById('lista-resultados');
    let timeoutId = null;

    // Escuchamos los cambios en el contenedor usando delegación de eventos
    container.addEventListener('change', async (event) => {
        if (!event.target.classList.contains('selector-cascada')) return;

        const selectActual = event.target;
        const nivelActual = parseInt(selectActual.dataset.level);
        const padreId = selectActual.value;

         // 1. Limpieza total de los niveles inferiores si el usuario cambia una opción superior
         limpiarNivelesInferiores(nivelActual);
         inputFinal.value = "";
         btnEnviar.disabled = true;

         if (!padreId) return; // Si vuelve a seleccionar la opción vacía, terminamos
            try {
                // 2. Consultar a la API de Django por los hijos del elemento seleccionado
                const respuesta = await fetch(`/SO/hijos/${padreId}/`);
                if (!respuesta.ok) throw new Error('Error en la comunicación con el servidor');
                    const hijos = await respuesta.json();

                    // 3. Evaluar el resultado asimétrico
                    if (hijos.length > 0) {
                    // El elemento tiene hijos, por lo tanto creamos el siguiente selector (Nivel + 1)
                       crearSiguienteSelect(hijos, nivelActual + 1);
                    } else {
                        // No hay más hijos: hemos llegado a un elemento "hoja" (Ramo o Sujeto final)
                        // Guardamos este ID en el input oculto y activamos el botón de enviar
                        inputFinal.value = padreId;
                        btnEnviar.disabled = false;
                    }
            } catch (error) {
                console.error("Error al cargar el catálogo:", error);
                alert("No se pudieron cargar las opciones del siguiente nivel.");
            }
    });

    /**
    * Enviar el SO
    */
    btnEnviar.addEventListener('click', () => {
        const idSeleccionado = inputFinal.value;

        // Obtenemos todos los selects generados y tomamos el último
        const todosLosSelects = container.querySelectorAll('.selector-cascada');
        const ultimoSelect = todosLosSelects[todosLosSelects.length - 1];

        // Obtenemos el texto de la opción seleccionada en el último select
        const nombreSeleccionado = ultimoSelect.options[ultimoSelect.selectedIndex].text;

        console.log("ID:", idSeleccionado);
        console.log("Nombre:", nombreSeleccionado);

        // confirm(`Selección en Cascada:\nID: ${idSeleccionado}\nNombre: ${nombreSeleccionado}`);
       // showMessage("warning", "Sujeto Obligado seleccionado:\nID: ${idSeleccionado}\nNombre: ${nombreSeleccionado}");
        mostrarConfirmacion(idSeleccionado,nombreSeleccionado);
    });

    /**
    * Remueve del DOM todos los divs de selectores que sean de un nivel mayor al actual.
    */
    function limpiarNivelesInferiores(nivelActual) {
        const grupos = container.querySelectorAll('.level-group');
        grupos.forEach(grupo => {
            if (parseInt(grupo.dataset.level) > nivelActual) {
                grupo.remove();
            }
        });
    }

    /**
    * Construye dinámicamente el HTML de un nuevo selector con Bootstrap y lo inyecta.
    */
    function crearSiguienteSelect(opciones, nuevoNivel) {
        // Crear el div contenedor con clases de Bootstrap
        const divGrupo = document.createElement('div');
        divGrupo.className = 'mb-3 level-group';
        divGrupo.dataset.level = nuevoNivel;

        // Crear el label descriptivo dependiente del nivel
        const label = document.createElement('label');
        label.className = 'form-label fw-semibold';
        label.setAttribute('for', `select-level-${nuevoNivel}`);
        label.textContent = `Subnivel ${nuevoNivel}`;

        // Crear el elemento Select
        const select = document.createElement('select');
        select.id = `select-level-${nuevoNivel}`;
        select.className = 'form-select selector-cascada';
        select.dataset.level = nuevoNivel;

        // Opción por defecto deshabilitada
        const opcionDefecto = document.createElement('option');
        opcionDefecto.value = "";
        opcionDefecto.textContent = `-- Selecciona una opción del nivel ${nuevoNivel} --`;
        opcionDefecto.disabled = true;
        opcionDefecto.selected = true;
        select.appendChild(opcionDefecto);

        // Rellenar con las opciones traídas de la base de datos
        opciones.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.nombre;
            select.appendChild(option);
        });

        // Armar la estructura e inyectarla al contenedor principal
        divGrupo.appendChild(label);
        divGrupo.appendChild(select);
        container.appendChild(divGrupo);
    }

    // ********************** BUSCADOR *********************
    inputBuscador.addEventListener('input', (e) => {
        const texto = e.target.value.trim();

        // Limpiar el ID seleccionado si el usuario modifica el texto
        inputOcultoB.value = "";
        btnEnviarBuscador.disabled = true;

        // Cancelar la petición anterior si el usuario sigue escribiendo (Debounce)
        clearTimeout(timeoutId);

        if (texto.length < 2) {
            listaResultados.style.display = 'none';
            listaResultados.innerHTML = '';
            return;
        }

        // Esperamos 300ms después de que el usuario deja de teclear para consultar al servidor
        timeoutId = setTimeout(async () => {
            try {
                const res = await fetch(`/SO/buscar-hijos/?q=${encodeURIComponent(texto)}`);
                const resultados = await res.json();

                listaResultados.innerHTML = '';

                if (resultados.length === 0) {
                    listaResultados.innerHTML = '<div class="dropdown-item disabled text-muted">No se encontraron elementos finales</div>';
                } else {
                    resultados.forEach(item => {
                        const opcion = document.createElement('a');
                        opcion.href = '#';
                        opcion.className = 'dropdown-item text-wrap py-2 border-bottom';
                        opcion.innerHTML = `
                            <div class="fw-bold">${item.nombre}</div>
                            <small class="text-muted d-block">${item.ruta_completa}</small>
                        `;

                        // Al hacer clic en una opción
                        opcion.addEventListener('click', (ev) => {
                            ev.preventDefault();
                            inputBuscador.value = item.nombre;
                            inputOcultoB.value = item.id;
                            listaResultados.style.display = 'none';
                            btnEnviarBuscador.disabled = false;
                        });

                        listaResultados.appendChild(opcion);
                    });
                }

                listaResultados.style.display = 'block';
            } catch (error) {
                console.error("Error buscando elementos:", error);
            }
        }, 300);
    });

    /*
    *** Enviar el SO
    */
    btnEnviarBuscador.addEventListener('click', () => {
        const idSeleccionado = inputOcultoB.value;
        const nombreSeleccionado = inputBuscador.value;

        console.log("ID Buscador:", idSeleccionado);
        console.log("Nombre Buscador:", nombreSeleccionado);

        // confirm(`Selección desde Buscador:\nID: ${idSeleccionado}\nNombre: ${nombreSeleccionado}`);
//        showMessage("warning", "Sujeto Obligado seleccionado:\nID: ${idSeleccionado}\nNombre: ${nombreSeleccionado}");
        mostrarConfirmacion(idSeleccionado,nombreSeleccionado);
    });

    // Ocultar la lista si el usuario hace clic fuera del buscador
    document.addEventListener('click', (e) => {
        if (!inputBuscador.contains(e.target) && !listaResultados.contains(e.target)) {
            listaResultados.style.display = 'none';
        }
    });

    // MENSAJE SELECCION

    const modal = document.getElementById("confirmModal");
    const btnAceptar = document.getElementById("btnAceptar");
    const btnCancelar = document.getElementById("btnCancelar");
    const parrafo = document.getElementById("sujetoSeleccionado");
    var padronSeleccionado = "";

    function mostrarConfirmacion(idPadron, nombrePadron) {
        parrafo.innerText = nombrePadron;
        padronSeleccionado = nombrePadron;
        modal.classList.add("active");
    }

    btnAceptar.addEventListener("click", function () {
        const cuestionario = btnAceptar.value; // Obtener id
        window.location.href = `/aviso-de-privacidad/${cuestionario}/iniciar/?nombrePadron=${encodeURIComponent(padronSeleccionado)}`;
    });

    // btnAceptar.addEventListener(
    //     "click",
    //     async (e) => {
    //         const cuestionario = btnAceptar.value; // Obtener id
    //
    //         const response =
    //             await fetch(
    //                 `/aviso-de-privacidad/${cuestionario}/`,
    //                 {
    //                     method: "PUT",
    //                     headers: {
    //                         "X-CSRFToken": getCSRFToken()
    //                     },
    //                     body: JSON.stringify({
    //                         nombrePadron: padronSeleccionado
    //                     })
    //                 }
    //             );
    //
    //         const data = await response.json();
    //
    //         if (!response.ok || !data.success) {
    //             alert(data.error ||"Error al cargar SO en cuestionario");
    //             return;
    //         }
    //
    //     }
    // );

    // Ocultar panel
    btnCancelar.addEventListener("click", function () {
        modal.classList.remove("active");
    });

    function getCSRFToken() {
        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        )?.value;
    }
});
