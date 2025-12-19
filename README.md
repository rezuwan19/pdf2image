# 📄 PDF2Image

A simple **Flask-based web application** that allows users to:

- ✅ Convert **PDF → Images** (JPG / JPEG / PNG)
- ✅ Convert **Images → PDF**
- ✅ Preview converted images
- ✅ Download single images
- ✅ Download generated PDFs
- ✅ Search files and folders from the dashboard

This project is lightweight, beginner-friendly, and suitable for local or LAN usage.

---

## 🚀 Features

### 🔹 PDF → Image
- Upload one or multiple PDF files
- Convert each page to images
- Choose output format (JPG / JPEG / PNG)
- Automatically creates folders per PDF
- Preview images page by page
- Download individual images

### 🔹 Image → PDF
- Upload multiple images
- Set custom PDF name
- Generates a single PDF
- Click on PDF to download from dashboard

### 🔹 Dashboard
- View all converted files
- Clickable folders and files
- 🔍 Search system (real-time)
- Clean and simple UI

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **PDF Processing:** PyMuPDF (fitz)
- **Image Processing:** Pillow
- **PDF Creation:** ReportLab
- **Frontend:** HTML, CSS, JavaScript

---

## 📂 Project Structure

```bash
pdf-image-converter/

├── app.py
├── requirements.txt
├── LICENSE.md
├── README.md
│
├── data/
│ └── usage.json
│
├── uploads/
│ ├── pdfs/
│ └── images/
│
├── output/
│ ├── pdf_to_images/
│ └── images_to_pdf/
│
├── static/
│ ├── css/
│ │ └── style.css
│ └── js/
│   ├── main.js
│   └── dashboard.js
│
└── templates/
   ├── home.html
   └── dashboard.html
   └── pdf_to_image.html
   └── image_to_pdf.html
   └── preview.html
   └── image_view.html
```
---

## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/pdf-image-converter.git
cd pdf-image-converter
```
### 2️⃣ Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### 3️⃣ Install dependencies
```pip
pip install -r requirements.txt
```
### 4️⃣ Run the application
```python
python app.py
```
### 5️⃣ Open in browser
```bash
http://localhost:5000
```
---
## 📸 Screenshots