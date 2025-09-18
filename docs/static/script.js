// /static/script.js
window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById("userForm");
  if (!form) { console.error("Form #userForm not found"); return; }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const data = {
        name: document.getElementById("name").value,
        address: document.getElementById("address").value,
        state: document.getElementById("state").value,
        zip: document.getElementById("zip").value
      };

      console.log("Submitting to /submit with:", data); // <-- helps debugging

      const response = await fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      document.getElementById("responseMessage").innerText = result.message || "Done";
      console.log("Server response:", result);
    } catch (err) {
      console.error("Submit failed:", err);
      document.getElementById("responseMessage").innerText = "Submit failed (see console).";
    }
  });
});
