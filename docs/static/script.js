document.addEventListener("DOMContentLoaded", () => {
    const userForm = document.getElementById("user-form");
    const userFormContainer = document.getElementById("user-form-container");
    const chatContainer = document.getElementById("chat-container");

    if (userForm) {
        userForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(userForm);
            const userData = Object.fromEntries(formData.entries());

            try {
                // Allow optional API prefix (e.g. /api)
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
});
