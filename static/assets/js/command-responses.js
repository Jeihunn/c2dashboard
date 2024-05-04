function updateResponseContainer(commandResponses) {
    const responseContainer = document.querySelector('.response-container');

    // If there are command responses
    if (commandResponses) {
        let htmlContent = '<div class="response-header">Command Responses:</div>';
        htmlContent += '<div class="terminal-output">';
        htmlContent += '<ul class="response-list">';
        
        // Generate HTML content for each command response
        Object.entries(commandResponses).forEach(([clientAddress, directoryPath]) => {
            htmlContent += `<li><span class="command">${clientAddress}:</span> <span class="directory">${directoryPath}</span></li>`;
        });

        htmlContent += '</ul></div>';
        responseContainer.innerHTML = htmlContent;
    } else {
        // If there are no command responses, display an appropriate message
        responseContainer.innerHTML = '<p class="no-response">No command responses available.</p>';
    }
}

// WebSocket connection
const socketCommandResponses = new WebSocket('ws://localhost:8000/ws/command-responses/');

// When the connection is started
socketCommandResponses.onopen = function(event) {
    console.log('WebSocket connection established.');
};

// When the connection is closed
socketCommandResponses.onclose = function(event) {
    console.log('WebSocket connection closed.');
};

// When message is received
socketCommandResponses.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const commandResponses = data.command_responses;
    
    console.log('Received command responses:', commandResponses);
    
    // Update page
    updateResponseContainer(commandResponses);
};

// When an error occurs
socketCommandResponses.onerror = function(error) {
    console.error('WebSocket error:', error);
};
