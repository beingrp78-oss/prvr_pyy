const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = process.env.TARGET_THREAD_ID;
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) {
        console.log(`❌ Agent ${agentId}: CSRF Missing from Cookie.`);
        return;
    }

    // 🛡️ AUTHENTIC HEADERS: These bypass the 403 check
    const headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': COOKIE,
        'origin': 'https://www.instagram.com',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459', // 🔑 THE MAGIC KEY
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest'
    };

    console.log(`🚀 Agent ${agentId} Active. Targeting: ${THREAD_ID}`);

    while (true) {
        try {
            const ts = Date.now();
            const params = new URLSearchParams();
            params.append('text', MESSAGE_BODY + " " + Math.random().toString(36).substring(7));
            params.append('client_context', ts.toString());

            await axios.post(
                `https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`,
                params.toString(),
                { headers }
            );

            process.stdout.write(`✅ [Agent ${agentId}] Strike Success\r`);
        } catch (e) {
            const status = e.response ? e.response.status : 'ERR';
            console.log(`\n⚠️ Agent ${agentId} Status: ${status}`);
            
            if (status === 403) {
                console.log("🚫 [403] Your account has a security block. Refresh your cookie on your phone/browser.");
                process.exit(1); 
            }
            await new Promise(r => setTimeout(r, 6000));
        }
        await new Promise(r => setTimeout(r, 100 + Math.random() * 50));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
