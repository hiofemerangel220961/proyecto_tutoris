document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const correo = document.getElementById("correo").value;
        const contrasena = document.getElementById("contrasena").value;

        errorMessage.style.display = "none";
        errorMessage.textContent = "";

        try {
            // CAMBIO AQUÍ: La ruta ahora es /login (sin /auth)
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    correo: correo,
                    contrasena: contrasena,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                errorMessage.textContent = errorData.detail || "Error al iniciar sesión";
                errorMessage.style.display = "block";
                return;
            }

            const data = await response.json();
            const usuario = data.usuario;
            const rol = usuario.rol;

            // Redirección según el rol con email como query param
            if (rol === "ADMINISTRADOR") {
                window.location.href = `/admin/dashboard?email=${encodeURIComponent(usuario.correo)}`;
            } else if (rol === "TUTOR") {
                window.location.href = `/tutor/dashboard?email=${encodeURIComponent(usuario.correo)}`;
            } else if (rol === "VERIFICADOR") {
                window.location.href = `/verificador/dashboard?email=${encodeURIComponent(usuario.correo)}`;
            } else if (rol === "ESTUDIANTE") {
                // Por ahora no hay dashboard de estudiante, mostrar mensaje o redirigir a perfil
                alert("Inicio de sesión exitoso. El dashboard de estudiante está en desarrollo.");
                window.location.href = "/";
            } else {
                errorMessage.textContent = "Rol desconocido";
                errorMessage.style.display = "block";
            }

        } catch (err) {
            console.error(err);
            errorMessage.textContent = "Error de conexión con el servidor";
            errorMessage.style.display = "block";
        }
    });

    // Lógica para el botón de "ver contraseña" (el ojito)
    const toggle = document.getElementById("toggle-password");
    const passwordInput = document.getElementById("contrasena");

    if (toggle && passwordInput) {
        toggle.addEventListener("click", () => {
            const type = passwordInput.type === "password" ? "text" : "password";
            passwordInput.type = type;
        });
    }
});