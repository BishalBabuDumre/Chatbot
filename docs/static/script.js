document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("userForm");
  const responseMessage = document.getElementById("responseMessage");
  const chatContainer = document.getElementById("chatContainer");
  const chatBox = document.getElementById("chatBox");
  const chatInput = document.getElementById("chatInput");
  const chatSend = document.getElementById("chatSend");

  // Handle form submission
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    try {
      const response = await fetch("/submit", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      responseMessage.textContent = result.message;
      responseMessage.style.color = result.status === "success" ? "green" : "red";

      if (result.status === "success") {
        form.style.display = "none"; // Hide form
        chatContainer.style.display = "block"; // Show chatbot
      }
    } catch (err) {
      responseMessage.textContent = "Error submitting form.";
      responseMessage.style.color = "red";
    }
  });

  // Handle chatbot messages
  chatSend.addEventListener("click", async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    // Show user message
    const userMsg = document.createElement("div");
    userMsg.className = "userMsg";
    userMsg.textContent = "You: " + message;
    chatBox.appendChild(userMsg);

    // Send to backend
    const chatData = new FormData();
    chatData.append("message", message);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        body: chatData
      });

      const result = await response.json();
      const botMsg = document.createElement("div");
      botMsg.className = "botMsg";
      botMsg.textContent = result.reply;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
      const botMsg = document.createElement("div");
      botMsg.className = "botMsg";
      botMsg.style.color = "red";
      botMsg.textContent = "Error: Could not reach chatbot.";
      chatBox.appendChild(botMsg);
    }

    chatInput.value = "";
  });
});
