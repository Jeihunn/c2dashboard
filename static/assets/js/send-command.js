function handleFormSubmit(event) {
  event.preventDefault();

  // Get form data
  const agentId = document.getElementById("agent").value;
  const command = document.getElementById("command").value;
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];

  // Prepare form data
  const formData = new FormData();
  formData.append("agent", agentId);
  formData.append("command", command);
  formData.append("file", file);

  // Sending a POST request with Fetch
  fetch("/send-command/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Form reset after successful submission
      document.getElementById("commandForm").reset();
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}

// Codes to be run after the page is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  let commandForm = document.querySelector("#commandForm");

  if (commandForm) {
    commandForm.addEventListener("submit", handleFormSubmit);
  }
});
