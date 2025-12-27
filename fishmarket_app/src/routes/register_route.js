const express = require('express');
const router = express.Router();
const db = require("../middleware/database");

router.get("/", (req, res) => {
    const msg = req.session.message;
    req.session.message = null;

    const req_data = {
        include_settings: false,
        active_tab: "register",
        header_name: 'Billingsgate Fish Market',
        message: msg
    };


    res.render("register.ejs", {
        req_data: req_data
    });
});


router.post('/', (req, res) => {
    const { email, password, confirm_password, role, forename, surname } = req.body;

    if (password !== confirm_password) {
        return res.json({
            success: false,
            type: "error",
            message: "Passwords do not match."
        });
    }

    const existingUser = db.findUser(email);
    if (existingUser) {
        return res.json({
            success: false,
            type: "error",
            message: "User already exists."
        });
    }
    db.addUser(email, password, role, forename, surname);

    req.session.message = "Registration successful! Please log in.";
    res.json({
        success: true,
        type: "success",
        message: "Registration Successful\nRedirecting to Login Page..."
    });
});


module.exports = router;
