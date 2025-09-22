from pathlib import Path
import PyPDF2

# Get project root (one level above app folder)
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"

# List all PDFs in data folder
pdf_files = list(data_dir.glob("*.pdf"))
print("PDFs found:", pdf_files)

# Read content from each PDF
for pdf_file in pdf_files:
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    print(f"\nContent of {pdf_file.name} (first 500 chars):\n{text[:500]}")
