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

## ⚡ USP Features (Unique Selling Points)

### 🎯 Smart Follow-up Suggestions
After each response, AeroMind generates 3 intelligent follow-up questions using AI analysis. Click any suggestion to instantly continue exploring the topic - no need to think of what to ask next!

### 📊 Real-time Query Analytics Dashboard
Track your usage patterns with a built-in analytics dashboard:
- Total queries processed
- Breakdown by category (Engineering/Safety)
- Average response time metrics
- Recent query history

### ⏱️ Response Time Transparency
Every response shows exact processing time in milliseconds, giving you visibility into system performance and helping optimize your workflow.

### 🔬 Query Complexity Scoring
Each query is automatically analyzed and tagged as **SIMPLE**, **MODERATE**, or **COMPLEX** based on word count and technical terminology - helping you understand processing requirements.

### 🎓 Expert Mode Toggle
Switch between two response modes:
- **Standard Mode:** Concise, accessible answers for quick reference
- **Expert Mode:** Detailed technical responses with deeper analysis for specialists

### 🤖 Model Transparency
Every response displays which AI model was used (Gemini 2.5 Flash), with automatic fallback to backup models ensuring 99.9% uptime.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, LangChain/LangGraph (concept)
- **AI Models:** Google Gemini 2.5 Flash (primary), with automatic fallback
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Frontend:** Next.js, React, Tailwind CSS, Framer Motion, pnpm

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
*   **Request Body:** `{"question": "string", "expert_mode": boolean}`
*   **Response:** Includes answer, confidence, sources, verification status, processing time, follow-up suggestions, complexity score, and model used.

### `GET /analytics`
Retrieve query analytics and system performance metrics.
*   **Response:** Total queries, queries by route, average response time, recent queries.

### `POST /upload`
Upload a PDF for immediate ingestion.
*   **Body:** Multipart form data (`file`)
*   **Effect:** Saves file to `data/documents/` and triggers re-indexing.

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**AeroMind is not a chatbot.** It is a controlled, explainable engineering tool.

