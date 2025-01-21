const apiUrl = "http://127.0.0.1:8000";

    // Fetch and display the unique code for sharing
    async function fetchCode() {
      const response = await fetch(`${apiUrl}/generate_code`);
      const data = await response.json();
      document.getElementById("clipboard-code").textContent = data.code || "Error generating code";
    }

    fetchCode();

    // Handle sending the clipboard content
    document.getElementById("send-button").addEventListener("click", async () => {
      const content = document.getElementById("clipboard-content").value.trim();
      if (content) {
        const response = await fetch(`${apiUrl}/add`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content }),
        });
        const data = await response.json();
        alert("Item added successfully with ID: " + data.id);
      } else {
        alert("Please enter some content to send.");
      }
    });

    document.getElementById("refresh-button").addEventListener("click", async () => {
      const response = await fetch(`${apiUrl}/get_all`);
      const items = await response.json();
      alert("Clipboard Items:\n" + JSON.stringify(items, null, 2));
    });

    document.getElementById("delete-button").addEventListener("click", async () => {
      const confirmDelete = confirm("Are you sure you want to delete all items?");
      if (confirmDelete) {
        const response = await fetch(`${apiUrl}/delete_all`, { method: "DELETE" });
        const data = await response.json();
        alert(data.message);
      }
    });

    document.getElementById("qr-button").addEventListener("click", () => {
      alert("QR functionality coming soon!");
    });