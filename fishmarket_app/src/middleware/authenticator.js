const checkAuth = (req, res, next) => {
    if (!req.session.user) {
        return res.redirect("/login");
    }

    if (req.session.cookie.expires < Date.now()) {
        req.session.destroy();
        return res.redirect("/login");
    }
    return next();
};

const forceLogout = (req, res, next) => {
    if (req.session.user) {
        req.session.destroy();
    }
    if (next) {
        return next();
    }
};


module.exports = {
    checkAuth,
    forceLogout,
};
