document.addEventListener("DOMContentLoaded", () => {
    // Elements for user form
    const userForm = document.getElementById("user-form");
    const userFormContainer = document.getElementById("user-form-container");
    const chatContainer = document.getElementById("chat-container");

    // Elements for chatbot
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // ----- USER FORM LOGIC -----
    if (userForm) {
        userForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(userForm);
            const userData = Object.fromEntries(formData.entries());

            try {
                // Allow optional API prefix (e.g. /api in Render)
                const apiPrefix = window.API_PREFIX || "";
                const apiUrl = `${window.location.origin}${apiPrefix}/submit_user`;

                let response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData),
                });

                if (response.ok) {
                    // Hide form and show chatbot
                    userFormContainer.style.display = "none";
                    chatContainer.style.display = "block";
                } else {
                    const error = await response.json();
                    alert("Failed to save user info: " + (error.error || response.status));
                }
            } catch (err) {
                console.error(err);
                alert("Error submitting form");
            }
        });
    }

    // ----- CHATBOT LOGIC -----
    if (sendBtn) {
        sendBtn.addEventListener("click", async () => {
            const message = userInput.value.trim();
            if (!message) return;

            // Show user message
            const userMsgElem = document.createElement("div");
            userMsgElem.textContent = "You: " + message;
            chatBox.appendChild(userMsgElem);

            // Call backend
            try {
                const apiPrefix = window.API_PREFIX || "";
                const chatUrl = `${window.location.origin}${apiPrefix}/chat`;

                const response = await fetch(chatUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();

                // Show reply
                const botMsgElem = document.createElement("div");
                botMsgElem.textContent = "Bot: " + (data.reply || "No reply");
                chatBox.appendChild(botMsgElem);

                // Scroll to bottom
                chatBox.scrollTop = chatBox.scrollHeight;

                userInput.value = "";
            } catch (err) {
                console.error("Chat error:", err);
                const botMsgElem = document.createElement("div");
                botMsgElem.textContent = "Bot: [Error connecting to server]";
                chatBox.appendChild(botMsgElem);
            }
        });
    }
});
