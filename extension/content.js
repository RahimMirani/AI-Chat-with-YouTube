// This script will be injected into the YouTube video page.
// It is responsible for creating the chat UI and interacting with the page.

(async () => {
    // Wait for the specific element that contains the YouTube "Up Next" playlist to appear.
    const secondaryContainer = await waitForElement('#secondary');

    if (secondaryContainer) {
        console.log("YouTube RAG Chat: Secondary container found. Injecting UI.");
        
        // Create a container for our chat UI
        const app = document.createElement('div');
        app.id = 'youtube-rag-chat-app';
        
        // Inject our app as the first child of the container
        secondaryContainer.prepend(app);

        // Fetch the HTML for the chat UI and inject it into our container
        const htmlURL = chrome.runtime.getURL('chat.html');
        const response = await fetch(htmlURL);
        const chatHtml = await response.text();
        app.innerHTML = chatHtml;

        // Inject the CSS so our UI is styled correctly
        const cssURL = chrome.runtime.getURL('style.css');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = cssURL;
        document.head.appendChild(link);

        // --- New UI logic starts here ---

        // Get references to the new UI elements
        const getStartedButton = document.getElementById('get-started-button');
        const processingIndicator = document.getElementById('processing-indicator');
        const welcomeView = document.getElementById('welcome-view');
        const mainChatView = document.getElementById('main-chat-view');

        // Get references to the chat UI elements
        const sendButton = document.getElementById('chat-send-button');
        const inputField = document.getElementById('chat-input');
        const messagesContainer = document.getElementById('chat-messages');

        // Listen for clicks on the "Get Started" button
        getStartedButton.addEventListener('click', () => {
            getStartedButton.disabled = true;
            processingIndicator.classList.remove('hidden');

            const urlParams = new URLSearchParams(window.location.search);
            const videoId = urlParams.get('v');

            // Validate video ID exists
            if (!videoId) {
                console.error('No video ID found in URL');
                processingIndicator.querySelector('p').textContent = 'Error: No video found. Please make sure you\'re on a YouTube video page.';
                // Reset error state to allow retry
                setTimeout(() => {
                    getStartedButton.disabled = false;
                    processingIndicator.classList.add('hidden');
                    processingIndicator.querySelector('p').textContent = 'Processing...';
                }, 3000);
                return;
            }

            chrome.runtime.sendMessage({
                type: 'PROCESS_VIDEO',
                payload: { video_id: videoId }
            }, (response) => {
                if (chrome.runtime.lastError || response.error) {
                    console.error(chrome.runtime.lastError?.message || response.error);
                    processingIndicator.querySelector('p').textContent = 'Error processing video. Please try again.';
                    // Reset error state to allow retry
                    setTimeout(() => {
                        getStartedButton.disabled = false;
                        processingIndicator.classList.add('hidden');
                        processingIndicator.querySelector('p').textContent = 'Processing...';
                    }, 3000);
                    return;
                }
                
                // On success, switch to the main chat view
                welcomeView.classList.add('hidden');
                mainChatView.classList.remove('hidden');
                // Focus the input field for immediate typing
                inputField.focus();
            });
        });

        // Listen for clicks on the send button
        sendButton.addEventListener('click', () => handleSend());

        // Also listen for 'Enter' key in the input field
        inputField.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                handleSend();
            }
        });

        function handleSend() {
            const question = inputField.value;
            if (!question) return;

            addMessage(question, 'user-message');
            inputField.value = '';

            // Get the video ID from the URL
            const urlParams = new URLSearchParams(window.location.search);
            const videoId = urlParams.get('v');

            // Get the current timestamp from the video player
            const player = document.querySelector('.html5-main-video');
            const timestamp = player ? player.currentTime : 0;
            
            chrome.runtime.sendMessage({
                type: 'CHAT_MESSAGE',
                payload: {
                    video_id: videoId,
                    question,
                    timestamp
                }
            }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error(chrome.runtime.lastError.message);
                    addMessage('Error: Could not connect to the backend.', 'bot-message');
                    return;
                }

                if (response.error) {
                    console.error('Backend error:', response.error);
                    addMessage(response.error, 'bot-message');
                } else {
                    addMessage(response.answer, 'bot-message');
                }
            });
        }

        function addMessage(text, className) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            messageDiv.textContent = text;
            messagesContainer.appendChild(messageDiv);

            // Scroll to the bottom of the messages container
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

    } else {
        console.error("YouTube RAG Chat: Could not find the secondary container to inject UI.");
    }
})();

function waitForElement(selector) {
    return new Promise(resolve => {
        const element = document.querySelector(selector);
        if (element) {
            return resolve(element);
        }

        const observer = new MutationObserver(mutations => {
            const element = document.querySelector(selector);
            if (element) {
                resolve(element);
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}  