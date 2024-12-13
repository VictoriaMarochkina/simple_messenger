const ws = new WebSocket("ws://localhost:8888/ws");

const messagesDiv = document.getElementById("messages");
const clientsList = document.getElementById("clients");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");


ws.onmessage = function (event) {
    console.log("Received raw data from server:", event.data);

    try {
        const data = JSON.parse(event.data);
        console.log("Parsed data:", data);

        if (data.type === "clients") {
            updateClientsList(data.clients);
        } else if (data.type === "message") {
            console.log("Adding message to chat:", data.content);
            addMessage(data.content);
        } else {
            console.warn("Unknown message type:", data.type);
        }
    } catch (error) {
        console.error("Error parsing message:", event.data, error);
    }
};

ws.onopen = function () {
    console.log("WebSocket connected");
    addMessage("✅ Подключено к серверу чата.");
    messageInput.disabled = false;
    sendButton.disabled = false;
};

ws.onerror = function (error) {
    console.error("WebSocket error:", error);
    addMessage("❌ Ошибка соединения с сервером.");
};

ws.onclose = function () {
    console.warn("WebSocket connection closed");
    addMessage("🔌 Соединение с сервером потеряно.");
    messageInput.disabled = true;
    sendButton.disabled = true;
};

sendButton.onclick = function () {
    const message = messageInput.value.trim();
    if (message) {
        try {
            console.log("Sending message:", message);
            ws.send(message);
            messageInput.value = "";
        } catch (error) {
            console.error("Error sending message:", error);
        }
    }
};

function updateClientsList(clients) {
    clientsList.innerHTML = "";
    clients.forEach((client) => {
        const li = document.createElement("li");
        li.textContent = client;
        clientsList.appendChild(li);
    });
    console.log("Updated clients list:", clients);
}

function addMessage(message) {
    console.log("Adding message to chat:", message);
    if (!messagesDiv) {
        console.error("Message container not found!");
        return;
    }
    const div = document.createElement("div");
    div.textContent = message;
    div.className = "message";
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

messageInput.disabled = true;
sendButton.disabled = true;
