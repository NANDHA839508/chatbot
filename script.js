document.addEventListener("DOMContentLoaded", function() {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.classList.add(isUser ? "user-message" : "bot-message");
        messageElement.textContent = message;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function handleUserMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = "";

            // Simulate bot response
            setTimeout(() => {
                addMessage("This is a simulated response from the chatbot.");
            }, 1000);
        }
    }

    sendButton.addEventListener("click", handleUserMessage);
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            handleUserMessage();
        }
    });
});