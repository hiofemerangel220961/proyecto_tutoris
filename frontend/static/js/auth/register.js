document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    const errorBox = document.getElementById("register-error");
    const successBox = document.getElementById("register-success");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        errorBox.style.display = "none";
        errorBox.textContent = "";
        successBox.style.display = "none";
        successBox.textContent = "";

        const nombres = document.getElementById("nombres").value.trim();
        const apellidos = document.getElementById("apellidos").value.trim();
        const correo = document.getElementById("correo").value.trim();
        const rol = document.getElementById("rol_solicitado").value;

        if (!rol) {
            errorBox.textContent = "Debe seleccionar un rol.";
            errorBox.style.display = "block";
            return;
        }

        try {
            const response = await fetch("/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    nombres: nombres,
                    apellidos: apellidos,
                    correo: correo,
                    rol_solicitado: rol,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                errorBox.textContent = data.detail || "Error al enviar la solicitud.";
                errorBox.style.display = "block";
                return;
            }

            successBox.textContent = data.mensaje;
            successBox.style.display = "block";
            form.reset();

        } catch (err) {
            console.error(err);
            errorBox.textContent = "Error de conexión con el servidor.";
            errorBox.style.display = "block";
        }
    });
});
