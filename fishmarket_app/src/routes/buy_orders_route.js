const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");

router.get("/", (req, res) => {
    const ordersPath = path.join(__dirname, "..", "json", "buy_orders.json");

    const req_data = {
        include_settings: true,
        active_tab: "reserve",
        role: req.session.user.role,
        header_name: "Billingsgate Fish Market"
    };

    fs.readFile(ordersPath, "utf8", (err, data) => {
        if (err) {
            console.error("Error reading buy_orders.json:", err);
            return res.status(500).send("Internal Server Error");
        }
        const orders = JSON.parse(data);
        
        res.render("buy_orders", { data: req_data, orders: orders });
    });
});

router.post("/delete", (req, res) => {
    const id = parseInt(req.body.id);
    const ordersPath = path.join(__dirname, "..", "json", "buy_orders.json");

    fs.readFile(ordersPath, "utf8", (err, data) => {
        if (err) return res.sendStatus(500);

        const orders = JSON.parse(data);

        const order = orders.find(o => o.id === id);
        if (!order) return res.sendStatus(404);

        order.is_deleted = true;

        fs.writeFile(
            ordersPath,
            JSON.stringify(orders, null, 2),
            err => {
                if (err) return res.sendStatus(500);
                res.sendStatus(200);
            }
        );
    });
});

module.exports = router;
