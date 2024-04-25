const clientsInfo = document.querySelector(".clients-info");
const commandFormContainer = document.querySelector(".command-form-container");

// Function to handle when WebSocket connection is opened
function onSocketOpen(event) {
  console.log("WebSocket connection opened");
}

// Function to handle incoming messages over WebSocket
function onSocketMessage(event) {
  const data = JSON.parse(event.data);
  console.log("data", data);

  const agents = data.agents;

  if (agents.length === 0) {
    showNoAgentsMessage();
    clearCommandForm();
  } else {
    showConnectedAgents(agents);
    renderCommandForm();
  }
}

// Function to handle when WebSocket connection is closed
function onSocketClose(event) {
  console.log("WebSocket connection closed");
}

// Function to handle WebSocket errors
function onSocketError(error) {
  console.error("WebSocket error:", error);
}

// Function to display "No agents connected" message
function showNoAgentsMessage() {
  const alertMessage = document.createElement("div");
  alertMessage.classList.add("alert", "alert-info");
  alertMessage.textContent = "No agents connected";
  clientsInfo.innerHTML = "";
  clientsInfo.appendChild(alertMessage);
}

// Function to clear the command form
function clearCommandForm() {
  commandFormContainer.innerHTML = "";
}

// Function to display connected agents
function showConnectedAgents(agents) {
  clientsInfo.innerHTML = "";

  const heading = document.createElement("h2");
  heading.textContent = "Connected Agents:";
  clientsInfo.appendChild(heading);

  const ul = document.createElement("ul");
  ul.classList.add("list-group");

  agents.forEach((agent) => {
    const listItem = document.createElement("li");
    listItem.classList.add(
      "list-group-item",
      "d-flex",
      "justify-content-between",
      "align-items-center"
    );
    listItem.textContent = agent;
    const badge = document.createElement("span");
    badge.classList.add("badge", "bg-primary", "rounded-pill");
    badge.textContent = "Connected";
    listItem.appendChild(badge);
    ul.appendChild(listItem);
  });

  clientsInfo.appendChild(ul);
}

// Function to render the command form
function renderCommandForm() {
  const formHTML = `
    <div class="command-form">
      <div class="row mt-4">
        <div class="col">
          <form action="/send-command/" method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            <div class="mb-3">
              <label for="command" class="form-label">Enter command:</label>
              <input type="text" class="form-control" id="command" name="command" placeholder="Type your command here">
            </div>
            <button type="submit" class="btn btn-primary">Send Command</button>
          </form>
        </div>
      </div>
    </div>
  `;

  commandFormContainer.innerHTML = formHTML;
}

// WebSocket connection
const socket = new WebSocket("ws://localhost:8000/ws/clients/");

// Event listeners for WebSocket
socket.onopen = onSocketOpen;
socket.onmessage = onSocketMessage;
socket.onclose = onSocketClose;
socket.onerror = onSocketError;
