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
    if (!csrftoken) return;

    // 🛡️ Optimized Web-Stable Headers
    const headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': COOKIE,
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    };

    while (true) {
        try {
            const now = Date.now();
            const params = new URLSearchParams();
            params.append('text', MESSAGE_BODY + " " + (Math.random() * 100).toFixed(0));
            params.append('client_context', now.toString());

            // 📍 Path: Standard Web Messaging
            await axios.post(
                `https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`,
                params.toString(),
                { headers }
            );

            process.stdout.write(`✅ [Agent ${agentId}] Strike Success\r`);
        } catch (e) {
            const status = e.response ? e.response.status : 'OFFLINE';
            console.log(`\n⚠️ Agent ${agentId} Error: ${status}`);
            
            if (status === 404) {
                console.log("❌ 404: The URL is invalid. Ensure THREAD_ID is ONLY numbers.");
                process.exit(1);
            }
            await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 100));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
