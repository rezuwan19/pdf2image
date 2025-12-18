import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from PIL import Image

app = Flask(__name__)

UPLOAD_PDF = "uploads/pdfs"
UPLOAD_IMG = "uploads/images"
OUTPUT_DIR = "output/pdf_to_images"

# Create folders
for folder in [UPLOAD_PDF, UPLOAD_IMG, OUTPUT_DIR]:
    os.makedirs(folder, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pdf-to-images", methods=["POST"])
def pdf_to_images():
    files = request.files.getlist("pdfs")

    for pdf in files:
        filename = secure_filename(pdf.filename)
        pdf_path = os.path.join(UPLOAD_PDF, filename)
        pdf.save(pdf_path)

        folder_name = os.path.splitext(filename)[0]
        out_folder = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(out_folder, exist_ok=True)

        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=300)
            pix.save(os.path.join(out_folder, f"page_{i+1}.png"))

    return "OK"


@app.route("/images-to-pdf", methods=["POST"])
def images_to_pdf():
    files = request.files.getlist("images")
    output_pdf = "output/images_to_pdf/output.pdf"
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    c = canvas.Canvas(output_pdf)

    for img in files:
        filename = secure_filename(img.filename)
        path = os.path.join(UPLOAD_IMG, filename)
        img.save(path)

        image = Image.open(path)
        w, h = image.size
        c.setPageSize((w, h))
        c.drawImage(path, 0, 0, w, h)
        c.showPage()

    c.save()
    return send_file(output_pdf, as_attachment=True)


@app.route("/dashboard")
def dashboard():
    folders = sorted(os.listdir(OUTPUT_DIR))
    return render_template("dashboard.html", pdf_folders=folders)


@app.route("/preview/<folder>")
def preview(folder):
    folder_path = os.path.join(OUTPUT_DIR, folder)
    images = sorted(os.listdir(folder_path))
    return render_template("preview.html", folder=folder, images=images)


@app.route("/image/<folder>/<filename>")
def image(folder, filename):
    return send_file(os.path.join(OUTPUT_DIR, folder, filename))


if __name__ == "__main__":
    app.run(debug=True)
