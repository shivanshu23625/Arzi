# 🚀 ARZI Platform — Complete Deployment & Startup Guide

This document provides step-by-step instructions to run the project locally with a **single command** or deploy it to the cloud using **Render** or **Vercel**.

---

## ⚡ 1. Single-Command Local Run

You can now start the entire ARZI engine, Notion sync worker, and web dashboard using **any** of the following single commands from the project root:

```bash
# Option A (Standard NPM)
npm start

# Option B (NPM Dev)
npm run dev

# Option C (Direct Python)
python start.py
```

Once started, open your browser to **[http://localhost:5000](http://localhost:5000)**.

---

## ☁️ 2. Deploying to Render (Recommended for Notion Track)

Render is the **ideal free hosting platform** for ARZI because it supports long-running background threads (such as the autonomous Notion poller).

### Step-by-Step Deployment:
1. Push your latest code to GitHub (**[https://github.com/shivanshu23625/Arzi](https://github.com/shivanshu23625/Arzi)**).
2. Go to **[https://render.com](https://render.com)** and sign in with GitHub.
3. Click **`New +`** $\rightarrow$ **`Web Service`**.
4. Select your **`shivanshu23625/Arzi`** repository.
5. Configure the service settings:
   - **Name**: `arzi-legal-engine`
   - **Language / Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_backend.app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`
6. *(Optional)* Add Environment Variables under **Advanced**:
   - `NOTION_API_KEY`: `secret_...`
   - `NOTION_CASES_DB_ID`: `...`
   - `NOTION_RUN_LOG_DB_ID`: `...`
7. Click **`Create Web Service`**.
8. Render will build and deploy your application. You will get a live public URL (e.g. `https://arzi-legal-engine.onrender.com`).

---

## ▲ 3. Deploying to Vercel

Vercel provides ultra-fast global CDN hosting for Python and Next.js applications using the included `vercel.json`.

### Step-by-Step Deployment:
1. Go to **[https://vercel.com](https://vercel.com)** and log in with GitHub.
2. Click **`Add New...`** $\rightarrow$ **`Project`**.
3. Import your **`shivanshu23625/Arzi`** repository.
4. Framework Preset: **`Other`** (Root Directory: `./`).
5. *(Optional)* Under **Environment Variables**, add:
   - `NOTION_API_KEY`
   - `NOTION_CASES_DB_ID`
   - `NOTION_RUN_LOG_DB_ID`
6. Click **`Deploy`**.
7. Vercel will automatically detect `vercel.json` and deploy the Python backend.

---

## 🔑 4. Environment Variables Reference

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `PORT` | Web server listening port | `5000` (Local) / `10000` (Render) |
| `NOTION_API_KEY` | Notion Internal Integration Token | `secret_...` |
| `NOTION_CASES_DB_ID` | Notion Cases Database ID | `32-character hex ID` |
| `NOTION_RUN_LOG_DB_ID` | Notion Run Log Database ID | `32-character hex ID` |
| `NOTION_PARENT_PAGE_ID` | Notion Parent Page ID for auto-setup | `32-character hex ID` |

---

## 🧪 5. Testing the Deployment

Run the automated test suite locally or in CI/CD:
```bash
npm test
# OR
pytest tests/test_notion_sync.py tests/test_flask_api.py
```
