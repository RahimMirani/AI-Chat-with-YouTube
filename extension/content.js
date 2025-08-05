(async () => {
    // This is the main entry point for our content script.
    // It runs as soon as the YouTube page's DOM is ready.
    console.log("YouTube RAG Chat content script loaded.");

    // Create a container for our chat UI
    const app = document.createElement('div');
    app.id = 'youtube-rag-chat-app';
    document.body.appendChild(app);

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

})(); 