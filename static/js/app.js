document.getElementById("story-form").addEventListener("submit", function(event) {
    event.preventDefault();
    generateText();
});

document.getElementById("settings-form").addEventListener("submit", function(event) {
    event.preventDefault();
    saveApiKey();
});

async function saveApiKey() {
    const apiKey = document.getElementById("api-key").value;

    const response = await fetch("/save-api-key", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ "api-key": apiKey })
    });

    if (response.ok) {
        alert("API key saved successfully.");
    } else {
        alert("An error occurred while saving the API key. Please try again.");
    }
}


async function generateText() {
    const title = document.getElementById("title").value;
    const genre = document.getElementById("genre").value;
    const characters = document.getElementById("characters").value;
    const plot = document.getElementById("plot").value;
    const prompt = document.getElementById("prompt").value;

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, genre, characters, plot, prompt })
    });

    if (response.ok) {
        const generatedText = await response.text();
        const formattedText = formatText(generatedText);
        document.getElementById("generated-text").innerHTML = formattedText;
    } else {
        alert("An error occurred while generating text. Please try again.");
    }
}

function formatText(text) {
    return text.replace(/\n\n/g, "<br><br>").replace(/\n/g, "<br>");
}

// Retrieve saved values from local storage
const title = localStorage.getItem("title");
const genre = localStorage.getItem("genre");
const characters = localStorage.getItem("characters");
const plot = localStorage.getItem("plot");
const prompt = localStorage.getItem("prompt");

// Set input values
document.getElementById("title").value = title;
document.getElementById("genre").value = genre;
document.getElementById("characters").value = characters;
document.getElementById("plot").value = plot;
document.getElementById("prompt").value = prompt;

window.addEventListener("beforeunload", function() {
    localStorage.setItem("title", document.getElementById("title").value);
    localStorage.setItem("genre", document.getElementById("genre").value);
    localStorage.setItem("characters", document.getElementById("characters").value);
    localStorage.setItem("plot", document.getElementById("plot").value);
    localStorage.setItem("prompt", document.getElementById("prompt").value);
});

document.addEventListener("DOMContentLoaded", function() {
    // Retrieve saved values from local storage
    const title = localStorage.getItem("title");
    const genre = localStorage.getItem("genre");
    const characters = localStorage.getItem("characters");
    const plot = localStorage.getItem("plot");
    const prompt = localStorage.getItem("prompt");

    // Set input values
    document.getElementById("title").value = title;
    document.getElementById("genre").value = genre;
    document.getElementById("characters").value = characters;
    document.getElementById("plot").value = plot;
    document.getElementById("prompt").value = prompt;

    window.addEventListener("beforeunload", function() {
        localStorage.setItem("title", document.getElementById("title").value);
        localStorage.setItem("genre", document.getElementById("genre").value);
        localStorage.setItem("characters", document.getElementById("characters").value);
        localStorage.setItem("plot", document.getElementById("plot").value);
        localStorage.setItem("prompt", document.getElementById("prompt").value);
    });
});
