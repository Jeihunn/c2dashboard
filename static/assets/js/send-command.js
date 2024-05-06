function handleFormSubmit(event) {
  event.preventDefault();

  // Get form data
  const agentId = document.getElementById("agent").value;
  const commandType = document.getElementById("commandType").value;
  const command = document.getElementById("command").value;
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];

  // Get error message elements
  const errorAgent = document.getElementById("errorAgent");
  const errorCommand = document.getElementById("errorCommand");
  const errorFile = document.getElementById("errorFile");

  // Reset previous error messages
  errorAgent.textContent = "";
  errorCommand.textContent = "";
  errorFile.textContent = "";

  // Check if agent is selected
  if (!agentId) {
    errorAgent.textContent = "Please select an agent.";
    return;
  }

  // Check if both command and file are empty
  if (!command && !file) {
    errorCommand.textContent =
      "Command cannot be empty if file is not uploaded.";
    errorFile.textContent = "Please upload a file or enter a command.";
    return;
  }

  // Check if file is uploaded but command is not empty
  if (file && command) {
    errorCommand.textContent =
      "Command cannot be entered if a file is uploaded.";
    return;
  }

  // Prepare form data
  const formData = new FormData();
  formData.append("agent", agentId);
  formData.append("command", `${commandType.toUpperCase()}:${command}`);
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
