const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 8080;

app.use(express.static(path.join(__dirname, '/')));
app.use(express.json());

app.get('/getSettings', (req, res) => {
    const filename = path.join(__dirname, 'UserPrefs.json');

    fs.readFile(filename, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading from', filename, ':', err);
            return res.status(500).json({ error: 'Internal Server Error' });
        }

        try {
            const settings = JSON.parse(data);
            res.json(settings);
        } catch (parseError) {
            console.error('Error parsing JSON:', parseError);
            res.status(500).json({ error: 'Error parsing JSON' });
        }
    });
});

app.post('/saveSettings', (req, res) => {
    const settings = req.body;
    const filename = path.join(__dirname, 'UserPrefs.json');

    const jsonString = JSON.stringify(settings, null, 2);

    fs.writeFile(filename, jsonString, 'utf8', (err) => {
        if (err) {
            console.error('Error writing to', filename, ':', err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            console.log(filename, 'has been saved.');
            res.json({ message: 'Settings saved successfully' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
