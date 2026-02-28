const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; 
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) return;

    // 🔥 Using the 'i.instagram' mobile-priority gateway to stop 404s
    const config = {
        headers: {
            'cookie': COOKIE,
            'x-csrftoken': csrftoken,
            'x-ig-app-id': '936619743392459',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Instagram 150.0.0.0.0 (iPhone; iOS 14_4_1; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
            'x-requested-with': 'XMLHttpRequest'
        }
    };

    console.log(`🚀 Agent ${agentId}: Titan Engine Armed.`);

    while (true) {
        try {
            const now = Date.now();
            const data = new URLSearchParams({
                'text': MESSAGE_BODY + " " + Math.random().toString(36).substring(7),
                'client_context': now.toString(),
                'thread_ids': `[${THREAD_ID}]`, // Required format for this endpoint
                'offline_threading_id': now.toString()
            });

            // 📍 TRYING THE MOBILE V2 ENDPOINT (Solves 404 for 16-digit IDs)
            await axios.post(
                'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/', 
                data.toString(), 
                { ...config, timeout: 10000 }
            );

            console.log(`✅ [Agent ${agentId}] Strike Delivered`);
            
        } catch (e) {
            const status = e.response ? e.response.status : 'ERR';
            console.log(`⚠️ [Agent ${agentId}] Status: ${status}`);

            if (status === 404) {
                console.log("📍 Path Error: Trying Fallback URL...");
                // AUTOMATIC FALLBACK TO WEB ENDPOINT
                try {
                    const webData = new URLSearchParams({
                        'text': MESSAGE_BODY,
                        'client_context': Date.now().toString()
                    });
                    await axios.post(`https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`, webData.toString(), config);
                    console.log(`✅ [Agent ${agentId}] Fallback Success`);
                } catch (fallbackErr) {
                    console.log("❌ Both paths failed. Checking ID integrity...");
                }
            }
            await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 1500));
    }
}

sendStrike(1);
