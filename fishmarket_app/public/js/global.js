document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark");
    }

    const darkToggle = document.getElementById("toggle-darkmode");

    if (darkToggle) {
        darkToggle.checked = document.documentElement.classList.contains("dark");

        darkToggle.addEventListener("change", () => {
            document.documentElement.classList.toggle("dark");

            const isDark = document.documentElement.classList.contains("dark");
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }
});
