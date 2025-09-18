document.getElementById("userForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        address: document.getElementById("address").value,
        state: document.getElementById("state").value,
        zip: document.getElementById("zip").value
    };

    const response = await fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById("responseMessage").innerText = result.message;
});
