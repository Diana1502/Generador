// ui/messages.js

export function initMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 3000);
    });
}

export function showMessage(message, type = "error") {
    const container = document.getElementById("message-container");

    if (!container) return;

    const msg = document.createElement("div");
    msg.className = `alert alert-${type}`;
    msg.textContent = message;

    container.appendChild(msg);

    setTimeout(() => {
        msg.remove();
    }, 3000);
}