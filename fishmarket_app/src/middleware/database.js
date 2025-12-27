const fs = require("fs");
const { get } = require("http");
const path = require("path");


const USERS_FILE = path.join(__dirname, "..", "json", "users.json");
const POSTS_FILE = path.join(__dirname, "..", "json", "posts.json");

function loadUsers() {
    if (!fs.existsSync(USERS_FILE)) {
        return [];
    }

    try {
        const data = fs.readFileSync(USERS_FILE, "utf8");
        return JSON.parse(data);
    } catch (err) {
        console.error("Error reading users.json:", err);
        return [];
    }
}

function saveUsers(users) {
    try {
        fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf8");
    } catch (err) {
        console.error("Error writing users.json:", err);
    }
}

function findUser(email) {
    const users = loadUsers();
    return users.find(u => u.email === email);
}

function addUser(email, password, role, forename, surname) {
    const users = loadUsers();

    users.push({
        email,
        password,
        role,
        forename,
        surname
    });

    saveUsers(users);
}

function getPosts() {
    if (!fs.existsSync(POSTS_FILE)) {
        return [];
    }
    try {
        const data = fs.readFileSync(POSTS_FILE, "utf8");
        return JSON.parse(data);
    }
    catch (err) {
        console.error("Error reading posts.json:", err);
        return [];
    }
}

function getSales() {
    const SALES_FILE = path.join(__dirname, "..", "json", "sales.json");
    if (!fs.existsSync(SALES_FILE)) {
        return [];
    }
    try {
        const data = fs.readFileSync(SALES_FILE, "utf8");
        return JSON.parse(data);
    } catch (err) {
        console.error("Error reading sales.json:", err);
        return [];
    }
}

function updateUser(email, updatedData, callback) {
    const users = loadUsers();
    const userIndex = users.findIndex(u => u.email === email);
    if (userIndex === -1) {
        return callback(new Error("User not found"));
    }
    users[userIndex] = { ...users[userIndex], ...updatedData };
    saveUsers(users);
    callback(null);
}

function validateUser(email, password) {
    const user = findUser(email);
    if (!user || user.password !== password) {
        return false;
    }
    return true;
}


function createListing(fishType, price, quantity, description, imagePath, sellerEmail, sellerName) {
    const posts = getPosts();

    const newListing = {
        id: posts.length + 1,
        email: sellerEmail,
        name: fishType,
        seller: sellerName,
        description: description,
        quantity: parseInt(quantity),
        image: imagePath,
        price: parseFloat(price)
    };

    posts.push(newListing);

    fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf8");
}


function editListing(id, fishType, price, quantity, description, imagePath) {
    const posts = getPosts();
    const listingIndex = posts.findIndex(post => post.id === parseInt(id));
    
    if (listingIndex === -1) {
        throw new Error("Listing not found");
    }

    posts[listingIndex] = {
        ...posts[listingIndex],
        name: fishType,
        price: parseFloat(price),
        quantity: parseInt(quantity),
        description: description,
        image: imagePath
    };

    fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf8");
}


function deleteListing(id) {
    const posts = getPosts();
    const listingIndex = posts.findIndex(post => post.id === parseInt(id));
    if (listingIndex === -1) {
        throw new Error("Listing not found");
    }

    posts[listingIndex].is_deleted = true;
    fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2), "utf8");
}

module.exports = {
    loadUsers,
    saveUsers,
    findUser,
    addUser,
    getPosts,
    getSales,
    updateUser,
    validateUser,
    createListing,
    editListing,
    deleteListing
};
