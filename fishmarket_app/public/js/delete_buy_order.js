document.querySelectorAll('.delete-order-btn').forEach(btn => {
    btn.addEventListener('click', async () => {

        const id = btn.dataset.id;

        await fetch('/buy_orders/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id })
        });

        location.reload();

    });
});
