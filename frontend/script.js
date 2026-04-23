const API_URL = "http://127.0.0.1:8000";

// 🔹 Upload File
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const status = document.getElementById("uploadStatus");

    const file = fileInput.files[0];

    if (!file) {
        status.innerText = "Please select a file";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_URL}/upload/`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        status.innerText = data.message;

    } catch (error) {
        console.error(error);
        status.innerText = "Upload failed!";
    }
}


// 🔹 Ask Question (CARD UI)
async function askQuestion() {
    const query = document.getElementById("queryInput").value;
    const responseDiv = document.getElementById("response");

    if (!query) {
        responseDiv.innerHTML = "<p>Please enter a question</p>";
        return;
    }

    responseDiv.innerHTML = "<p>Searching...</p>";

    try {
        const res = await fetch(`${API_URL}/search/?query=${query}`);
        const data = await res.json();

        if (!data || data.length === 0) {
            responseDiv.innerHTML = "<p>No results found</p>";
            return;
        }

        let seen = new Set();
        let output = "";

        data.forEach(item => {
            if (!seen.has(item.filename)) {
                seen.add(item.filename);

                output += `
                <div class="card">
                    <div class="card-header">
                        <span class="file-name">${item.filename}</span>
                        <span class="score">Score: ${item.score}</span>
                    </div>
                    <div class="card-body">
                        ${item.relevant_text}
                    </div>
                </div>
                `;
            }
        });

        responseDiv.innerHTML = output;

    } catch (error) {
        console.error(error);
        responseDiv.innerHTML = "<p>Error fetching results</p>";
    }
}