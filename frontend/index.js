// take necessary elements
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const mainContent = document.getElementById("mainContent");
const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const newChatButton = document.querySelector(".new-chat-button");
const chatItems = document.getElementById("chatItems");
const currentChatTitle = document.getElementById("currentChatTitle");

// variables
let botIsAnswering = false;
let currentChatId = null;

// toggle button to collapse sidebar
sidebarToggle.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
});

// load chats and start new chat if page was reloaded or "New chat" button is pressed
window.addEventListener("load", function () {
    loadChatList();
    startNewChat();
});
newChatButton.addEventListener("click", startNewChat);

// call send message function if button or "Enter" is pressed
sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("input", resizeMessageInput);
messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});


// resize textarea depending on message length
function resizeMessageInput() {
    messageInput.style.height = "26px";

    const maxHeight = 160;
    const newHeight = Math.min(messageInput.scrollHeight, maxHeight);

    messageInput.style.height = newHeight + "px";

    if (messageInput.scrollHeight > maxHeight) {
        messageInput.style.overflowY = "auto";
    } else {
        messageInput.style.overflowY = "hidden";
    }
}


// start new chat
async function startNewChat() {
    if (botIsAnswering) {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/new_chat", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("New chat could not be created");
        }

        const chat = await response.json();

        clearFrontendChat();

        currentChatId = chat.id;
        currentChatTitle.textContent = "New chat";
    } catch (error) {
        console.log("New chat could not be created");
    }
}


// load chat list
async function loadChatList() {
    try {
        const response = await fetch("http://127.0.0.1:5000/chats_titles");
        const data = await response.json();

        chatItems.innerHTML = "";

        for (const chat of data.chats) {
            const chatRow = document.createElement("div");
            const chatButton = document.createElement("button");
            const deleteButton = document.createElement("button");

            chatRow.classList.add("chat-item-row");

            chatButton.classList.add("chat-item");
            chatButton.textContent = chat.title;

            chatButton.addEventListener("click", function () {
                loadSavedChat(chat.id);
            });

            deleteButton.classList.add("delete-chat-button");
            deleteButton.setAttribute("aria-label", "Delete chat");
            deleteButton.innerHTML = `
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M3 6h18"></path>
                    <path d="M8 6V4h8v2"></path>
                    <path d="M19 6l-1 14H6L5 6"></path>
                    <path d="M10 11v5"></path>
                    <path d="M14 11v5"></path>
                </svg>
            `;

            deleteButton.addEventListener("click", function (event) {
                event.stopPropagation();
                deleteSavedChat(chat.id);
            });

            chatRow.appendChild(chatButton);
            chatRow.appendChild(deleteButton);
            chatItems.appendChild(chatRow);
        }
    } catch (error) {
        console.log("Chat list could not be loaded");
    }
}


// load saved chat
async function loadSavedChat(chatId) {
    if (botIsAnswering) {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/chat/" + chatId);
        const chat = await response.json();

        clearFrontendChat();

        currentChatId = chat.id;
        currentChatTitle.textContent = chat.title;

        for (let index = 2; index < chat.messages.length; index++) {
            const message = chat.messages[index];

            if (message.role === "user") {
                addMessage(message.content, "user-message");
            }

            if (message.role === "assistant") {
                addMessage(message.content, "bot-message");
            }
        }

        if (chat.messages.length > 2) {
            mainContent.classList.add("chat-active");
            messageInput.placeholder = "Ask OTH Guide AI";
        }

        scrollChatToBottom();
    } catch (error) {
        console.log("Saved chat could not be loaded");
    }
}


// clear last chat
function clearFrontendChat() {
    messages.innerHTML = "";
    messageInput.value = "";
    messageInput.placeholder = "How can I help you with OTH Regensburg today?";
    mainContent.classList.remove("chat-active");

    currentChatTitle.textContent = "New chat";
    resizeMessageInput();

    botIsAnswering = false;
    sendButton.disabled = false;
}


// delete saved chat
async function deleteSavedChat(chatId) {
    if (botIsAnswering) {
        return;
    }

    const currentChatWasDeleted = currentChatId === chatId;

    try {
        const response = await fetch("http://127.0.0.1:5000/chat/" + chatId, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Chat could not be deleted");
        }

        if (currentChatWasDeleted) {
            await startNewChat();
        }

        await loadChatList();
    } catch (error) {
        console.log("Chat could not be deleted");
    }
}


// show user message and AI answer
async function sendMessage() {
    // avoid several messages
    if (botIsAnswering) {
        return;
    }

    // avoid empty messages
    const userText = messageInput.value.trim();
    if (userText === "") {
        return;
    }

    if (currentChatId === null) {
        await startNewChat();
    }

    // disable button during AI thinking and answering
    botIsAnswering = true;
    sendButton.disabled = true;

    // change and move input box
    mainContent.classList.add("chat-active");
    messageInput.placeholder = "Ask OTH Guide AI";

    // add user message
    addMessage(userText, "user-message");
    messageInput.value = "";
    resizeMessageInput();

    // show "Thinking..." during AI thinking
    const thinkingMessage = addMessage("Thinking...", "thinking-message");

    // scroll to a new message
    scrollChatToBottom();

    try {
        // frontend <--> backend connection
        const response = await fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userText
            })
        });

        const data = await response.json();

        thinkingMessage.remove();

        // add bot message
        addMessage(data.answer, "bot-message");

        if (currentChatTitle.textContent === "New chat") {
            currentChatTitle.textContent = "Chat #" + currentChatId;
        }

        loadChatList();
    } catch (error) {
        thinkingMessage.remove();

        // add bot message
        addMessage("Connection error. Please check if the Python backend is running.", "bot-message");
    }

    // allow next message sending
    botIsAnswering = false;
    sendButton.disabled = false;

    // scroll to a new message
    scrollChatToBottom();
}


// show new message
function addMessage(text, className) {
    const message = document.createElement("div");

    message.classList.add("message");
    message.classList.add(className);
    message.textContent = text;

    messages.appendChild(message);

    return message;
}


// scroll chat to bottom
function scrollChatToBottom() {
    const chatSection = document.getElementById("chatSection");
    chatSection.scrollTop = chatSection.scrollHeight;
}