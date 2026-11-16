document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('modal-eliminar');
    if (!el) return;
    const modal = new bootstrap.Modal(el);
    const form = document.getElementById('form-eliminar');
    const nombre = document.getElementById('modal-nombre');

    // Delegacion de eventos: sigue funcionando cuando DataTables cambia de pagina
    document.addEventListener('click', (e) => {
        const boton = e.target.closest('.btn-eliminar');
        if (!boton) return;
        form.action = boton.dataset.url;
        nombre.textContent = boton.dataset.nombre;
        modal.show();
    });
});