# Repository Structure

```
physical-ai-robotics/
├─ .github/
│  └─ workflows/
│     └─ deploy.yml          # CI/CD for Vercel preview & production
├─ spec/
│  └─ spec.md                # Spec‑Kit Plus prompt history & configuration
├─ textbook-frontend/
│  ├─ docusaurus.config.ts   # Docusaurus site configuration (Vercel static host)
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ ChatWidget.tsx    # Embedded RAG chatbot UI
│  │  │  ├─ AuthProvider.tsx # Better Auth integration
│  │  │  ├─ PersonalizeButton.tsx
│  │  │  └─ TranslateButton.tsx (already present)
│  │  └─ theme/
│  │     └─ Layout/index.js   # Layout overrides for premium dark theme
│  └─ scripts/
│     └─ generate_content.py # Spec‑Kit Plus + Claude/ChatGPT content generator
├─ rag-backend/
│  ├─ main.py                # FastAPI entry point (Vercel Serverless)
│  ├─ rag.py                 # Core RAG logic (vector store, LLM calls)
│  ├─ db.py                  # Neon Postgres helper
│  ├─ requirements.txt       # Python dependencies
│  └─ scripts/
│     └─ ingest.py           # Markdown ingestion → Qdrant + Neon metadata
└─ README.md                 # Project overview & deployment instructions
```

All chapters are generated automatically by `scripts/generate_content.py` which talks to **Spec‑Kit Plus** and the chosen LLM (Claude, ChatGPT, Gemini, etc.). The repo is ready for Vercel preview builds for both the static Docusaurus site and the FastAPI backend.
