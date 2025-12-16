async function extract() {
    const fileInput = document.getElementById("fileInput");
    const tableBody = document.querySelector("#resultTable tbody");

    // Clear previous results
    tableBody.innerHTML = "";

    if (!fileInput.files.length) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/extract", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("API RESPONSE:", data);

        if (!data.success) {
            alert("Extraction failed: " + data.error);
            return;
        }

        const fields = data.fields;

        if (!fields || Object.keys(fields).length === 0) {
            tableBody.innerHTML =
                "<tr><td colspan='3'>No fields detected</td></tr>";
            return;
        }

        for (const key in fields) {
            const value = fields[key].value ?? "";
            const confidence = fields[key].confidence ?? 0;

            let confidenceClass = "low";
            if (confidence >= 0.85) confidenceClass = "high";
            else if (confidence >= 0.6) confidenceClass = "medium";

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${key}</td>
                <td>${value}</td>
                <td>
                    <span class="${confidenceClass}">
                        ${confidence}
                    </span>
                </td>
            `;

            tableBody.appendChild(row);
        }

    } catch (error) {
        console.error(error);
        alert("Error connecting to backend");
    }
}
