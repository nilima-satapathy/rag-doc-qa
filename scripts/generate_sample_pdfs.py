"""
Create small sample PDFs under data/ for RAG experiments.

Run once (or anytime you want to regenerate):
  python scripts/generate_sample_pdfs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Plain ASCII-heavy text so default fonts render cleanly.
DOCS: dict[str, list[str]] = {
    "project1-api-automation-notes.pdf": [
        "Project 1 - API Automation Framework (Notes)",
        "",
        "Goal: Maintainable REST API tests in Python for an SDET portfolio.",
        "Repo: api-automation-pytest",
        "Target API: JSONPlaceholder (public demo, no auth).",
        "",
        "Stack: Python, Pytest, requests, jsonschema, pytest-html, GitHub Actions.",
        "",
        "Architecture:",
        "tests call fixtures in conftest, which create an ApiClient.",
        "ApiClient wraps requests.Session with base URL, headers, and timeout.",
        "Default timeout is 10 seconds.",
        "Payloads live in data/payloads. Schemas live in data/schemas.",
        "",
        "Coverage:",
        "About 77 automated tests total.",
        "GET and parametrize coverage around 33 cases.",
        "Write operations POST PUT PATCH DELETE around 12 cases.",
        "JSON Schema validation around 12 cases.",
        "Negative and edge cases around 20 cases.",
        "",
        "Important honesty: JSONPlaceholder fakes writes. It echoes data and",
        "returns success-like codes but does not really persist new records.",
        "So write tests assert status and response body echo, not GET-after-POST.",
        "",
        "Negative testing note:",
        "Unknown resource ids usually return HTTP 404.",
        "A valid filter with zero matches often returns HTTP 200 and an empty list.",
        "Those two outcomes mean different things and should not be mixed up.",
        "",
        "CI: GitHub Actions runs pytest on push and uploads an HTML report artifact.",
    ],
    "project2-playwright-pom-notes.pdf": [
        "Project 2 - Playwright UI Suite with Page Object Model (Notes)",
        "",
        "Goal: Browser UI automation proof for SDET and AI Test roles.",
        "Repo: playwright-pom-saucedemo",
        "Target app: https://www.saucedemo.com",
        "",
        "Stack: Python, Playwright, Pytest, pytest-playwright, pytest-html, GitHub Actions.",
        "",
        "Page Object Model (POM):",
        "Each page is a class. Selectors and actions live in pages/.",
        "Tests describe user intent only, not raw CSS selectors.",
        "Pages include BasePage, LoginPage, InventoryPage, CartPage, CheckoutPage.",
        "",
        "Journeys covered:",
        "Successful login lands on the Products page.",
        "Add Sauce Labs Backpack to cart and verify cart contents.",
        "Add two items and verify badge count.",
        "Full checkout to the thank-you page message.",
        "Checkout then logout back to the login form.",
        "",
        "Negative login cases:",
        "Wrong password shows credentials error.",
        "locked_out_user shows locked-out error.",
        "Missing username or password shows required-field errors.",
        "",
        "Demo credentials for happy path: standard_user and secret_sauce.",
        "",
        "Failure debugging:",
        "pytest.ini keeps screenshot and Playwright trace only on failure.",
        "Artifacts go under test-results. Open a trace with:",
        "playwright show-trace path/to/trace.zip",
        "",
        "CI runs headless Chromium on Ubuntu with playwright install chromium --with-deps.",
        "Suite size: 9 automated UI tests. Milestones M1 through M6 complete.",
    ],
    "rag-and-ai-quality-notes.pdf": [
        "RAG and AI Quality - Short Study Notes",
        "",
        "What is RAG?",
        "Retrieval-Augmented Generation means: find relevant document pieces first,",
        "then ask the language model to answer using those pieces.",
        "The goal is fewer hallucinations and answers grounded in your files.",
        "",
        "Pipeline stages:",
        "1. Ingest: load PDFs and extract text.",
        "2. Chunk: split text into smaller overlapping windows.",
        "3. Embed: turn each chunk into a numeric vector of meaning.",
        "4. Store: save vectors in a vector database such as Chroma or FAISS.",
        "5. Retrieve: embed the question and find the closest chunks.",
        "6. Generate: LLM answers using retrieved context and should cite sources.",
        "",
        "Chunk size tradeoffs:",
        "Chunks that are too small may miss surrounding context.",
        "Chunks that are too large add noise and weaken search precision.",
        "Overlap helps keep sentence context across chunk boundaries.",
        "",
        "When the documents do not contain the answer, a good system should say",
        "I do not know, instead of inventing facts.",
        "",
        "Evaluation ideas for a portfolio RAG app:",
        "Use at least 10 hand-written questions.",
        "Measure retrieval hit-rate at k equals 3: was the right chunk in the top 3?",
        "Record average latency and note known failure modes.",
        "",
        "RAG vs fine-tuning:",
        "Use RAG when knowledge lives in changing documents and must be citable.",
        "Use fine-tuning more for style, format, or behavior, not daily PDF updates.",
    ],
}


def write_pdf(path: Path, lines: list[str]) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Keep cursor at left margin after each multi_cell (avoids width=0 errors)
    for i, line in enumerate(lines):
        if not line:
            pdf.ln(6)
            continue
        if i == 0:
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=12)
            pdf.ln(2)
        else:
            pdf.set_font("Helvetica", size=12)
            pdf.multi_cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(path))
    print(f"wrote {path.name}")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    for name, lines in DOCS.items():
        write_pdf(DATA / name, lines)
    print(f"Done. {len(DOCS)} PDFs in {DATA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
