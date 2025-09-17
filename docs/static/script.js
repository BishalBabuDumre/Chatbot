// Handle user info form submission
document.getElementById("user-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    let response = await fetch("/save_user", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    if (result.status === "success") {
        // Hide form and show chat container
        document.getElementById("user-form-container").style.display = "none";
        document.getElementById("chat-container").style.display = "block";
    } else {
        alert("Error: " + result.detail);
    }
});

// Handle chatbot messages
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (!message) return;

    appendMessage("You", message, "user-message");
    inputField.value = "";

    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    });

    let result = await response.json();
    appendMessage("Bot", result.reply, "bot-message");
}

function appendMessage(sender, text, className) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = "message " + className;
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
