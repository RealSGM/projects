document.addEventListener("DOMContentLoaded", () => {
    const darkToggle = document.getElementById("toggle-darkmode");

    const savedTheme = localStorage.getItem("theme") || "light";

    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark");
        if (darkToggle) darkToggle.checked = true;
    } else {
        document.documentElement.classList.remove("dark");
        if (darkToggle) darkToggle.checked = false;
    }

    if (darkToggle) {
        darkToggle.addEventListener("change", () => {
            const enableDark = !darkToggle.checked;

            document.documentElement.classList.toggle("dark", enableDark);

            localStorage.setItem("theme", enableDark ? "dark" : "light");
        });
    }

    const fontSelect = document.getElementById("font-size-select");

    const savedFont = localStorage.getItem("font-size") || "normal";
    fontSelect.value = savedFont;
    applyFontSize(savedFont);

    fontSelect.addEventListener("change", () => {
        const value = fontSelect.value;
        localStorage.setItem("font-size", value);
        applyFontSize(value);
    });

    function applyFontSize(size) {
        document.documentElement.classList.remove("font-large", "font-xl");

        if (size === "large") {
            document.documentElement.classList.add("font-large");
        }
        if (size === "xl") {
            document.documentElement.classList.add("font-xl");
        }
    }
});
