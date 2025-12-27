const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");
const db = require("../middleware/database");
const multer = require("multer");
const upload = multer({
    dest: path.join(__dirname, "..", "..", "public", "images")
});

router.get("/edit/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const filePath = path.join(__dirname, "..", "json", "posts.json");

    fs.readFile(filePath, "utf8", (err, data) => {
        if (err) return res.status(500).send("Error loading listing");

        const listings = JSON.parse(data);
        const listing = listings.find(p => p.id === id);

        if (!listing) {
            return res.status(404).send("Listing not found");
        }

        const req_data = {
            active_tab: "editlisting",
            include_settings: true,
            role: req.session.user.role,
            header_name: "Billingsgate Fish Market"
        };

        res.render("edit_listing", { listing, data: req_data });
    });
});

router.post("/edit/:id", upload.single("image"), (req, res) => {
    const id = parseInt(req.params.id);
    const { fishType, price, quantity, description } = req.body;
    const imageUrl = req.file
        ? `/images/${req.file.filename}`
        : `/images/cod.JPG`;

    db.editListing(id, fishType, price, quantity, description, imageUrl);
    
    res.redirect(`/listings/self`);
});


router.get("/create", (req, res) => {

    const listing = {
        id: null,
        name: "",
        price: "",
        quantity: 1,
        description: ""
    };

    const req_data = {
        active_tab: "createlisting",
        include_settings: true,
        role: req.session.user.role,
        header_name: "Billingsgate Fish Market"
    };

    res.render("create_listing", { listing: listing, data: req_data });
});


router.get("/self", (req, res) => {
    const filePath = path.join(__dirname, "..", "json", "posts.json");

    fs.readFile(filePath, "utf8", (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send("Error loading products");
        }

        const products = JSON.parse(data);

        const userProducts = products.filter(product => product.email === req.session.user.email);

        const req_data = {
            active_tab: "mylistings",
            include_settings: true,
            role: req.session.user.role,
            header_name: "Billingsgate Fish Market"
        };

        res.render("marketplace", {
            products: userProducts,
            email: req.session.user.email,
            data: req_data
        });
    }); 
});

router.post("/create_listing", upload.single("image"), (req, res) => {
    const sellerName = req.session.user.forename + " " + req.session.user.surname;
    const sellerEmail = req.session.user.email;

    const { fishType, price, quantity, description } = req.body;

    const imageUrl = req.file
    ? `/images/${req.file.filename}`
    : `/images/cod.JPG`;

    db.createListing(fishType, price, quantity, description, imageUrl, sellerEmail, sellerName);

    res.redirect("/listings/self");
});

router.post("/delete/:id", (req, res) => {
    const id = parseInt(req.params.id);
    db.deleteListing(id);
    res.redirect("/listings/self");
});

module.exports = router;
