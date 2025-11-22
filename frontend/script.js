const API_URL = "http://127.0.0.1:8000/query/";

async function sendQuery() {
    const query = document.getElementById("queryInput").value.trim();
    const mode = document.getElementById("modeSelect").value;

    if (!query) {
        alert("Please enter a query.");
        return;
    }

    // Clear old output
    document.getElementById("answerBox").innerHTML = "Loading...";
    document.getElementById("resultsBox").innerHTML = "";

    // Build request
    const payload = {
        query: query,
        mode: mode
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Show answer
        document.getElementById("answerBox").innerHTML = data.answer;

        // Show chunks
        const resultsDiv = document.getElementById("resultsBox");
        resultsDiv.innerHTML = "";

        data.results.forEach(chunk => {
            const card = `
                <div class="border p-4 rounded-lg bg-white shadow">
                    <p><b>File:</b> ${chunk.file_name}</p>
                    <p><b>Snippet:</b> ${chunk.snippet}</p>
                    <a class="text-blue-600"
                        href="${chunk.drive_link}"
                        target="_blank">Open in Drive</a>
                </div>
            `;
            resultsDiv.innerHTML += card;
        });

    } catch (error) {
        document.getElementById("answerBox").innerHTML = "Error: " + error;
    }
}
