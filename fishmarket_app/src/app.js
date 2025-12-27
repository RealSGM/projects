const express = require('express');
const favicon = require('serve-favicon');
const path = require('path');
const fs = require("fs");
const session = require('express-session');
const app = express();
const { checkAuth, forceLogout, checkRole } = require('./middleware/authenticator.js');

const PORT = 3000;

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.static("public"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(favicon(path.join(__dirname, "../public", "favicon.ico")));

app.use(session({
    secret: 'secretkey123', 
    resave: false,
    saveUninitialized: true,
    cookie: {
        maxAge: 1000 * 60 * 60 * 24 
    }
}));

app.use((req, res, next) => {
    if (!req.session.cart) {
        req.session.cart = [];
    }
    next();
});


loginRoute = require('./routes/login_route');
registerRoute = require('./routes/register_route');
logoutRoute = require('./routes/logout_route');
marketplaceRoute = require('./routes/marketplace_route');
listingsRoute = require('./routes/listings_route');
accountRoute = require('./routes/account_route');
messagesRoute = require('./routes/messages_route');
reserveRoute = require('./routes/reserve_route');
buyOrdersRoute = require('./routes/buy_orders_route');
cartRoute = require("./routes/cart_route");

app.use("/login", forceLogout, loginRoute);
app.use("/register", forceLogout, registerRoute);
app.use("/marketplace", checkAuth, marketplaceRoute);
app.use("/logout", logoutRoute);
app.use("/listings", checkAuth, listingsRoute);
app.use("/account", checkAuth, accountRoute);
app.use("/messages", checkAuth, messagesRoute);
app.use("/reserve", checkAuth, reserveRoute);
app.use("/buy_orders", checkAuth, buyOrdersRoute);
app.use("/cart", checkAuth, cartRoute);

app.get('/', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    res.redirect('/marketplace');
});

app.get("/checkout", checkAuth, (req, res) => {
    const req_data = {
        include_settings: true,
        active_tab: "checkout",
        role: req.session.user.role,
        header_name: "Billingsgate Fish Market",
        cart: req.session.cart || [],
        showUndo: req.session.showUndo || false 
    };

     req.session.showUndo = false;

    res.render("checkout", { message: null, data: req_data });
});



app.get("/:page", (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    
    const page = req.params.page;
    const filePath = path.join(__dirname, "views", `${page}.ejs`);

    const req_data = {
        include_settings: true,
        active_tab: page,
        role: req.session.user.role,
        header_name: 'Billingsgate Fish Market'
    };

    if (fs.existsSync(filePath)) {
        res.render(page, {message: req.session.message || null, data: req_data });
    } else {
        res.redirect("/marketplace");
    }
});


app.listen(PORT, () => {
    console.log(`My app listening on PORT ${PORT}!`);
});


