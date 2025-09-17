// -------------------------------
// Handle user info form submission
// -------------------------------
document.getElementById("user-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
        full_name: e.target.full_name.value,
        address: e.target.address.value,
        state: e.target.state.value,
        zip_code: e.target.zip_code.value
    };

    try {
        let response = await fetch("/save_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            // Hide form and show chat
            document.getElementById("user-form-container").style.display = "none";
            document.getElementById("chat-container").style.display = "block";
        } else {
            let error = await response.json();
            alert("Error saving user: " + (error.error || "Unknown error"));
        }
    } catch (err) {
        alert("Failed to connect to server: " + err.message);
    }
});

// -------------------------------
// Handle chat messages
// -------------------------------
document.getElementById("send-btn").addEventListener("click", async () => {
    sendMessage();
});

document.getElementById("user-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const inputBox = document.getElementById("user-input");
    const message = inputBox.value.trim();
    if (!message) return;

    // Display user message in chatbox
    addMessage(message, "user-message");
    inputBox.value = "";

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        if (response.ok) {
            let data = await response.json();
            addMessage(data.response, "bot-message");
        } else {
            addMessage("Error: Unable to get response from server.", "bot-message");
        }
    } catch (err) {
        addMessage("Error: " + err.message, "bot-message");
    }
}

// -------------------------------
// Utility to add messages to chat
// -------------------------------
function addMessage(text, className) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", className);
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
