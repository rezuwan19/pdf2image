import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_PDF = "uploads/pdfs"
UPLOAD_IMG = "uploads/images"
OUTPUT_DIR = "output/pdf_to_images"

# Create folders if not exist
for folder in [UPLOAD_PDF, UPLOAD_IMG, OUTPUT_DIR]:
    os.makedirs(folder, exist_ok=True)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pdf-to-images", methods=["POST"])
def pdf_to_images():
    files = request.files.getlist("pdfs")  # Multiple PDF support

    for pdf in files:
        filename = secure_filename(pdf.filename)
        pdf_path = os.path.join(UPLOAD_PDF, filename)
        pdf.save(pdf_path)

        # Create a folder with PDF filename (without extension)
        folder_name = os.path.splitext(filename)[0]
        out_folder = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(out_folder, exist_ok=True)

        # Convert PDF to images
        doc = fitz.open(pdf_path)
        for page_number in range(len(doc)):
            pix = doc.load_page(page_number).get_pixmap(dpi=300)
            image_name = f"page_{page_number+1}.png"
            pix.save(os.path.join(out_folder, image_name))

    return redirect("/dashboard")

@app.route("/images-to-pdf", methods=["POST"])
def images_to_pdf():
    files = request.files.getlist("images")
    out_folder = os.path.join("output/images_to_pdf")
    os.makedirs(out_folder, exist_ok=True)

    pdf_path = os.path.join(out_folder, "output.pdf")
    from reportlab.pdfgen import canvas
    from PIL import Image

    c = canvas.Canvas(pdf_path)

    for img in files:
        name = secure_filename(img.filename)
        path = os.path.join(UPLOAD_IMG, name)
        img.save(path)

        image = Image.open(path)
        w, h = image.size
        c.setPageSize((w, h))
        c.drawImage(path, 0, 0, w, h)
        c.showPage()

    c.save()
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    # List all folders (PDF converted images)
    pdf_folders = []
    if os.path.exists(OUTPUT_DIR):
        pdf_folders = sorted(os.listdir(OUTPUT_DIR))
    return render_template("dashboard.html", pdf_folders=pdf_folders)

if __name__ == "__main__":
    app.run(debug=True)
