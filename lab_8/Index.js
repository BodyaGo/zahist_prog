const axios = require('axios');
const uuid = require('uuid');
const express = require('express');
const onFinished = require('on-finished');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const jwt = require('jsonwebtoken');  
const jwksClient = require('jwks-rsa');
const port = 3000;

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const DOMAIN = 'dev-4piqjyt8i3e2h2ww.eu.auth0.com'; 
const CLIENT_ID = 'F1e6bh022aCtnRgnSF2dtK7HGU4cw7Xz'; 
const CLIENT_SECRET = 'X8Q2ghz0W6rT7mUPrMSV-MdrwSmpN-Vu9iRGGyGjaVwUn_IS-ilFnvrRdqv5VLnU';
const AUDIENCE = `https://${DOMAIN}/api/v2/`;
const SESSION_KEY = 'Authorization';

class Session {
    #sessions = {}

    constructor() {
        try {
            this.#sessions = fs.readFileSync('./sessions.json', 'utf8');
            this.#sessions = JSON.parse(this.#sessions.trim());
            console.log('Existing sessions:', this.#sessions);
        } catch (e) {
            this.#sessions = {};
        }
    }

    #storeSessions() {
        fs.writeFileSync('./sessions.json', JSON.stringify(this.#sessions), 'utf-8');
    }

    set(key, value) {
        this.#sessions[key] = value || {};
        this.#storeSessions();
        console.log('Updated session:', this.#sessions);
    }

    get(key) {
        return this.#sessions[key];
    }

    init() {
        const sessionId = uuid.v4();
        this.set(sessionId, {});
        console.log(`Initialized new session with ID: ${sessionId}`);
        return sessionId;
    }

    destroy(sessionId) {
        delete this.#sessions[sessionId];
        this.#storeSessions();
        console.log(`Destroyed session with ID: ${sessionId}`);
    }
}

const sessions = new Session();
const client = jwksClient({
    jwksUri: `https://${DOMAIN}/.well-known/jwks.json`
});
async function getKey(header) {
    const key = await client.getSigningKeyAsync(header.kid);
    return key.getPublicKey();
}
const verifyTokenSignature = (token) => {
    return new Promise((resolve, reject) => {
        jwt.verify(token, getKey, {
            audience: AUDIENCE,
            issuer: `https://${DOMAIN}/`,
            algorithms: ['RS256']
        }, (err, decoded) => {
            if (err) {
                return reject(err);
            }
            resolve(decoded);
        });
    });
};
const checkToken = async (req, res, next) => {
    if (req.session.access_token) {
        try {
            console.log('Validating JWT signature...');
            const decoded = await verifyTokenSignature(req.session.access_token);
            console.log('JWT signature validated successfully:', decoded);

            if (req.session.expires_in && Date.now() > req.session.expires_in - 60000) {
                console.log('Token is about to expire, refreshing...');
                const newTokenData = await refreshToken(req.session.refresh_token);
                if (newTokenData && newTokenData.access_token) {
                    req.session.access_token = newTokenData.access_token;
                    req.session.expires_in = Date.now() + newTokenData.expires_in * 1000;
                    console.log('Token refreshed and session updated:', req.session);
                }
            }

            next();
        } catch (error) {
            console.error('Invalid JWT signature:', error);
            return res.status(401).send('Invalid token signature');
        }
    } else {
        console.log('No access token found in session');
        res.status(401).send('Unauthorized');
    }
};

app.use((req, res, next) => {
    let sessionId = req.get(SESSION_KEY);
    
    if (sessionId) {
        const currentSession = sessions.get(sessionId);
        if (currentSession) {
            console.log(`Existing session found for ID: ${sessionId}`);
            req.session = currentSession;
        } else {
            console.log(`No session found for this session ID (${sessionId}). Initializing a new session.`);
            sessionId = sessions.init();
            req.session = {};
        }
    } else {
        console.log('No valid session ID found. Initializing a new session.');
        sessionId = sessions.init();
        req.session = {};
    }

    req.sessionId = sessionId;

    onFinished(res, () => {
        sessions.set(req.sessionId, req.session);
    });

    next();
});

const getToken = async (username, password) => {
    const options = {
        method: 'POST',
        url: `https://${DOMAIN}/oauth/token`,
        headers: { 'content-type': 'application/json' },
        data: {
            grant_type: 'password',
            username: username,
            password: password,
            audience: AUDIENCE,
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            scope: 'openid profile email offline_access'
        }
    };

    try {
        const response = await axios.request(options);
        return response.data; 
    } catch (error) {
        console.error('Error fetching token:', error.response ? error.response.data : error.message);
        throw new Error('Authentication failed');
    }
};

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const tokenData = await getToken(username, password);
        req.session.access_token = tokenData.access_token;
        req.session.refresh_token = tokenData.refresh_token;
        req.session.expires_in = Date.now() + tokenData.expires_in * 1000;

        console.log('User logged in successfully. Session:', req.session);
        res.status(200).send({ success: true, access_token: tokenData.access_token });
    } catch (error) {
        console.error('Login failed:', error);
        res.status(401).send({ success: false, message: error.message });
    }
});

app.get('/protected', checkToken, (req, res) => {
    res.status(200).send({ message: 'Welcome to the protected route!' });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
