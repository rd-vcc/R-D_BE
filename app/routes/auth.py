from flask import Blueprint, request, jsonify
from app.repositories.auth_repo import login_user

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"message": "Thiếu dữ liệu"}, 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Thiếu username hoặc password"}, 400

    user = login_user(username, password)

    if not user:
        return {"message": "Tên đăng nhập hoặc mật khẩu không đúng"}, 401
    return jsonify({
        "token": "fake-token-123",
        "user": user
    })
