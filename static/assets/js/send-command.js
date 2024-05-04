function handleFormSubmit(event) {
    event.preventDefault();
  
    // Get form data
    const agentId = document.getElementById("agent").value;
    const command = document.getElementById("command").value;
  
    // Sending a POST request with Fetch
    fetch("/send-command/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken,
      },
      body: new URLSearchParams({
        agent: agentId,
        command: command,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
      });
  }
  
  // Codes to be run after the page is fully loaded
  document.addEventListener("DOMContentLoaded", function() {
    let commandForm = document.querySelector("#commandForm");
    console.log("commandForm", commandForm);
  
    if (commandForm) {
        commandForm.addEventListener("submit", handleFormSubmit);
    }
  });
  