const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const jwt = require('jsonwebtoken');
const onFinished = require('on-finished');
const port = 3000;

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const SESSION_KEY = 'Authorization';
const JWT_SECRET = 'QW5hc3Rhc2lpYToxOTIy';

const users = [
    {
        login: 'BohdanM',
        password: '1922',
        username: 'Bohdan',
    }
];

app.use((req, res, next) => {
    const authHeader = req.get(SESSION_KEY); 
    if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.split(' ')[1];
        try {
            const decoded = jwt.verify(token, JWT_SECRET); 
            req.session = decoded; 
        } catch (err) {
            return res.status(401).json({ message: 'Invalid token' });
        }
    } else {
        req.session = {};
    }
    next();
});

app.get('/', (req, res) => {
    if (req.session.username) {
        return res.json({
            username: req.session.username,
            logout: 'http://localhost:3000/logout'
        });
    }
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.get('/logout', (req, res) => {
    res.redirect('/');
});

app.post('/api/login', (req, res) => {
    const { login, password } = req.body;

    const user = users.find((user) => user.login === login && user.password === password);

    if (user) {
        const token = jwt.sign({ login: user.login, username: user.username }, JWT_SECRET, { expiresIn: '1h' });
        return res.json({ token });
    }

    res.status(401).send('Invalid credentials');
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});
