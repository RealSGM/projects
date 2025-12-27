document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("menu-toggle");
    const dropdown = document.getElementById("menu-dropdown");
    const overlay = document.getElementById("menu-overlay");

    function openMenu() {
        dropdown.classList.add("show");
        overlay.style.pointerEvents = "auto";
        toggle.classList.add("active");
    }

    function closeMenu() {
        dropdown.classList.remove("show");
        overlay.style.pointerEvents = "none";
        toggle.classList.remove("active");
    }

    toggle?.addEventListener("click", (e) => {
        e.stopPropagation();

        if (dropdown.classList.contains("show")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    overlay?.addEventListener("click", closeMenu);
});
