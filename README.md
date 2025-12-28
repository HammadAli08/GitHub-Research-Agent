# GitHub Intelligence & Research Tool 🚀

A high-performance, multi-agent system designed to perform deep technical research on GitHub repositories. This tool automates the process of auditing, analyzing, and "interrogating" any public repository on GitHub.

Built with a state-of-the-art AI stack featuring **LangGraph**, **Groq (gpt-oss-120b)**, and **FastAPI**.

## 🌟 Key Features

- **Multi-Agent Research Pipeline**: Uses specialized AI agents to analyze code structure, technical debt, maintenance health, and community trends in parallel.
- **Smart Discovery**: Search for repositories by keyword, direct GitHub URL, or `owner/repo` patterns.
- **Agentic Interrogation Chat**: A dedicated "ReAct" agent that has access to both a static research snapshot and **live GitHub tools** to fetch original, real-time data during conversations.
- **Deep Technical Synthesis**: Generates a production-grade report covering risk scores, architectural patterns, and maintenance quality.
- **Premium UI**: A sleek, minimal "Intelligence Dashboard" aesthetic built with React, Tailwind, and Lucide.

## 🛠️ Tech Stack

- **AI Orchestration**: LangGraph (Directed Acyclic Graphs for Agentic logic)
- **LLM**: Groq (utilizing the `openai/gpt-oss-120b` model for deep reasoning)
- **Backend**: FastAPI, LangChain, HTTPX
- **Frontend**: React (Vite, TypeScript, Tailwind CSS, remark-gfm)
- **API Integration**: GitHub REST API (optimized for Fine-grained PATs)

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+ & npm

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_fine_grained_access_token
```

### 3. Quick Install (Root Directory)
I have provided a root-level script to install everything at once:
```bash
npm run install:all
```

### 4. Running the Application
You will need two terminal windows running:

**Terminal 1 (Backend):**
```bash
python main.py
```

**Terminal 2 (Frontend):**
```bash
npm run dev:frontend
```
*Access the dashboard at `http://localhost:5173`.*

## 🧠 How the Research Graph Works

The system orchestrates research through a structured **LangGraph** workflow:

1.  **Code Analysis**: Maps the file tree and summarizes core logic files (README, main, app.py, etc.).
2.  **Issue Intelligence**: Fetches and evaluates the 15 most recent issues and PRs to gauge community demand and response time.
3.  **Trend/Risk Node**: Analyzes commit frequency, star velocity, and licensing risks.
4.  **Community Health**: Checks for documentation standards (Contributing, Code of Conduct, etc.).
5.  **Senior Synthesis**: A final agent combines all research into a structured JSON report.

## 💬 Live Interrogation
The "Interrogation" chat isn't just a simple bot. It is a **Tool-Calling Agent**. If you ask it for something not in the initial report (e.g., *"What is written in the package.json file right now?"*), it will call the live GitHub API to fetch the **original results** and incorporate them into the answer.

---
*Created as part of a high-performance GitHub Intelligence project.*
