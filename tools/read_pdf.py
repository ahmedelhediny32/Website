import sys

def extract_text(pdf_path):
    try:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                print("--- SUCCESS with PyPDF2 ---")
                print(text)
                return
        except ImportError:
            pass

        try:
            import fitz
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            print("--- SUCCESS with PyMuPDF ---")
            print(text)
            return
        except ImportError:
            pass
        
        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            print("--- SUCCESS with pypdf ---")
            print(text)
            return
        except ImportError:
            pass
        
        print("Error: No PDF parsing libraries found (tried PyPDF2, PyMuPDF/fitz, pypdf).")
        print("Please install one, for example: pip install PyPDF2")

    except Exception as e:
        print("Error reading PDF:", str(e))

if __name__ == "__main__":
    extract_text(r"d:\website\raw-assets\raw-assets.pdf")
