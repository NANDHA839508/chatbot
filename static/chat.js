function toggleSidebar() {
    document.querySelector(".sidebar").classList.toggle("hidden");
}

// Clears chat on frontend (does not clear server history)
function startNewChat() {
    document.getElementById("chatBox").innerHTML = "";
}

function sendMessage() {
    let userMessage = document.getElementById("userMessage").value.trim();
    if (userMessage === "") return;

    // Append user message to chat
    $("#chatBox").append("<p><strong>You:</strong> " + userMessage + "</p>");

    // Send request to Flask backend
    $.ajax({
        url: "/send_message",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: userMessage }),
        success: function (data) {
            $("#chatBox").append("<p><strong>Bot:</strong> " + data.bot_response + "</p>");
        },
        error: function () {
            $("#chatBox").append("<p><strong>Bot:</strong> Sorry, an error occurred.</p>");
        }
    });

    document.getElementById("userMessage").value = ""; // Clear input field
}

// Load chat history from backend
function loadChatHistory() {
    $.get("/chat_history", function (data) {
        let chatHistory = document.getElementById("chatHistory");
        chatHistory.innerHTML = "";
        data.forEach(chat => {
            chatHistory.innerHTML += `<p><strong>${chat[0]}:</strong> ${chat[1]}</p>`;
        });
    }).fail(function () {
        console.error("Error loading chat history");
    });
}

// Audio Recording (Speech-to-Text)
function recordAudio() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function (event) {
        let speechText = event.results[0][0].transcript;
        document.getElementById("userMessage").value = speechText;
        sendMessage();
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
    };
}

$(document).ready(function () {
    loadChatHistory();
});
