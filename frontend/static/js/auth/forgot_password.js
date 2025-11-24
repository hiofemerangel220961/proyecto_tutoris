document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("forgot-form");
    const errorBox = document.getElementById("forgot-error");
    const successBox = document.getElementById("forgot-success");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        errorBox.style.display = "none";
        errorBox.textContent = "";
        successBox.style.display = "none";
        successBox.textContent = "";

        const correo = document.getElementById("correo").value.trim();

        try {
            const response = await fetch("/auth/forgot-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ correo }),
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
