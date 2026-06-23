import pypdf
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
PDF_TARGET = PROJECT_ROOT / "data" / "raw" / "Algorithms-JeffE.pdf"

def find_text_in_pdf(pdf_path: Path, search_term: str):
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        print(f"DEBUG: Page 103 Text: {reader.pages[103].extract_text()[:500]}")
        for page_idx in range(len(reader.pages)):
            page_text = reader.pages[page_idx].extract_text()
            if not page_text:
                continue
            if search_term.lower() in page_text.lower():
                print(f"Found on page {page_idx}")
                # Show surrounding context
                idx = page_text.lower().find(search_term.lower())
                print(repr(page_text[max(0, idx-50):idx+100]))
                print("---")

find_text_in_pdf(PDF_TARGET, "tower of hanoi")
find_text_in_pdf(PDF_TARGET, "1.3")
