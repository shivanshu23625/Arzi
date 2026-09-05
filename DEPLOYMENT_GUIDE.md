# 🚀 ARZI Platform — Complete Deployment & Startup Guide

This document provides step-by-step instructions to run the project locally with a **single command** or deploy it to the cloud using **Railway** with **Supabase**.

---

## ⚡ 1. Single-Command Local Run

You can start the ARZI engine and web dashboard using **any** of the following single commands from the project root:

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

## 🚂 2. Deploying to Railway

Railway provides seamless container and Procfile hosting with automatic SSL, custom domains, and zero-configuration environment variables.

### Step-by-Step Deployment:
1. Push your latest code to GitHub (**[https://github.com/shivanshu23625/Arzi](https://github.com/shivanshu23625/Arzi)**).
2. Go to **[https://railway.app](https://railway.app)** and log in.
3. Click **`New Project`** $\rightarrow$ **`Deploy from GitHub repo`**.
4. Select your **`shivanshu23625/Arzi`** repository.
5. Railway will automatically detect the **`Procfile`** / **`Dockerfile`**:
   - Start Command: `gunicorn flask_backend.app:app` (via Procfile) or custom command.
6. Under **Variables** in your Railway dashboard, configure:
   - `PORT`: `5000` (or leave Railway to assign `$PORT` automatically)
   - `DATABASE_URL`: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `[YOUR-SECRET-KEY]`
7. Railway will build and deploy your container with a public HTTPS URL (e.g., `https://arzi-production.up.railway.app`).

---

## 🗄️ 3. Connecting Supabase Database

ARZI uses PostgreSQL (with pgvector support) hosted on **Supabase**:
1. Create a project at **[https://supabase.com](https://supabase.com)**.
2. In the Supabase SQL Editor, run `scripts/init_db.sql` to initialize database tables and the vector extension.
3. Copy your database connection string from **Project Settings $\rightarrow$ Database** and add it as `DATABASE_URL` in Railway.

---

## 🔑 4. Environment Variables Reference

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `PORT` | Web server listening port | `5000` (Assigned automatically by Railway) |
| `DATABASE_URL` | Supabase / PostgreSQL URI | `postgresql://postgres:...@db...supabase.co:5432/postgres` |
| `FLASK_ENV` | Application environment | `production` |
| `SECRET_KEY` | Secret session key | Secure random string |

---

## 🧪 5. Testing the Deployment

Run the automated test suite locally or in CI/CD:
```bash
npm test
# OR
pytest tests/test_flask_api.py
```
