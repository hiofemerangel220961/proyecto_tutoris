document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-sidebar');
    
    // Clave para localStorage
    const STORAGE_KEY = 'tutoris_sidebar_state';

    // 1. Cargar estado guardado
    const savedState = localStorage.getItem(STORAGE_KEY);
    if (savedState === 'collapsed') {
        sidebar.classList.add('collapsed');
    }

    // 2. Función toggle
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            
            // Guardar estado
            if (sidebar.classList.contains('collapsed')) {
                localStorage.setItem(STORAGE_KEY, 'collapsed');
            } else {
                localStorage.setItem(STORAGE_KEY, 'expanded');
            }
        });
    }
});