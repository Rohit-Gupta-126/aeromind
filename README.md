# AeroMind
**Multi-Agent GenAI Framework for Engineering Document Intelligence**

AeroMind is a modular, explainable, document-grounded GenAI system designed to answer engineering queries using *only* verified technical documents. It emphasizes safety, determinism, and explainability, making it suitable for aerospace and other safety-critical domains.

---

## 1. Core Philosophy
*   **Read Before Speak:** Answers are strictly grounded in retrieved document context (RAG).
*   **Explainability:** Every response includes a confidence level and source citations.
*   **Safety First:** The system explicitly states uncertainty and refuses to speculate.
*   **Multi-Agent Architecture:** Specialized agents handle routing, retrieval, generation, and verification.

---

## 2. Architecture & Data Flow

```ascii
                                    +-----------------+
                                    |  Client (API)   |
                                    +--------+--------+
                                             |
                                             v
                                    +--------+--------+
                                    | FastAPI Backend |
                                    +--------+--------+
                                             |
                                             v
                                  +----------+----------+
                                  | Workflow Orchestrator|
                                  +----------+----------+
                                             |
                                             v
                                    +--------+--------+
                                    |   Router Agent  |
                                    +--------+--------+
                                             |
           +---------------------------------+---------------------------------+
           |                                 |                                 |
           v                                 v                                 v
+----------+----------+           +----------+----------+           +----------+----------+
|  Engineering Agent  |           |    Safety Agent     |           |   Unsupported       |
+----------+----------+           +----------+----------+           +----------+----------+
           |                                 |
           | (Retrieves Context)             |
           v                                 |
+----------+----------+                      |
|      RAG Service    |                      |
+----------+----------+                      |
           |                                 |
           v                                 |
+----------+----------+                      |
|    Verifier Agent   | <--------------------+
+----------+----------+
           |
           v
+----------+----------+
|  Response Formatter |
+----------+----------+
           |
           v
    Final Response
```

### Execution Steps
1.  **Request:** Client sends a question to `/ask`.
2.  **Routing:** `Router Agent` classifies the query (Engineering, Safety, or Unsupported) using an LLM.
3.  **Retrieval & Generation:** The selected agent retrieves relevant chunks from the FAISS vector DB and generates a structured JSON answer.
4.  **Verification:** The `Verifier Agent` cross-checks the answer against the source text to detect hallucinations.
5.  **Formatting:** The internal JSON is converted into a clean Markdown report.

---

## 3. Project Structure

```text
aeromind/
├── app/
│   ├── agents/          # Router, Engineering, Safety, Verifier agents
│   ├── api/             # FastAPI routes and schemas
│   ├── core/            # LLM wrapper, Embeddings, VectorDB logic
│   ├── graph/           # Workflow orchestration (State management)
│   ├── models/          # Pydantic models and TypedDicts
│   ├── services/        # RAG retrieval and Response formatting
│   └── main.py          # Application entry point
├── data/
│   ├── documents/       # Source PDFs
│   └── vectorstore/     # FAISS index
├── scripts/
│   └── ingest.py        # Document ingestion script
├── tests/               # Integration tests
└── requirements.txt
```

---

## 4. Setup & Usage

### Prerequisites
*   Python 3.10+
*   Node.js 18+ & pnpm (for Frontend)
*   Google Gemini API Key (in `.env` as `GEMINI_API_KEY`)

### Installation

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd aeromind-ui
pnpm install
```

### Ingestion
Place PDF documents in `data/documents/` and run:
```bash
python scripts/ingest.py
```
*Alternatively, use the Web UI to upload documents.*

### Running the System

**Backend:**
```bash
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd aeromind-ui
pnpm dev
```
Access the UI at: `http://localhost:3000`

### API Endpoints

**POST** `/ask`
```json
{
  "question": "What causes jet engine vibration?"
}
```

**POST** `/upload`
*   Multipart form data: `file` (PDF)
*   Uploads and immediately re-indexes the knowledge base.

---

## 5. Key Features
*   **Web Interface:** Modern Next.js UI for querying and document upload.
*   **Strict RAG:** Uses FAISS for vector search and HuggingFace embeddings.
*   **Self-Correction:** The Verifier Agent downgrades confidence if the answer isn't fully supported by the text.
*   **Structured Output:** Engineering answers are formatted with Summary, Key Findings, Risks, and Assumptions.
*   **Extensible:** New agents (e.g., Compliance, Maintenance) can be added by updating the Router.

---

**AeroMind is not a chatbot.** It is a controlled, explainable engineering tool.
