from db import _get_pool
from pydantic import BaseModel
import hashlib

class User(BaseModel):
    email: str
    password: str
    full_name: str
    gpu: str
    ros_level: str
    programming_level: str
    preferred_language: str = "en"

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

async def create_user(user: User):
    pool = await _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                gpu TEXT,
                ros_level TEXT,
                programming_level TEXT,
                preferred_language TEXT DEFAULT 'en'
            );
            """
        )
        row = await conn.fetchrow(
            """INSERT INTO users (email, password_hash, full_name, gpu, ros_level, programming_level, preferred_language)
               VALUES ($1, $2, $3, $4, $5, $6, $7)
               ON CONFLICT (email) DO UPDATE SET
                 password_hash = EXCLUDED.password_hash,
                 full_name = EXCLUDED.full_name,
                 gpu = EXCLUDED.gpu,
                 ros_level = EXCLUDED.ros_level,
                 programming_level = EXCLUDED.programming_level,
                 preferred_language = EXCLUDED.preferred_language
               RETURNING id;""",
            user.email,
            hash_password(user.password),
            user.full_name,
            user.gpu,
            user.ros_level,
            user.programming_level,
            user.preferred_language,
        )
    await pool.close()
    return row['id'] if row else None

async def authenticate_user(email, password):
    pool = await _get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1;", email)
    await pool.close()

    if user and user['password_hash'] == hash_password(password):
        return dict(user)
    return None
