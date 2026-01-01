# Deployment Guide

## Backend Deployment (Render)

This project is configured for deployment on Render as a Web Service.

1.  **Connect to Render**:
    *   Go to [dashboard.render.com](https://dashboard.render.com/).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.

2.  **Configuration**:
    *   **Name**: `github-research-agent` (or your preferred name)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

    *Alternatively, you can use the `render.yaml` by creating a "Blueprint" instance if you prefer Infrastructure as Code.*

3.  **Environment Variables**:
    *   Add your `OPENAI_API_KEY` or `GROQ_API_KEY`, `GITHUB_TOKEN`, etc., in the "Environment" tab.

## Frontend Deployment (Vercel)

The frontend is a React app that can be deployed on Vercel. It also includes a serverless function entry point for the backend in `api/index.py` if you prefer a monorepo deployment.

1.  **Connect to Vercel**:
    *   Go to [vercel.com](https://vercel.com/dashboard).
    *   Click **Add New...** -> **Project**.
    *   Import your GitHub repository.

2.  **Configuration**:
    *   **Framework Preset**: `Vite`
    *   **Root Directory**: `frontend` (Important!)
    *   **Build Command**: `npm run build`
    *   **Output Directory**: `dist`
    *   **Install Command**: `npm install`

3.  **Environment Variables**:
    *   Add `VITE_API_URL` pointing to your Render backend URL (e.g., `https://github-research-agent.onrender.com`).
    
    *Note: If you are using the Vercel serverless functions for the backend (via `api/index.py`), you might not need the external URL, but the Render deployment is recommended for long-running agent tasks.*
