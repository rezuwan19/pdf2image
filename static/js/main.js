let files = [];
const input = document.getElementById('pdfInput');
const list = document.getElementById('fileList');
const bar = document.getElementById('bar');
const status = document.getElementById('status');


input.onchange = () => {
    for (let f of input.files) {
        if (!files.some(x => x.name === f.name)) files.push(f);
    }
    input.value = '';
    render();
};


function render() {
    list.innerHTML = '';
    files.forEach((f, i) => {
        list.innerHTML += `<li>${i + 1}. ${f.name}</li>`;
    });
}


function upload() {
    if (!files.length) return alert('Select PDF');
    const fd = new FormData();
    files.forEach(f => fd.append('pdfs', f));


    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/pdf-to-images');


    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            bar.style.width = (e.loaded / e.total * 100) + '%';
            status.innerText = 'Uploading...';
        }
    };


    xhr.onload = () => {
        status.innerText = 'Done';
        bar.style.width = '100%';
        window.location.href = '/dashboard';
    };


    xhr.send(fd);
}