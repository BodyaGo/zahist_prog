const uuid = require('uuid');
const express = require('express');
const onFinished = require('on-finished');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const SESSION_KEY = 'Authorization';
const TOKEN_EXPIRY_THRESHOLD = 10;

const AUTH0_DOMAIN = 'dev-4piqjyt8i3e2h2ww.eu.auth0.com'; 
const AUTH0_CLIENT_ID = 'F1e6bh022aCtnRgnSF2dtK7HGU4cw7Xz'; 
const AUTH0_CLIENT_SECRET = 'X8Q2ghz0W6rT7mUPrMSV-MdrwSmpN-Vu9iRGGyGjaVwUn_IS-ilFnvrRdqv5VLnU'; 
const AUTH0_AUDIENCE = `https://dev-4piqjyt8i3e2h2ww.eu.auth0.com/api/v2/`;

class Session {
    #sessions = {};

    constructor() {
        try {
            this.#sessions = JSON.parse(fs.readFileSync('./sessions.json', 'utf8').trim());
            console.log('Sessions loaded successfully.');
        } catch (e) {
            this.#sessions = {};
        }
    }

    getAllSessionIds() { return Object.keys(this.#sessions); }

    #storeSessions() { fs.writeFileSync('./sessions.json', JSON.stringify(this.#sessions, null, 2), 'utf-8'); }

    set(key, value = {}) { this.#sessions[key] = value; this.#storeSessions(); }
    get(key) { return this.#sessions[key]; }

    async refreshToken(sessionId) {
        const session = this.get(sessionId);
        if (!session || !session.refresh_token) throw new Error('Refresh token is missing.');

        const data = { grant_type: 'refresh_token', client_id: AUTH0_CLIENT_ID, client_secret: AUTH0_CLIENT_SECRET, refresh_token: session.refresh_token };
        const response = await axios.post(`https://dev-4piqjyt8i3e2h2ww.eu.auth0.com/oauth/token`, data);
        const { access_token, expires_in } = response.data;

        session.access_token = access_token;
        session.expires_at = Math.floor(Date.now() / 1000) + expires_in;
        this.set(sessionId, session);
        console.log(`Token refreshed for session ${sessionId}`);
    }

    isTokenExpired(session) { return session.expires_at && session.expires_at - Math.floor(Date.now() / 1000) < TOKEN_EXPIRY_THRESHOLD; }
}

const sessions = new Session();

app.get('/', (req, res) => {
    if (req.session.username) return res.json({ username: req.session.username, token: req.session.access_token });
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.post('/api/login', async (req, res) => {
    const { login, password } = req.body;
    const data = { grant_type: 'password', username: login, password, client_id: AUTH0_CLIENT_ID, client_secret: AUTH0_CLIENT_SECRET, audience: AUTH0_AUDIENCE };
    const tokenData = await axios.post(`https://dev-4piqjyt8i3e2h2ww.eu.auth0.com/oauth/token`, data);

    req.session = { username: login, access_token: tokenData.data.access_token, refresh_token: tokenData.data.refresh_token, expires_at: Math.floor(Date.now() / 1000) + tokenData.data.expires_in };
    sessions.set(req.get(SESSION_KEY), req.session);
    res.json({ token: req.session.access_token });
});

app.listen(3000, () => console.log(`Server running on http://localhost:3000`));

