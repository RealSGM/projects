const express = require("express");
const router = express.Router();

router.post("/add", (req, res) => {
    const { id, name, owner, image, price, quantity } = req.body;

    if (!req.session.cart) req.session.cart = [];

    const existing = req.session.cart.find(item => item.id === id);

    if (existing) {
        existing.quantity += parseInt(quantity);
    } else {
        req.session.cart.push({
            id,
            name,
            owner,
            image,
            price: parseFloat(price),
            quantity: parseInt(quantity)
        });
    }

    return res.json({ success: true });
});
router.post("/clear", (req, res) => {
    req.session.cart = [];
    res.json({ success: true });
});

router.post("/remove", (req, res) => {
    const { id } = req.body;

    if (!req.session.cart) req.session.cart = [];

    const item = req.session.cart.find(i => i.id === id);

    if (item) {
        req.session.lastRemovedItem = { ...item };  
        req.session.showUndo = true;               
    }

    req.session.cart = req.session.cart.filter(i => i.id !== id);

    return res.json({ success: true });
});
router.post("/undo", (req, res) => {
    const last = req.session.lastRemovedItem;

    if (!last) {
        return res.json({ success: false });
    }

    req.session.cart.push(last);

    req.session.lastRemovedItem = null;
    req.session.showUndo = false;  

    res.json({ success: true });
});

module.exports = router;