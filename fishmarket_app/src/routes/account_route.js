const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");
const { getPosts, getSales, updateUser, validateUser } = require("../middleware/database");

router.get("/", (req, res) => {
    const filePath = path.join(__dirname, "..", "json", "orders.json");

    fs.readFile(filePath, "utf8", (err, data) => {
        if (err) return res.status(500).send("Error loading orders");

        const ordersData = JSON.parse(data);
        const orders = ordersData.find(e => e.email === req.session.user.email) || { orders: [] };

        const productsList = getPosts();

        let filteredProducts = [];
        orders.orders.forEach(order => {
            order.products.forEach(orderProduct => {
                const product = productsList.find(p => p.id === orderProduct.id);
                if (product) filteredProducts.push(product);
            });
        });

        let salesData = getSales().filter(s => s.email === req.session.user.email);

        const req_data = {
            include_settings: true,
            active_tab: "account",
            role: req.session.user.role,
            header_name: 'Billingsgate Fish Market',
        };

        const message = req.session.message;
        const type = req.session.messageType;
        req.session.message = null;
        req.session.messageType = null;

        res.render("account", {
            user: req.session.user,
            orders: orders.orders,
            products: filteredProducts,
            stats: salesData[0] || { totalSales: 0, totalRevenue: 0, productsListed: 0 },
            data: req_data,
            message,
            type,
        });
    });
});

router.post("/update-profile", (req, res) => {
    const { forename, surname, confirm_password } = req.body;

    const valid = validateUser(req.session.user.email, confirm_password);

    if (!valid) {
        return res.json({ success: false, type: "error", message: "Incorrect password" });
    }

    updateUser(req.session.user.email, { forename, surname }, (err) => {
        if (err) {
            return res.json({ success: false, type: "error", message: "Error updating profile" });
        }

        req.session.user.forename = forename;
        req.session.user.surname = surname;

        res.json({ success: true, type: "success", message: "Profile updated successfully" });
    });
});

router.post("/update-password", (req, res) => {
    const { current_password, new_password, confirm_new_password } = req.body;

    if (new_password !== confirm_new_password) {
        return res.json({ success: false, type: "error", message: "Passwords do not match" });
    }

    const valid = validateUser(req.session.user.email, current_password);

    if (!valid) {
        return res.json({ success: false, type: "error", message: "Incorrect current password" });
    }

    updateUser(req.session.user.email, { password: new_password }, (err) => {
        if (err) {
            return res.json({ success: false, type: "error", message: "Error updating password" });
        }

        res.json({ success: true, type: "success", message: "Password updated successfully" });
    });
});

module.exports = router;
