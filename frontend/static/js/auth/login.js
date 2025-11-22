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
            const response = await fetch("/auth/login", {
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

            // Redirección según el rol
            if (rol === "ADMINISTRADOR") {
                window.location.href = "/admin/dashboard";   // luego crearemos estas vistas
            } else if (rol === "TUTOR") {
                window.location.href = "/tutor/dashboard";
            } else if (rol === "VERIFICADOR") {
                window.location.href = "/verificador/dashboard";
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
});

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggle-password");
    const passwordInput = document.getElementById("contrasena");

    if (toggle && passwordInput) {
        toggle.addEventListener("click", () => {
            const type = passwordInput.type === "password" ? "text" : "password";
            passwordInput.type = type;
        });
    }
});
