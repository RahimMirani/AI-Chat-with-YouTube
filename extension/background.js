// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // We only want to handle messages of type 'CHAT_MESSAGE'
    if (request.type === 'CHAT_MESSAGE') {
        console.log('Background script received message:', request.payload);
        
        // This is an async function to handle the API call
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
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Response from backend:', data);
                
                // For now, we are just logging the response.
                // In the next step, we would send this back to the content script.

            } catch (error) {
                console.error('Error calling backend API:', error);
            }
        };

        getAiResponse();

        // Return true to indicate that we will send a response asynchronously.
        // This is important to keep the message channel open.
        return true; 
    }
}); 