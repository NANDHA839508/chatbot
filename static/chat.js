function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim().toLowerCase();
    let chatBox = document.getElementById("chat-box");

    if (userInput === "") return;

    // Append user's message to chat box
    let userMessage = `<div class='user-message'>${userInput}</div>`;
    chatBox.innerHTML += userMessage;

    // Greeting detection
    let greetings = ["hi", "hello", "hey", "help"];
    if (greetings.includes(userInput)) {
        chatBox.innerHTML += document.getElementById("suggestions").innerHTML;
    }

    // Navigation Logic
    let navigationLinks = {
        "chart": "chart.html",
        "investment": "/investment",
        "long-term investment": "long-term-investment.html",
        "short-term investment": "short-term-investment.html",
        "stock price": "Stock Price.html"
    };

    if (navigationLinks[userInput]) {
        window.location.href = navigationLinks[userInput];  // Redirect to the respective page
        return;
    }

    // Clear input field
    document.getElementById("user-input").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}
