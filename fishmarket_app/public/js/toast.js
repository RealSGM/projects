window.showToast = function(message, type = "error") {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.innerText = message;

    toast.style.display = "block";

    if (type === "success") {
        toast.style.background = "#e8ffe8";
        toast.style.color = "#076b07";
    } else {
        toast.style.background = "#ffe6e6";
        toast.style.color = "#8b0000";
    }

    toast.classList.remove("hide");
    toast.classList.add("show");

    clearTimeout(toast._timeout);

    toast._timeout = setTimeout(() => {
        toast.classList.remove("show");
        toast.classList.add("hide");
        setTimeout(() => toast.style.display = "none", 300);
    }, 3500);
};