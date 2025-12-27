const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

router.get('/', (req, res) => {
    const req_data = {
        include_settings: true,
        active_tab: 'messages',
        role: req.session.user?.role,
        header_name: 'Billingsgate Fish Market'
    };
    res.render('messages', {
        data: req_data,
    });
});

router.get('/:id', (req, res) => {
    const filePath = path.join(__dirname, '..', '..', 'public', 'json', 'messages.json');
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    const dm = data.find(m => m.id === req.params.id);

    if (!dm) return res.status(404).send('Conversation not found');

    const req_data = {
        include_settings: true,
        active_tab: 'messages',
        role: req.session.user?.role,
        header_name: dm.name
    };

    res.render('direct_messages', {
        dm,
        data: req_data,
    });
});

module.exports = router;
