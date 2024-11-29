const axios = require('axios');
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const port = 3000;

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const DOMAIN = 'dev-4piqjyt8i3e2h2ww.eu.auth0.com'; 
const CLIENT_ID = 'F1e6bh022aCtnRgnSF2dtK7HGU4cw7Xz'; 
const CLIENT_SECRET = 'X8Q2ghz0W6rT7mUPrMSV-MdrwSmpN-Vu9iRGGyGjaVwUn_IS-ilFnvrRdqv5VLnU'; 
const SESSION_KEY = 'Authorization';

const sessions = {};

// Middleware для управління сессіями
app.use((req, res, next) => {
    let sessionId = req.get(SESSION_KEY);
    
    if (sessionId && sessions[sessionId]) {
        req.session = sessions[sessionId];
        console.log(`Existing session found for ID: ${sessionId}`);
    } else {
        sessionId = Math.random().toString(36).substring(2);
        req.session = {};
        sessions[sessionId] = req.session;
        console.log(`Initialized new session with ID: ${sessionId}`);
    }

    req.sessionId = sessionId;
    res.set(SESSION_KEY, sessionId);
    next();
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    console.log(`Received login attempt with username: ${username} and password: ${password}`);

    const REDIRECT_URI = 'http://localhost:3000/callback';
    const AUTH_URL = `https://${DOMAIN}/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&scope=openid profile email offline_access`;
    res.redirect(AUTH_URL);
});

// Маршрут для обробки callback після авторизації
app.get('/callback', async (req, res) => {
    const authorizationCode = req.query.code;
    if (!authorizationCode) {
        return res.status(400).send('Authorization code not found');
    }
    try {
        const tokenResponse = await axios.post(`https://${DOMAIN}/oauth/token`, {
            grant_type: 'authorization_code',
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: authorizationCode,
            redirect_uri: 'http://localhost:3000/callback'
        });

        const accessToken = tokenResponse.data.access_token;
        const refreshToken = tokenResponse.data.refresh_token;
        req.session.access_token = accessToken;
        req.session.refresh_token = refreshToken;
        console.log('Current session data:', req.session);
        res.redirect('/');
    } catch (error) {
        console.error('Error retrieving access token:', error.response?.data || error.message);
        res.status(500).send('Error retrieving access token');
    }
});

app.get('/', (req, res) => {
    if (req.session.access_token) {
        console.log('Returning access token and user info to client');
        res.json({
            access_token: req.session.access_token,
            user_info: req.session.user_info,
            logout: 'http://localhost:3000/logout'
        });
    } else {
        res.redirect('/login');
    }
});

app.get('/logout', (req, res) => {
    delete sessions[req.sessionId];
    res.redirect('/');
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});

