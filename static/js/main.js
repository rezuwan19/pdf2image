let pdfFiles = [];
let imgFiles = [];

const pdfInput = document.getElementById("pdfInput");
const imgInput = document.getElementById("imgInput");
const bar = document.getElementById("bar");

if (pdfInput) {
    pdfInput.onchange = () => {
        for (let f of pdfInput.files) {
            if (!pdfFiles.find(x => x.name === f.name)) {
                pdfFiles.push(f);
            }
        }
        pdfInput.value = "";
        renderList(pdfFiles, "fileList");
    };
}

if (imgInput) {
    imgInput.onchange = () => {
        for (let f of imgInput.files) {
            if (!imgFiles.find(x => x.name === f.name)) {
                imgFiles.push(f);
            }
        }
        imgInput.value = "";
        renderList(imgFiles, "imgList");
    };
}

function renderList(files, elementId) {
    const ul = document.getElementById(elementId);
    ul.innerHTML = "";
    files.forEach((f, i) => {
        ul.innerHTML += `<li>${i + 1}. ${f.name}</li>`;
    });
}

function uploadPDF() {
    if (!pdfFiles.length) return alert("Select PDFs");

    const fd = new FormData();
    pdfFiles.forEach(f => fd.append("pdfs", f));
    fd.append("format", document.getElementById("format").value);

    sendXHR(fd, "/convert-pdf");
}

function uploadImages() {
    if (!imgFiles.length) return alert("Select images");

    const fd = new FormData();
    imgFiles.forEach(f => fd.append("images", f));
    fd.append("pdf_name", document.getElementById("pdfName").value);

    sendXHR(fd, "/convert-images");
}

function sendXHR(fd, url) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            bar.style.width = (e.loaded / e.total * 100) + "%";
        }
    };

    xhr.onload = () => {
        window.location.href = "/dashboard";
    };

    xhr.send(fd);
}
