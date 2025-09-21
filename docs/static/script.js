document.addEventListener("DOMContentLoaded", () => {
    // Elements for user form
    const userForm = document.getElementById("user-form");
    const userFormContainer = document.getElementById("user-form-container");
    const chatContainer = document.getElementById("chat-container");

    // Elements for chatbot
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Helper: format time like "10:45 PM"
    function formatTime(date) {
        return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }

    // ----- USER FORM LOGIC -----
    if (userForm) {
        userForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(userForm);
            const userData = Object.fromEntries(formData.entries());

            try {
                const apiPrefix = window.API_PREFIX || "";
                const apiUrl = `${window.location.origin}${apiPrefix}/submit_user`;

                let response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData),
                });

                if (response.ok) {
                    userFormContainer.style.display = "none";
                    chatContainer.style.display = "flex"; // flex so chatbox expands
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
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Show user message
        const userMsgElem = document.createElement("div");
        userMsgElem.classList.add("message", "user-message");
        userMsgElem.innerHTML = `<div>${message}</div><div class="timestamp">${formatTime(new Date())}</div>`;
        chatBox.appendChild(userMsgElem);

        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        userInput.value = "";

        try {
            const apiPrefix = window.API_PREFIX || "";
            const chatUrl = `${window.location.origin}${apiPrefix}/chat`;

            const response = await fetch(chatUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();

            // ---- Typing indicator ----
            const typingElem = document.createElement("div");
            typingElem.classList.add("message", "bot-message", "typing");
            typingElem.innerHTML = `
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            `;
            chatBox.appendChild(typingElem);
            chatBox.scrollTop = chatBox.scrollHeight;


            // Wait ~1 second before showing real reply
            setTimeout(() => {
                chatBox.removeChild(typingElem);

                const botMsgElem = document.createElement("div");
                botMsgElem.classList.add("message", "bot-message");
                botMsgElem.innerHTML = `<div>${data.reply || "No reply"}</div><div class="timestamp">${formatTime(new Date())}</div>`;
                chatBox.appendChild(botMsgElem);

                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000); // delay in ms
        } catch (err) {
            console.error("Chat error:", err);
            const botMsgElem = document.createElement("div");
            botMsgElem.classList.add("message", "bot-message");
            botMsgElem.innerHTML = `<div>Bot: [Error connecting to server]</div><div class="timestamp">${formatTime(new Date())}</div>`;
            chatBox.appendChild(botMsgElem);
        }
    }

    if (sendBtn) {
        // Click send
        sendBtn.addEventListener("click", sendMessage);

        // Press Enter to send
        userInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});
