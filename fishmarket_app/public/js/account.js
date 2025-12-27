document.addEventListener("DOMContentLoaded", () => {

    const profileForm = document.querySelector("form[action='/account/update-profile']");
    const passwordForm = document.querySelector("form[action='/account/update-password']");

    const handleSubmit = async (form, url) => {
        if (!form) return;

        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const body = Object.fromEntries(formData.entries());

            const res = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });

            const result = await res.json();

            showToast(result.message, result.type);

            setTimeout(() => {
                window.location.href = "/account";
            }, 800);
        });
    };

    handleSubmit(profileForm, "/account/update-profile");
    handleSubmit(passwordForm, "/account/update-password");
});
