const searchInput = document.getElementById("marketSearchInput");
const priceFilter = document.getElementById("priceFilter");
const sellerFilter = document.getElementById("sellerFilter");
const inStockOnly = document.getElementById("inStockOnly");
const sortBy = document.getElementById("sortBy");
const productList = document.getElementById("productList");

function applyFilters() {
    const searchValue = searchInput.value.toLowerCase();
    const priceValue = priceFilter.value;
    const sortValue = sortBy.value;

    let cards = Array.from(document.querySelectorAll(".product-card"));

    cards.forEach(card => {
        const title = card.dataset.title;
        const desc = card.dataset.desc;
        const price = parseFloat(card.dataset.price);
        const seller = card.dataset.seller;
        const quantity = parseInt(card.dataset.quantity);

        let visible = true;

        if (!title.includes(searchValue) && !desc.includes(searchValue)) visible = false;
        if (priceValue === "low" && price >= 20) visible = false;
        if (priceValue === "mid" && (price < 20 || price > 30)) visible = false;
        if (priceValue === "high" && price <= 30) visible = false;

        card.style.display = visible ? "block" : "none";
    });

    if (sortValue) {
        cards.sort((a, b) => {
            const priceA = parseFloat(a.dataset.price);
            const priceB = parseFloat(b.dataset.price);
            const nameA = a.dataset.title;
            const nameB = b.dataset.title;

            switch (sortValue) {
                case "price-asc":
                    return priceA - priceB;
                case "price-desc":
                    return priceB - priceA;
                case "name-asc":
                    return nameA.localeCompare(nameB);
                case "name-desc":
                    return nameB.localeCompare(nameA);
                default:
                    return 0;
            }
        });

        cards.forEach(card => productList.appendChild(card));
    }
}

searchInput.addEventListener("input", applyFilters);
priceFilter.addEventListener("change", applyFilters);
sortBy.addEventListener("change", applyFilters);