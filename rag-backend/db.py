# db.py
"""Neon Postgres helper utilities.

Provides a simple async wrapper around asyncpg for storing user profiles and preferences.
The Better Auth SDK will issue a JWT containing the user's email; we can use that as the primary key.
"""
import os
import asyncpg
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
DATABASE_URL = os.getenv("NEON_DB_URL")

async def _get_pool():
    return await asyncpg.create_pool(DATABASE_URL)

async def store_user_profile(email: str, profile: Dict[str, Any]):
    """Insert or update a user profile.
    `profile` is a dict of arbitrary fields (e.g., hardware background).
    """
    pool = await _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO user_profiles (email, data)
            VALUES ($1, $2::jsonb)
            ON CONFLICT (email) DO UPDATE SET data = EXCLUDED.data;
            """,
            email,
            profile,
        )
    await pool.close()

async def get_user_preferences(email: str) -> Dict[str, Any]:
    """Retrieve stored preferences for a user. Returns empty dict if none."""
    pool = await _get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT data FROM user_profiles WHERE email = $1;",
            email,
        )
    await pool.close()
    return row["data"] if row else {}
