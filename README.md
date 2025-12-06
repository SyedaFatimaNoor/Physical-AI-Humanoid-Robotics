# README.md

## Physical AI & Humanoid Robotics Textbook

A **premium, AI‑native textbook** built with **Docusaurus** (static site) and a **FastAPI RAG backend**. All content is generated automatically via **Spec‑Kit Plus** (prompt history stored in `spec/spec.md`) and an LLM of your choice (Claude, ChatGPT, Gemini, etc.).

### Features
- **Spec‑Kit Plus‑driven content generation** – every chapter is produced by prompts recorded in `spec/spec.md`.
- **Retrieval‑Augmented Generation chatbot** – answer questions based on selected text.
- **Authentication** (Better Auth) – email/password signup/login.
- **Per‑chapter personalization** – user preferences stored in Neon Postgres.
- **On‑demand Urdu translation** – cached in Neon.
- **Premium dark UI** – custom CSS with gradients, micro‑animations, Inter font.
- **Vercel preview deployments** for both frontend and backend (GitHub Actions workflow).

### Repository Layout
```
physical-ai-robotics/
├─ .github/
│  └─ workflows/
│     └─ deploy.yml               # CI/CD for Vercel previews
├─ spec/
│  └─ spec.md                    # Prompt history for Spec‑Kit Plus
├─ textbook-frontend/
│  ├─ docusaurus.config.ts       # Docusaurus site config (dark theme, Inter font)
│  ├─ src/
│  │  ├─ components/
│  │  │  └─ ChatWidget.tsx       # Embedded RAG chatbot UI
│  │  ├─ css/
│  │  │  └─ custom.css           # Premium dark theme, gradients, animations
│  │  └─ theme/…                 # Layout overrides (optional)
│  └─ scripts/
│     └─ generate_content.py      # Spec‑Kit Plus content generation script
├─ rag-backend/
│  ├─ main.py                     # FastAPI entrypoint (Vercel Serverless)
│  ├─ rag.py                      # RAG core (Qdrant + OpenAI)
│  ├─ db.py                       # Neon Postgres helper (profiles, preferences)
│  ├─ requirements.txt            # Python dependencies
│  └─ scripts/
│     └─ ingest.py                # Ingest markdown into Qdrant & Neon
└─ repo_structure.md              # High‑level repo diagram (for reference)
```

### Quick Start (local development)
1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd physical-ai-robotics
   ```
2. **Frontend**
   ```bash
   cd textbook-frontend
   npm ci
   npm run start   # Docusaurus dev server at http://localhost:3000
   ```
3. **Backend**
   ```bash
   cd ../rag-backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload   # FastAPI dev server at http://localhost:8000
   ```
4. **Generate content** (once you have Spec‑Kit Plus installed and configured)
   ```bash
   cd ../textbook-frontend/scripts
   python generate_content.py
   ```
   This will populate `textbook-frontend/docs/` with markdown chapters.
5. **Ingest into vector store** (requires Qdrant & Neon credentials)
   ```bash
   cd ../../rag-backend/scripts
   python ingest.py
   ```

### Deployment (Vercel)
- **Frontend** – Vercel will build the Docusaurus site using `npm run build`.
- **Backend** – Vercel Serverless will run the FastAPI app (`main.py`).
- The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically creates preview URLs for every PR.

### Environment Variables

#### Backend Environment Variables
Create a `.env` file in `rag-backend/` directory:

```bash
LLM_PROVIDER=openrouter  # or 'gemini'
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_EMBED_MODEL=text-embedding-3-small
GEMINI_API_KEY=your_gemini_api_key  # if using Gemini
GEMINI_MODEL=gemini-1.5-flash
GEMINI_EMBED_MODEL=text-embedding-004
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DB_URL=your_neon_postgres_url
BETTER_AUTH_CLIENT_ID=your_better_auth_client_id
BETTER_AUTH_CLIENT_SECRET=your_better_auth_secret
```

#### Frontend Environment Variables
Create a `.env.local` file in `textbook-frontend/` directory:

**For Local Development:**
```bash
REACT_APP_API_URL=http://localhost:8003
```

**For Production (Vercel):**
- Leave `REACT_APP_API_URL` empty or unset to use relative paths
- The Vercel deployment will automatically route `/api/*` requests to the backend

#### Vercel Deployment
Set these environment variables in your Vercel project settings:
- All backend variables listed above
- `REACT_APP_API_URL` should be left empty (uses relative paths)

### Submission Checklist
- Public GitHub Repo Link
- Published book link (GitHub Pages/Vercel)
- Demo video (under 90 seconds)
- WhatsApp number

### License
MIT – feel free to adapt and extend for your own courses.

---
*Generated with Spec‑Kit Plus and ready for Vercel preview deployments.*
