const clientsInfo = document.querySelector(".clients-info");
const commandFormContainer = document.querySelector(".command-form-container");

// Function to handle when WebSocket connection is opened
function onSocketOpen(event) {
  console.log("Clients WebSocket connection opened");
}

// Function to handle incoming messages over WebSocket
function onSocketMessage(event) {
  const data = JSON.parse(event.data);
  console.log("data", data);

  const agents = data.agents;
  const agentCount = Object.keys(agents).length;

  if (agentCount === 0) {
    showNoAgentsMessage();
    clearCommandForm();
  } else {
    showConnectedAgents(agents);
    renderCommandForm(agents);
    commandForm = document.querySelector("#commandForm");
    commandForm.addEventListener("submit", handleFormSubmit);
  }
}

// Function to handle when WebSocket connection is closed
function onSocketClose(event) {
  console.log("Clients WebSocket connection closed");
}

// Function to handle WebSocket errors
function onSocketError(error) {
  console.error("Clients WebSocket error:", error);
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
  // First, let's clear the existing content
  clientsInfo.innerHTML = "";

  // Create a heading
  const heading = document.createElement("h2");
  heading.textContent = `Connected Agents (${Object.keys(agents).length}):`;
  clientsInfo.appendChild(heading);

  // Create an accordion
  const accordion = document.createElement("div");
  accordion.classList.add("accordion");
  accordion.id = "connectedAgentsAccordion";

  // Create an accordion item for each agent
  Object.entries(agents).forEach(([agentId, agentInfo], index) => {
    const accordionItem = document.createElement("div");
    accordionItem.classList.add("accordion-item");

    // Accordion header
    const accordionHeader = document.createElement("h2");
    accordionHeader.classList.add("accordion-header");

    const button = document.createElement("button");
    button.classList.add("accordion-button", "collapsed");
    button.type = "button";
    button.setAttribute("data-bs-toggle", "collapse");
    button.setAttribute("data-bs-target", `#collapse${index + 1}`);
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", `collapse${index + 1}`);
    button.textContent = agentId;

    const badge = document.createElement("span");
    badge.classList.add("badge", "bg-primary", "rounded-pill", "ms-4");
    badge.textContent = "Connected";
    button.appendChild(badge);

    accordionHeader.appendChild(button);
    accordionItem.appendChild(accordionHeader);

    // Accordion body
    const accordionBody = document.createElement("div");
    accordionBody.id = `collapse${index + 1}`;
    accordionBody.classList.add("accordion-collapse", "collapse");

    const bodyContent = document.createElement("div");
    bodyContent.classList.add("accordion-body");
    bodyContent.innerHTML = `
      <p>Username: ${agentInfo.username}</p>
      <p>OS: ${agentInfo.os}</p>
    `;

    accordionBody.appendChild(bodyContent);
    accordionItem.appendChild(accordionBody);

    // Akordionı ana akordiyon alanına ekleyelim
    accordion.appendChild(accordionItem);
  });

  clientsInfo.appendChild(accordion);
}

// Function to render the command form
function renderCommandForm(agents) {
  const formHTML = `
    <div class="command-form-container">
        <div class="command-form border rounded p-4 mt-4">
          <h2 class="mb-4">Command</h2>
          <div class="row mt-4">
            <div class="col">
            <form method="post" id="commandForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <div class="mb-3">
                  <label for="agent" class="form-label">Select Agent:</label>
                  <select class="form-select" name="agent" id="agent" required>
                    <option value="">Select an agent</option>
                    <option value="all">All</option>
                    ${Object.entries(agents)
                      .map(
                        ([agentId, _]) => `
                      <option value="${agentId}">${agentId}</option>
                    `
                      )
                      .join("")}
                  </select>
                </div>
                <div class="mb-3">
                  <label for="command" class="form-label">Enter Command:</label>
                  <input type="text" class="form-control" id="command" name="command" placeholder="Type your command here" required>
                </div>
                <button type="submit" class="btn btn-primary">Send Command</button>
              </form>
            </div>
          </div>
        </div>
    </div>
  `;

  commandFormContainer.innerHTML = formHTML;
}

// WebSocket connection
const socketClients = new WebSocket("ws://localhost:8000/ws/clients/");

// Event listeners for WebSocket
socketClients.onopen = onSocketOpen;
socketClients.onmessage = onSocketMessage;
socketClients.onclose = onSocketClose;
socketClients.onerror = onSocketError;
