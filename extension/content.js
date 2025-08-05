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

        // Get references to the UI elements
        const sendButton = document.getElementById('chat-send-button');
        const inputField = document.getElementById('chat-input');
        const messagesContainer = document.getElementById('chat-messages');

        // Listen for clicks on the send button
        sendButton.addEventListener('click', () => {
            const question = inputField.value;
            if (!question) return; // Don't send empty messages

            // Get the video ID from the URL
            const urlParams = new URLSearchParams(window.location.search);
            const videoId = urlParams.get('v');

            // Get the current timestamp from the video player
            const player = document.querySelector('.html5-main-video');
            const timestamp = player ? player.currentTime : 0;
            
            console.log("Question:", question);
            console.log("Video ID:", videoId);
            console.log("Timestamp:", timestamp);

            // Clear the input field after sending
            inputField.value = '';
        });

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