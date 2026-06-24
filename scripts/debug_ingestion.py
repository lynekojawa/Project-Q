import sys
import re
from pathlib import Path
import pypdf

# Add project root to sys.path for module imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Define target path with a fail-safe check
PDF_TARGET = PROJECT_ROOT / "data" / "raw" / "Algorithms-JeffE.pdf"


def scan_pdf_headers(pdf_path: Path):
    """
    Scans all pages in the PDF and prints lines that look like structural headers.
    Useful for identifying mismatch between DB titles and actual PDF content.
    """
    if not pdf_path.exists():
        print(f"CRITICAL ERROR: PDF not found at {pdf_path}")
        return

    reader = pypdf.PdfReader(pdf_path)
    print(f"--- Scanning PDF for structural headers in: {pdf_path.name} ---")

    # Regex to catch patterns like '3.2', '12.2.', '3.2 Aside'
    header_pattern = re.compile(r'^\s*\d+\.\d+')

    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue

        lines = text.split('\n')
        for line in lines:
            clean_line = line.strip()
            # If line starts with a number pattern, it's a potential header
            if header_pattern.match(clean_line):
                print(f"Page {page_idx} | Found header: '{clean_line}'")


if __name__ == "__main__":
    # Execute the scan
    scan_pdf_headers(PDF_TARGET)
