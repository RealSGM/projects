document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("registerForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            email: form.querySelector("input[name='email']").value,
            password: form.querySelector("input[name='password']").value,
            confirm_password: form.querySelector("input[name='confirm_password']").value,
            role: form.querySelector("input[name='role']:checked")?.value,
            forename: form.querySelector("input[name='first_name']").value,
            surname: form.querySelector("input[name='surname']").value
        };

        const res = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        showToast(result.message, result.type);

        if (result.success) {
            setTimeout(() => {
                window.location.href = "/login";
            }, 1200);
        }

    });

});
