# RAG Document Q&A (`rag-doc-qa`)

Chat over **your PDFs** with retrieval + answers + citations (full pipeline in later milestones).

| | |
|---|---|
| **Status** | In progress — **M1 complete** |
| **Stack (planned)** | Python · pypdf · embeddings · Chroma · LLM · Streamlit |
| **Progress board** | [ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey) |

---

## Milestone 1 (done) — PDF load + chunking

Load sample PDFs, split text into overlapping chunks, print a summary.

No embeddings or LLM yet (that is M2+).

### Setup (Windows / PowerShell)

```powershell
cd Desktop\Code\rag-doc-qa
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_pdfs.py
```

### Run M1

```powershell
python scripts/run_m1_chunk.py
```

### Configure chunk size (no code change)

```powershell
# Option A — env vars
$env:RAG_CHUNK_SIZE = "500"
$env:RAG_CHUNK_OVERLAP = "80"
python scripts/run_m1_chunk.py

# Option B — CLI flags
python scripts/run_m1_chunk.py --chunk-size 400 --chunk-overlap 80 --preview 3
```

| Setting | Default | Meaning |
|---------|---------|---------|
| `chunk_size` | 800 | Max characters per chunk |
| `chunk_overlap` | 120 | Shared chars between neighboring chunks |

**Why overlap?** If a sentence is cut at a boundary, the next chunk still carries some of the previous words so meaning is less often lost.

### Sample documents (`data/`)

| File | Content |
|------|---------|
| `project1-api-automation-notes.pdf` | API suite notes (ApiClient, 77 tests, negatives) |
| `project2-playwright-pom-notes.pdf` | Playwright POM / SauceDemo notes |
| `rag-and-ai-quality-notes.pdf` | RAG pipeline + eval basics |

---

## Project layout (M1)

```text
rag-doc-qa/
├── README.md
├── MILESTONES.md
├── requirements.txt
├── data/                      # sample PDFs
├── scripts/
│   ├── generate_sample_pdfs.py
│   └── run_m1_chunk.py
└── src/
    ├── config.py              # chunk size / paths
    └── ingest.py              # load + chunk
```

**Next (M2):** Embed chunks → store in Chroma → similarity search from the CLI.
