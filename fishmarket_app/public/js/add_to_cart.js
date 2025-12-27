document.addEventListener("click", async e => {
    if (!e.target.classList.contains("add")) return;

    const card = e.target.closest(".card");

    const id = card.dataset.id;
    const owner = card.dataset.owner;
    const name = card.querySelector(".title").innerText;
    const image = card.querySelector("img").src;
    const price = card.querySelector(".price-tag").innerText.replace("$", "");
    const quantity = card.querySelector(".qty-input").value;

    const response = await fetch("/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, name, owner, image, price, quantity })
    });

    const result = await response.json();

    if (result.success) {
        document.getElementById("cart-modal").classList.add("show");
        document.getElementById("cartModalName").innerText = name;
        document.getElementById("cartModalImg").src = image;
        document.getElementById("cartModalPrice").innerText = `£${price}`;
        document.getElementById("cartModalQty").innerText = quantity;
    }
});

document.getElementById("continueShoppingBtn")
    .addEventListener("click", () => {
        document.getElementById("cart-modal").classList.remove("show")
    })

document.addEventListener("click", e => {

    if (e.target.classList.contains("plus")) {
        const input = e.target.parentElement.querySelector(".qty-input");
        const stock = parseInt(input.dataset.stock, 10);

        let value = parseInt(input.value) || 1;
        if (value < stock) value = value + 1;

        input.value = value;
    }

    if (e.target.classList.contains("minus")) {
        const input = e.target.parentElement.querySelector(".qty-input");

        let value = parseInt(input.value) || 1;
        if (value > 1) value = value - 1;

        input.value = value;
    }
});


function addToBasket(item) {
    let basket = JSON.parse(localStorage.getItem("basket")) || [];
    basket.push(item);
    localStorage.setItem("basket", JSON.stringify(basket));
}