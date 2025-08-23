This extension is for chatting with Youtube video in real time. 

The flow is as follows:
1) The user loads the extension on Youtube and the extension loads.
2) The user presses get started, and the youtube video id is captured and sent to the backend
3) The Youtube API is hit to get the video transcript along with timestamps
4) Chunking is performed on the transcript.
5) Chunked data is stored in Vector DB (Currently using fais) for retrival
6) When the user asks the question, the question is sent to the backend through background.js, retreival is perfomed from the vector db to get the appropriate answer and then shown to the user. 