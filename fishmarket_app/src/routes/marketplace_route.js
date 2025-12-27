const express = require("express");
const router = express.Router();
const { getPosts } = require("../middleware/database");

router.get("/", (req, res) => {
    let productsList = getPosts();

    const req_data = {
        include_settings: true,
        active_tab: "marketplace",
        role: req.session.user.role,
        header_name: "Billingsgate Fish Market"
    };

    res.render("marketplace", {
        products: productsList,
        email: req.session.user.email,
        data: req_data
    });
});


module.exports = router;
