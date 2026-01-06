# AeroMind
**Multi-Agent GenAI Framework for Engineering Document Intelligence**

AeroMind is a modular, explainable, document-grounded GenAI system designed to answer engineering queries using *only* verified technical documents. It emphasizes safety, determinism, and explainability, making it suitable for aerospace and other safety-critical domains.

---

## 🚀 Key Features

*   **Zero Hallucination Policy:** A dedicated `Verifier Agent` cross-checks every generated claim against the source text to ensure factual accuracy.
*   **Multi-Agent Workflow:** Specialized agents manage the pipeline:
    *   **Router:** Classifies queries into Engineering, Safety, or Unsupported categories.
    *   **Domain Agents:** Specialize in technical RAG and safety protocol compliance.
    *   **Verifier:** Validates answers against retrieved chunks, providing a `PASS/PARTIAL/FAIL` status.
*   **Explainable RAG:** Every response includes confidence levels, source citations, and verification notes.
*   **Dynamic Knowledge Base:** Supports real-time PDF uploads and automated re-indexing via the UI.
*   **Structured Intelligence:** Outputs are formatted for engineers, highlighting findings, risks, and assumptions.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, LangChain/LangGraph (concept)
- **AI Models:** Google Gemini (2.0-flash, 1.5-pro, etc.)
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Frontend:** Next.js, React, Tailwind CSS, pnpm

---

## 📐 Architecture & Data Flow

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

### Execution Pipeline
1.  **Request:** User asks a question via the `/ask` endpoint.
2.  **Routing:** The `Router Agent` uses an LLM to determine the appropriate domain.
3.  **RAG Execution:** The selected agent searches the FAISS index for relevant document chunks and generates a structured JSON response.
4.  **Verification:** The `Verifier Agent` compares the generated answer with the retrieved context. It assigns a status:
    - `PASS`: Every claim is supported by the context.
    - `PARTIAL`: Some claims are unsupported or speculative.
    - `FAIL`: Significant hallucinations detected.
5.  **Formatting:** The Response Formatter converts internal structured data into a detailed Markdown report.

---

## 📂 Project Structure

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
└── run.py               # Main entry point to start backend
```

---

## 🔧 Setup & Installation

### Prerequisites
*   Python 3.10+
*   Node.js 18+ & pnpm
*   Google Gemini API Key

### 1. Clone & Environment
```bash
git clone <repo-url>
cd aeromind
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Ingestion
Add your PDFs to [data/documents/](data/documents/) and run:
```bash
python scripts/ingest.py
```

---

## 🚦 Running the System

### Backend
```bash
python run.py
```
*API will be available at `http://localhost:8000`*

### Frontend
```bash
cd aeromind-ui
pnpm install
pnpm dev
```
*Access the UI at `http://localhost:3000`*

---

## 📡 API Documentation

### `POST /ask`
Submit a question to the multi-agent system.
*   **Request Body:** `{"question": "string"}`
*   **Response:** Includes answer, confidence, sources, and verification status.

### `POST /upload`
Upload a PDF for immediate ingestion.
*   **Body:** Multipart form data (`file`)
*   **Effect:** Saves file to `data/documents/` and triggers re-indexing.

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**AeroMind is not a chatbot.** It is a controlled, explainable engineering tool.

