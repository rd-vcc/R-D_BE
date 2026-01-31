from sqlalchemy import text
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
def get_all_users():
    sql = text("""
        SELECT id, employee_code, username, full_name, role
        FROM users
        ORDER BY id
    """)
    result = db.session.execute(sql).mappings().all()
    users_list = [dict(row) for row in result]
    return users_list

def get_user_by_id(user_id):
    sql = text("""
        SELECT id, employee_code, username, full_name
        FROM users
        WHERE id = :id
    """)
    result = db.session.execute(sql, {"id": user_id}).mappings().fetchone()
    if not result:
        return None

    return dict(result)
def create_user(data):
    try:
        sql = text("""
            INSERT INTO users (employee_code, username, password, full_name, role)
            VALUES (:employee_code, :username, :password, :full_name, :role)
        """)

        result = db.session.execute(sql, {
            "employee_code": data["employee_code"],
            "username": data["username"],
            "password": data["password"],
            "full_name": data.get("full_name", ""),
            "role": data.get("role", "user"),
        })

        db.session.commit()

        new_id = result.lastrowid
        return {"id": new_id, "message": "Tạo user thành công"}

    except IntegrityError:
        db.session.rollback()
        return {"message": "Employee code hoặc username đã tồn tại"}, 400

    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500
def update_user(user_id, data):
    fields = []
    params = {"id": user_id}

    if "employee_code" in data:
        fields.append("employee_code = :employee_code")
        params["employee_code"] = data["employee_code"]

    if "full_name" in data:
        fields.append("full_name = :full_name")
        params["full_name"] = data["full_name"]

    if "username" in data:
        fields.append("username = :username")
        params["username"] = data["username"]

    if "role" in data:
        fields.append("role = :role")
        params["role"] = data["role"]

    if "password" in data:
        fields.append("password = :password")
        params["password"] = data["password"]

    if not fields:
        return False

    sql = f"""
        UPDATE users
        SET {', '.join(fields)}
        WHERE id = :id
    """

    result = db.session.execute(text(sql), params)
    db.session.commit()

    return result.rowcount > 0
def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id = :id")
    result = db.session.execute(sql, {"id": user_id})
    db.session.commit()

    return result.rowcount > 0

def change_password(user_id, old_password, new_password):
    sql = text("""
        SELECT password
        FROM users
        WHERE id = :id
    """)
    user = db.session.execute(sql, {"id": user_id}).fetchone()

    if not user:
        return False, "User không tồn tại"
    if user.password != old_password:
        return False, "Mật khẩu cũ không đúng"

    sql = text("""
        UPDATE users
        SET password = :password
        WHERE id = :id
    """)

    db.session.execute(sql, {
        "id": user_id,
        "password": new_password
    })
    db.session.commit()

    return True, "Đổi mật khẩu thành công"


