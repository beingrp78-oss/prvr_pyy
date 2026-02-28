const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; // 🎯 Your 16-digit ID
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) return;

    // 🛡️ Optimized Web Headers for 2026
    const headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': COOKIE,
        'origin': 'https://www.instagram.com',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest'
    };

    console.log(`🚀 Agent ${agentId}: DM Engine Initialized.`);

    while (true) {
        try {
            const now = Date.now().toString();
            // 📦 Form-Data Payload (Required for send_item)
            const params = new URLSearchParams();
            params.append('text', MESSAGE_BODY + " " + Math.random().toString(36).substring(7));
            params.append('client_context', now);
            params.append('offline_threading_id', now);

            // 📍 DIRECT SEND PATH (Fixes 404/500)
            const response = await axios.post(
                `https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`, 
                params.toString(), 
                { headers, timeout: 15000 }
            );

            process.stdout.write(`✅ [Agent ${agentId}] Message Sent | Status: ${response.status}\r`);
            
        } catch (e) {
            const status = e.response ? e.response.status : 'ERR';
            console.log(`\n⚠️ [Agent ${agentId}] Status: ${status}`);

            if (status === 404) {
                console.log("📍 ID Mismatch: This ID might be a USER_ID, not a THREAD_ID.");
            } else if (status === 429) {
                console.log("💤 Rate Limited. Waiting 60s...");
                await new Promise(r => setTimeout(r, 60000));
            }
            await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 2000));
    }
}

sendStrike(1);
