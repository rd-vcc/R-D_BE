from sqlalchemy import text
from app.extensions import db

def login_user(username, password):
    sql = text("""
        SELECT 
            id,
            username,
            full_name,
            employee_code,
            role,
            password
        FROM users
        WHERE LOWER(username) = LOWER(:username)
    """)

    user = db.session.execute(
        sql,
        {"username": username}
    ).mappings().fetchone()

    if not user:
        return None
    if user["password"] != password:
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "employee_code": user["employee_code"],
        "role": user["role"],
    }
