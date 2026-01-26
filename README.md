# 🧪 AI Cosmetic Formulation Agent System

> **A production-ready multi-agent system for automating cosmetic R&D, from concept to lab-ready formula.**

This project implements a sophisticated **agentic AI workflow** that acts as a virtual laboratory assistant. Unlike simple chatbots, it coordinates specialized agents to conduct live deep research, synthesize scientific evidence, construct detailed formulations, and assess stability risks—all transparently and referenced.

---

## 🚀 Key Features

- **⚡ Live Scientific Deep Search**: Does not rely on static training data. Uses `SerpAPI` to fetch real-time papers, supplier sheets, and technical articles.
- **🤖 Multi-Agent Architecture**:
  - **Orchestrator**: Manages workflow state and agent transitions.
  - **DeepSearch Agent**: Generates queries, deduplicates findings, and verifies evidence.
  - **Formulation Agent**: Acts as the senior chemist, calculating percentages and phases (A/B/C) based on evidence.
  - **Stability Agent**: Predicts risks (pH drift, oxidation, separation) and suggests mitigation strategies.
  - **Documentation Agent**: Compiles professional technical reports.
- **🩺 Safety & Compliance**: Auto-sanitizes inputs and provides risk assessments for every formula.
- **🏢 Robust & Typed**: Built with `Pydantic` for strict data validation and schema enforcement.
- **🖥️ Modern UI**: Includes a `Streamlit` dashboard for interactive testing and report generation.

---

## 🛠️ Tech Stack

- **language**: Python 3.10+
- **LLM Engine**: Compatible with OpenAI-API compliant endpoints (configured for **Llama 3.1 70B via hosted VLLM**).
- **Search Engine**: Google Search via **SerpAPI**.
- **Frameworks**:
  - `Streamlit` (Web Interface)
  - `Pydantic` (Data Validation)
  - `httpx` & `asyncio` (Async Networking)
- **Package Manager**: `uv` (recommended) or `pip`

---

## 📂 Project Structure

```bash
cosmetic-formulation-agent/
├── src/
│   ├── agents/           # Logic for individual agents
│   │   ├── orchestrator.py
│   │   ├── deep_search.py
│   │   ├── formulation.py
│   │   └── stability.py
│   ├── models/           # Pydantic schemas (Domain & State)
│   ├── tools/            # External tool integrations (SerpAPI)
│   └── utils/            # LLM Client wrapper
├── app.py                # Streamlit Web Dashboard
├── main.py               # CLI Entrypoint
├── requirements.txt      # Dependency list
└── .env                  # Environment secrets
```

---

## ⚙️ Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/bmejri988-spec/cosmetic-formulation-agent.git
    cd cosmetic-formulation-agent
    ```

2.  **Install dependencies** (using `uv` is recommended for speed):

    ```bash
    uv pip install -r requirements.txt
    # OR
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:

    ```ini
    # LLM Configuration (Example: Hosted VLLM)
    LLM_API_KEY=your_llm_key_here
    LLM_API_BASE=https://tokenfactory.esprit.tn/api  # or https://api.openai.com/v1

    # Search Configuration
    SERPAPI_API_KEY=your_serpapi_key_here
    ```

---

## 🏃‍♂️ Usage

### Option 1: Web Interface (Recommended)

Launch the interactive dashboard to visualize the research, formula table, and risk analysis in real-time.

```bash
streamlit run app.py
```

### Option 2: Command Line Interface

Run a full headless simulation in your terminal.

```bash
python main.py
```

_(or `uv run main.py`)_

---

## 🧠 How It Works

1.  **Brief Ingestion**: The user inputs a request (e.g., _"Develop a rich barrier repair cream for dry skin using ceramides"_).
2.  **Product Brief Parsing**: The LLM structures this into a strict JSON brief (Target Audience, pH target, Texture, etc.).
3.  **Deep Search**: The system generates specific search queries (e.g., _"ceramide NP solubility,"_ _"natural emulsifiers for O/W creams"_) and fetches live results via SerpAPI.
4.  **Evidence Collection**: It filters and stores unique, relevant snippets as "Evidence".
5.  **Formulation Synthesis**: The Formulation Agent synthesizes this evidence to create a balanced formula (Phase A, B, C) ensuring it adds up to 100%.
6.  **Risk Assessment**: The Stability Agent reviews the ingredients (e.g., Vitamin C + Water) to flag oxidation or stability risks.
7.  **Reporting**: A final Markdown report is generated with citations.

---

## 📝 Example Output

**Input:** "Develop a night cream for sensitive skin with retinol alternatives."

**System Output:**

- **Product:** Bakuchiol Restorative Night Cream
- **Key Ingredients:** Bakuchiol (1%), Squalane (5%), Oat Kernel Extract.
- **Justification:** "Bakuchiol selected as a non-irritating retinol alternative referenced in [Study X]; Squalane chosen for biomimetic barrier support."
- **Risk:** "Bakuchiol can degrade in UV; formulation intended for night use and opaque packaging recommended."

---

## 🤝 Contributing

Contributions are welcome! Please submit a Pull Request or open an Issue for bug reports.

## 📄 License

MIT License.
