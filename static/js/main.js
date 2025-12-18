let selectedFiles = [];

const input = document.getElementById("pdfInput");
const list = document.getElementById("fileList");

input.addEventListener("change", () => {
    for (let file of input.files) {
        // Prevent duplicate files
        if (!selectedFiles.some(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    }
    renderList();
    input.value = ""; // IMPORTANT: reset input
});

function renderList() {
    list.innerHTML = "";
    selectedFiles.forEach((file, index) => {
        const li = document.createElement("li");
        li.textContent = `${index + 1}. ${file.name}`;
        list.appendChild(li);
    });
}

function submitPDFs() {
    if (selectedFiles.length === 0) {
        alert("Please select at least one PDF");
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append("pdfs", file);
    });

    fetch("/pdf-to-images", {
        method: "POST",
        body: formData
    })
        .then(() => {
            selectedFiles = [];
            renderList();
            window.location.href = "/dashboard";
        })
        .catch(err => alert("Upload failed"));
}
