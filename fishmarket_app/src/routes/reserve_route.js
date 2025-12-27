const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");

router.get("/", (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }

    const req_data = {
        include_settings: true,
        active_tab: "reserve",
        role: req.session.user.role,
        header_name: "Billingsgate Fish Market"
    };

    res.render("reserve", {message: null, data: req_data});
});

router.post("/", (req, res) => {
    const buyOrdersPath = path.join(__dirname, "..", "json", "buy_orders.json");
    let buyOrders = [];
    if (fs.existsSync(buyOrdersPath)) {
        const fileData = fs.readFileSync(buyOrdersPath);
        buyOrders = JSON.parse(fileData);
    }

    const { fishType, maxPrice, quantity, deliveryDay } = req.body;

    const id = buyOrders.length > 0 ? buyOrders[buyOrders.length - 1].id + 1 : 1;

    const data = {
        id: id,
        fish: fishType,
        maxPrice: parseFloat(maxPrice),
        quantity: parseInt(quantity),
        day: deliveryDay,
        status: "waiting"
    };

    buyOrders.push(data);
    fs.writeFileSync(buyOrdersPath, JSON.stringify(buyOrders, null, 2));

    res.redirect('/buy_orders');
});


module.exports = router;