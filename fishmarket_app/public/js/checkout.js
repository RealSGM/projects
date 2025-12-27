document.addEventListener("click", async e => {
    if (!e.target.closest(".delete-btn")) return;

    const btn = e.target.closest(".delete-btn");
    const id = btn.dataset.id;

    const res = await fetch("/cart/remove", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });

    const result = await res.json();

    if (result.success) {
        window.location.reload();   
    }
});

document.addEventListener("click", e => {
    if (!e.target.classList.contains("plus") && !e.target.classList.contains("minus")) return;

    const pill = e.target.closest(".qty-pill");
    const valueElement = pill.querySelector(".pill-value");

    const itemElement = pill.closest(".basket-item");
    const priceElement = itemElement.querySelector(".item-price");
    const subtotalElement = itemElement.querySelector(".item-subtotal");

    let quantity = parseInt(valueElement.textContent);
    const price = parseFloat(priceElement.dataset.price);

    if (e.target.classList.contains("plus")) quantity++;
    if (e.target.classList.contains("minus") && quantity > 1) quantity--;

    valueElement.textContent = quantity;

    const newSubtotal = (price * quantity).toFixed(2);
    subtotalElement.textContent = `£${newSubtotal}`;

    updateBasketTotals();
});

document.addEventListener("DOMContentLoaded", () => {
    const undoBtn = document.getElementById("undo-btn");

    undoBtn.addEventListener("click", () => {
        fetch("/cart/undo", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                clearTimeout(window.undoTimeout);
                
                location.reload();
            }
        });
    });
});

function updateBasketTotals() {
    let totalItems = 0;
    let totalPrice = 0;

    document.querySelectorAll(".basket-item").forEach(item => {
        const qty = parseInt(item.querySelector(".pill-value").textContent);
        const price = parseFloat(item.querySelector(".item-price").dataset.price);

        totalItems += qty;
        totalPrice += qty * price;
    });

    document.querySelector(".subtotal").innerHTML =
        `Total (${totalItems} Items): <strong>£${totalPrice.toFixed(2)}</strong>`;
}

document.addEventListener("DOMContentLoaded", () => {
    const paymentButtons = document.querySelectorAll(".payment-buttons .pay");
    const popup = document.getElementById("payment-popup");

    paymentButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            popup.classList.remove("hidden");
            popup.classList.add("show");

            fetch("/cart/clear", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    setTimeout(() => {
                        popup.classList.remove("show");

                        setTimeout(() => {
                            popup.classList.add("hidden");
                            window.location.reload();
                        }, 250);
                    }, 2000);
                });
        });
    });
});