document.querySelectorAll(".faq-question").forEach(btn => {
    btn.addEventListener("click", () => {
        const answer = btn.nextElementSibling;
        const icon = btn.querySelector("i");

        answer.style.display =
            answer.style.display === "block" ? "none" : "block";

        icon.classList.toggle("fa-chevron-down");
        icon.classList.toggle("fa-chevron-up");
    });
});
