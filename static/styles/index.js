function sendMessage() {
    let input = document.getElementById("userInput").value;
    document.getElementById("chatbox").innerHTML += "<p><b>You:</b> " + input + "</p>";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("chatbox").innerHTML += "<p><b>Bot:</b> " + data.response + "</p>";
    });

    document.getElementById("userInput").value = "";
}