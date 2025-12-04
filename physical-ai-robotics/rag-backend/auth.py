from .db import get_db_connection
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

def create_user(user: User):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users 
               (email, password_hash, full_name, gpu, ros_level, programming_level, preferred_language) 
               VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (user.email, hash_password(user.password), user.full_name, user.gpu, user.ros_level, user.programming_level, user.preferred_language)
        )
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def authenticate_user(email, password):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and user['password_hash'] == hash_password(password):
            return user
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None
