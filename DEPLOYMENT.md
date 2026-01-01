# Deployment Guide

## Backend Deployment (Render)

This project is configured for deployment on Render as a Web Service.

### 1. Backend: Deploy to Render
1. Create a New Web Service on [Render](https://dashboard.render.com/).
2. Link your GitHub repository.
3. Render will detect `render.yaml`. Use these settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
4. Add Environment Variables:
   - `GITHUB_TOKEN`: Your Personal Access Token.
   - `GROQ_API_KEY`: Your Groq API Key.

### 2. Frontend: Deploy to Vercel
1. Create a New Project on [Vercel](https://vercel.com/).
2. Link your GitHub repository.
3. Vercel will detect `vercel.json`. It is configured to **proxy all `/api` requests to your Render URL**.
4. Important: If you change your Render URL, update it in `vercel.json`.

---

## 🛠 Local Development
1. **Install Dependencies**: `npm run install:all`
2. **Setup Secrets**: Create a `.env` in the root (see `.env.example`).
3. **Run Backend**: `npm run dev:backend`
4. **Run Frontend**: `npm run dev:frontend`

The frontend is configured to hit `http://localhost:10000` via Vite proxy during development, and the Render URL in production via Vercel rewrites.
