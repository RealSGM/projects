document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = form.querySelector("input[name='email']").value;
        const password = form.querySelector("input[name='password']").value;

        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const result = await res.json();

        showToast(result.message, result.type);

        if (result.success) {
            setTimeout(() => {
                window.location.href = "/marketplace";
            }, 800);
        }
    });

});
