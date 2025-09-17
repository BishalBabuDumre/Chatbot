document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ script.js loaded!");
    
    // Handle user info form
    const userForm = document.getElementById("user-form");
    if (userForm) {
        userForm.addEventListener("submit", async function (e) {
            e.preventDefault(); // This should prevent page reload
            console.log("Form submitted"); // Debug log
            
            const formData = new FormData(this);

            try {
                let response = await fetch("/save_user", {
                    method: "POST",
                    body: formData
                });

                let result = await response.json();

                if (result.status === "success") {
                    console.log("✅ User info saved to DB");
                    document.getElementById("user-form-container").style.display = "none";
                    document.getElementById("chat-container").style.display = "block";
                } else {
                    alert("❌ Error saving user info: " + result.detail);
                }
            } catch (err) {
                alert("❌ Network error while saving user info: " + err);
            }
        });
    }
document.getElementById("user-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // stop page reload

    const formData = new FormData(this);

    try {
        let response = await fetch("/save_user", {
            method: "POST",
            body: formData
        });

        let result = await response.json();

        if (result.status === "success") {
            console.log("✅ User info saved to DB");

            // Hide the form
            document.getElementById("user-form-container").style.display = "none";

            // Show the chatbot
            document.getElementById("chat-container").style.display = "block";
        } else {
            alert("❌ Error saving user info: " + result.detail);
        }
    } catch (err) {
        alert("❌ Network error while saving user info: " + err);
    }
});

// ---------------------------
// Chatbot interaction
// ---------------------------
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
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

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        let result = await response.json();

        // Backend returns {"reply": "..."}
        if (result.reply) {
            appendMessage("Bot", result.reply, "bot-message");
        } else {
            appendMessage("Bot", "⚠️ Error: no reply received.", "bot-message");
        }
    } catch (err) {
        appendMessage("Bot", "⚠️ Error talking to server: " + err, "bot-message");
    }
}

// ---------------------------
// Utility: append messages
// ---------------------------
function appendMessage(sender, text, className) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = "message " + className;
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
});
