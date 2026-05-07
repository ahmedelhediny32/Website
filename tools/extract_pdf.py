import fitz
doc = fitz.open(r"d:\website\raw-assets\raw-assets.pdf")
with open(r"d:\website\pdf_text_2.txt", "w", encoding="utf-8") as f:
    for page in doc:
        f.write(page.get_text() + "\n")
