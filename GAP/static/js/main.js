// main.js

import { initNavigation } from './ui/navigation.js';
import { initMessages } from './ui/messages.js';

initNavigation();
initMessages();

// cargar lógica por sección
console.log("MAIN OK");

const section = parseInt(document.body.dataset.section);
console.log("Sección:", section);

import(`./sections/section${section}.js`)
    .then(module => {
        console.log("MÓDULO:", module);

        // CSS para los formularios
        const css = document.createElement("link");
        css.rel = "stylesheet";
        css.href = "/static/css/formularios.css";
        document.head.appendChild(css);


        if (typeof module.init === "function") {
            module.init();
        } else {
            console.warn("No tiene init()", module);
        }
    })
    .catch(err => {
        console.warn(`No existe JS para section ${section}`, err);
    });

