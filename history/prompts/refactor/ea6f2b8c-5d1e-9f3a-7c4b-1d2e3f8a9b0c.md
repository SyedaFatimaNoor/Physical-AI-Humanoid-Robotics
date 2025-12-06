---
id: ea6f2b8c-5d1e-9f3a-7c4b-1d2e3f8a9b0c
title: Fix Backend Dependencies and Frontend Locale
stage: refactor
feature: Project Configuration
created_at: 2025-12-06T11:08:00+05:00
---

**PROMPT_TEXT**
```
1. Update rag-backend/requirements.txt to use standard versions that likely have pre-built wheels for Windows, avoiding local compilation requiring Rust.
   - Pydantic 2.x often needs Rust; if binary wheels fail, fallback to Pydantic 1.10.x or ensure a compatible environment. However, usually pydantic binary wheels exist for standard Python versions.
   - Asyncpg also usually has wheels.
   (The failure happened on Python 3.14? The log mentioned c:\users\lenovo\appdata\local\programs\python\python314 -- Python 3.14 is pre-alpha/experimental and likely has NO binary wheels. I should try to enforce a check or just assume I can't change the python version easily, so I must try to find pure python alternatives or ignore for now if I can't change the environment).
   Wait, the log says python314. That is very new.
   Process:
   - Downgrade dependencies or assume the user's environment is bleeding edge.
   - Actually, I can't change the user's installed python.
   - I will try to use `pydantic` < 2 if possible, or just standard versions and hope. But `pydantic-core` is Rust-based.
   - Alternative: Use `fastapi` < 0.100 which might use pydantic v1.
   
2. Update textbook-frontend/docusaurus.config.ts to comment out the 'ur' locale to fix the build error until translations are set up.
```

**RESPONSE_TEXT**
Acknowledged. I will relax the backend requirements to improve compatibility and temporarily disable the Urdu locale in the frontend configuration to unblock the build process.
