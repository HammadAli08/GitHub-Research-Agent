# GitHub Research Agent 🚀

A multi-agent system designed to perform deep technical research on GitHub repositories. Powered by **LangGraph**, **Groq (Llama 3.1)**, and the **GitHub REST API**.

## Features
- **Code Analysis**: Deep dive into repository structure and core file purposes.
- **Issue & PR Intelligence**: Analyze maintenance health and community demand.
- **Trend & Risk Assessment**: Evaluate activity patterns and potential risks.
- **Community Health**: Assessment of documentation, licenses, and ecosystem health.
- **Interactive Search**: Discover repositories and initiate research with a single click.
- **Context-Aware Chat**: Interrogate the research report with an AI assistant.

## Tech Stack
- **Frontend**: React (Vite, TypeScript, Tailwind CSS, Lucide Icons)
- **Backend**: FastAPI, LangGraph, LangChain, Groq LLM
- **API**: GitHub REST API (Fine-grained PAT supported)

## Setup

### 1. Requirements
- Python 3.10+
- Node.js & npm

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key
GITHUB_TOKEN=your_fine_grained_pat
```

### 3. Backend Installation
```bash
pip install -r requirements.txt
python main.py
```

### 4. Frontend Installation
```bash
cd frontend
npm install
npm run dev
```

## How it works
The system uses a directed graph (LangGraph) to sequence research tasks:
1. **Code Analysis**: Scans the file tree and summarizes key files.
2. **Intelligence**: Fetches and evaluates recent issues and PRs.
3. **Trends**: Checks commit history and stars.
4. **Community**: Evaluates health metrics and languages.
5. **Synthesis**: A Senior AI Systems Engineer agent compiles all data into a JSON report.
