const express = require('express');
const router = express.Router();
const db = require("../middleware/database");


router.get("/", (req, res) => {

    if (req.session && req.session.user) {
        return res.redirect('/marketplace');
    }

    let msg = null;

    if (req.session) {
        msg = req.session?.message || null;
        req.session.message = null;
    }

    const req_data = {
        include_settings: false,
        active_tab: "login",
        header_name: "Billingsgate Fish Market"
    };
    
    res.render("login.ejs", {
        message: msg,
        data: req_data,
    });
});


router.post('/', (req, res) => {
    const { email, password} = req.body;

    const user = db.findUser(email);
    if (!user || user.password !== password) {
        return res.json({
            success: false,
            type: "error",
            message: "Invalid email or password."
        });
    }

    req.session.user = {
        email: user.email,
        forename: user.forename,
        surname: user.surname,
        role: user.role,
        loggedIn: true
    };

    res.json({
        success: true,
        type: "success",
        message: "Login Successful! Redirecting to Dashboard..."
    });
});

module.exports = router;