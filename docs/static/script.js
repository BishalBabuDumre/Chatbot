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
                let response = await fetch("/submit_user", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData),
                });

                if (response.ok) {
                    // Hide form and show chatbot
                    userFormContainer.style.display = "none";
                    chatContainer.style.display = "block";
                } else {
                    alert("Failed to save user info.");
                }
            } catch (err) {
                console.error(err);
                alert("Error submitting form");
            }
        });
    }
});
