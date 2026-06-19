import sys
from pathlib import Path
import pypdf
from ingestion.sanitizer import sanitize_all

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

def extract_text_from_pdf(pdf_path: Path, start_page: int = 0, end_page: int = None) -> str:
    """
    Extracts raw text blocks from a targeted local PDF file, normalized whitespaces,
    and returns a clean string payload for local LLM token parsing.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"Target PDF binary not found at: {pdf_path}")
    extracted_chunks = []

    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        total_pages = len(reader.pages)

        actual_end_page = min(end_page or total_pages, total_pages)

        for page_idx in range(start_page, actual_end_page):
            page = reader.pages[page_idx]
            page_text = page.extract_text()
            if page_text:
                extracted_chunks.append(page_text.strip())
        full_text = "\n".join(extracted_chunks)

        return sanitize_all(full_text)

if __name__ == "__main__":
    sample_pdf = PROJECT_ROOT / "data" /"raw" / "Algorithms-JeffE.pdf"

    try:
        print(f"🧪 Testing extraction on: {sample_pdf.name}")
        text = extract_text_from_pdf(sample_pdf, start_page=0, end_page=2)
        print(f"✅ Success! Extracted {len(text)} characters.")
        print("--- Preview (First 200 chars) ---")
        print(text[:200])
    except Exception as e:
        print(f"❌ Test Failed: {e}")