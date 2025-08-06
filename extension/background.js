// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'CHAT_MESSAGE') {
        //This is an async function to handle the API call
        const getAiResponse = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(request.payload),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                sendResponse(data);

            } catch (error) {
                console.error('Error calling backend API:', error);
                sendResponse({ error: error.message });
            }
        };

        getAiResponse();

        // Return true to indicate that we will send a response asynchronously.
        // This is important to keep the message channel open.
        return true; 
    }
}); 