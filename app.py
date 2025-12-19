import os
import fitz
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from reportlab.pdfgen import canvas
from flask import send_from_directory

app = Flask(__name__)

PDF_UPLOAD = "uploads/pdfs"
IMG_UPLOAD = "uploads/images"
PDF_IMG_OUT = "output/pdf_to_images"
IMG_PDF_OUT = "output/images_to_pdf"

for d in [PDF_UPLOAD, IMG_UPLOAD, PDF_IMG_OUT, IMG_PDF_OUT]:
    os.makedirs(d, exist_ok=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/pdf")
def pdf_page():
    return render_template("pdf_to_image.html")


@app.route("/image")
def image_page():
    return render_template("image_to_pdf.html")


# ---------- PDF → IMAGE ----------
@app.route("/convert-pdf", methods=["POST"])
def convert_pdf():
    files = request.files.getlist("pdfs")
    fmt = request.form.get("format", "jpg").lower()

    for pdf in files:
        filename = secure_filename(pdf.filename)
        pdf_path = os.path.join(PDF_UPLOAD, filename)
        pdf.save(pdf_path)

        base = os.path.splitext(filename)[0]
        out_folder = os.path.join(PDF_IMG_OUT, base)
        os.makedirs(out_folder, exist_ok=True)

        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            pix = doc.load_page(i).get_pixmap(dpi=300)
            pix.save(os.path.join(out_folder, f"{base}_page_{i+1}.{fmt}"))

@app.route("/download/image/<folder>/<filename>")
def download_single_image(folder, filename):
    folder_path = os.path.join(PDF_IMG_OUT, folder)
    return send_from_directory(
        folder_path,
        filename,
        as_attachment=True
    )

@app.route("/view/<folder>/<filename>")
def view_image(folder, filename):
    return render_template(
        "image_view.html",
        folder=folder,
        filename=filename
    )

@app.route("/output/pdf_to_images/<folder>/<filename>")
def serve_image(folder, filename):
    return send_from_directory(
        os.path.join(PDF_IMG_OUT, folder),
        filename
    )

    # ✅ REDIRECT (VERY IMPORTANT)
    return redirect(url_for("dashboard"))


# ---------- IMAGE → PDF ----------
@app.route("/convert-images", methods=["POST"])
def convert_images():
    images = request.files.getlist("images")
    pdf_name = request.form.get("pdf_name", "output")

    out_pdf = os.path.join(IMG_PDF_OUT, f"{pdf_name}.pdf")
    c = canvas.Canvas(out_pdf)

    for img in images:
        name = secure_filename(img.filename)
        path = os.path.join(IMG_UPLOAD, name)
        img.save(path)

        im = Image.open(path)
        w, h = im.size
        c.setPageSize((w, h))
        c.drawImage(path, 0, 0, w, h)
        c.showPage()

    c.save()

    # ✅ REDIRECT (VERY IMPORTANT)
    return redirect(url_for("dashboard"))


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    image_folders = sorted(os.listdir(PDF_IMG_OUT))
    pdf_files = sorted(os.listdir(IMG_PDF_OUT))
    return render_template(
        "dashboard.html",
        image_folders=image_folders,
        pdf_files=pdf_files
    )


# ---------- PREVIEW IMAGES ----------
@app.route("/preview/images/<folder>")
def preview_images(folder):
    folder_path = os.path.join(PDF_IMG_OUT, folder)
    images = sorted(os.listdir(folder_path))
    return render_template(
        "preview.html",
        title=folder,
        images=images,
        folder=folder
    )


# ---------- SERVE IMAGE FILE ----------
@app.route("/image-file/<folder>/<filename>")
def image_file(folder, filename):
    return send_file(os.path.join(PDF_IMG_OUT, folder, filename))


# ---------- DOWNLOAD PDF ----------
@app.route("/preview/pdf/<filename>")
def preview_pdf(filename):
    return send_file(os.path.join(IMG_PDF_OUT, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # 🔥 allow LAN access
        port=5000,        # 🔧 change port here
        debug=False
    )
