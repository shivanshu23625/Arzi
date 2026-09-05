# ARZI — Civic Legal Intelligence Platform

**Automating India's public law processes — RTI applications, legal notices, and statutory compliance.**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://arzi-rti-filedesk.up.railway.app/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/backend-Flask-black)](#tech-stack)
[![Database](https://img.shields.io/badge/database-Supabase%20%2F%20Postgres-3ecf8e)](#tech-stack)

🔗 **Live App:** [arzi-rti-filedesk.up.railway.app](https://arzi-rti-filedesk.up.railway.app/)
📦 **Repository:** [github.com/shivanshu23625/Arzi](https://github.com/shivanshu23625/Arzi)

---

## 📖 Overview

**ARZI** is a civic legal intelligence platform built to simplify and automate India's public law processes. It helps citizens draft, file, and track **Right to Information (RTI) applications**, generate **legal notices**, and stay on top of **statutory compliance** — without needing a legal background.

The platform combines rule-based legal templates with intelligent classification to route requests to the correct authority, generate properly formatted documents, and reduce the friction citizens face when exercising their legal rights.

---

## ✨ Features

- **RTI Application Drafting** — Generate legally compliant RTI applications tailored to the relevant Public Information Officer (PIO) / department.
- **Legal Notice Generation** — Create structured legal notices for common civic and consumer grievances.
- **Statutory Compliance Assistance** — Track and surface compliance requirements relevant to a user's request.
- **Document Export** — Produce polished, ready-to-file PDF documents.
- **Intelligent Classification** — ML-assisted routing/categorization of requests using `scikit-learn`.
- **Web Dashboard** — A frontend interface for creating, tracking, and managing filings.
- **Cloud-Native Deployment** — Ships with Docker, Procfile, and Railway/Supabase configuration for one-click deployment.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python), Gunicorn |
| Frontend | Node.js / npm-based SPA (`arzi-frontend`) |
| Database | PostgreSQL via Supabase (with `pgvector` support) |
| ML / NLP | scikit-learn |
| Document Generation | ReportLab (PDF generation) |
| Validation | Pydantic / Pydantic Settings |
| Testing | Pytest |
| Deployment | Docker, Railway, Procfile |

---

## 📁 Project Structure

```
Arzi/
├── api/                  # API layer / route handlers
├── arzi-frontend/        # Frontend web dashboard (Node/npm)
├── common/               # Shared utilities and helpers
├── config/               # App configuration
├── flask_backend/        # Core Flask application (app.py entrypoint)
├── scripts/              # Setup & database scripts (e.g. init_db.sql)
├── services/             # Business logic / service layer
├── tests/                # Automated test suite
├── .env.example          # Environment variable template
├── Dockerfile            # Container build definition
├── docker-compose.yml    # Local multi-service orchestration
├── Procfile              # Railway/Heroku-style process definition
├── requirements.txt      # Python dependencies
├── package.json          # NPM scripts for fullstack orchestration
├── seed_db.py            # Database seeding script
├── start.py              # Single-command fullstack launcher
└── DEPLOYMENT_GUIDE.md   # Detailed deployment instructions
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js & npm
- PostgreSQL database (a free [Supabase](https://supabase.com) project works well)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shivanshu23625/Arzi.git
   cd Arzi
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # then edit .env with your DATABASE_URL, SECRET_KEY, etc.
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd arzi-frontend
   npm install
   cd ..
   ```

5. **Initialize the database**
   Run `scripts/init_db.sql` against your PostgreSQL/Supabase instance, then seed it:
   ```bash
   python seed_db.py
   ```

### Running Locally

Start the full application (backend + frontend) with a single command:

```bash
npm start
# or
npm run dev
# or directly via Python
python start.py
```

Then open your browser to **http://localhost:5000**.

You can also run the backend and frontend independently:

```bash
npm run backend    # Flask backend only
npm run frontend   # Frontend dev server only
```

---

## 🧪 Testing

Run the automated test suite with either:

```bash
npm test
# or
pytest tests/test_flask_api.py
```

---

## ☁️ Deployment

ARZI is designed for zero-configuration deployment on **Railway** with a **Supabase** Postgres backend. Full step-by-step instructions — including required environment variables and Docker/Procfile setup — are documented in [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md).

**Quick summary:**

1. Push your code to GitHub.
2. Create a new Railway project → **Deploy from GitHub repo**.
3. Railway auto-detects the `Procfile` (`gunicorn flask_backend.app:app`) or `Dockerfile`.
4. Set the following environment variables in Railway:

   | Variable | Description |
   |---|---|
   | `PORT` | Web server port (Railway sets this automatically) |
   | `DATABASE_URL` | Supabase/PostgreSQL connection string |
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | A secure random string |

5. Connect Supabase by running `scripts/init_db.sql` in the Supabase SQL editor and adding your connection string as `DATABASE_URL`.

A live instance is available at: **https://arzi-rti-filedesk.up.railway.app/**

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please make sure tests pass (`pytest tests/test_flask_api.py`) before submitting a PR.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

Built to make Indian public law — RTI filings, legal notices, and statutory compliance — more accessible to everyday citizens.
