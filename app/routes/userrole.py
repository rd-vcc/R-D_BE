from flask import Blueprint, request, jsonify
from app.repositories.userrole_repo import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    change_password
)

user = Blueprint("user", __name__, url_prefix="/users")

# GET ALL USERS
@user.route("", methods=["GET"])
def list_users():
    data = get_all_users()
    return jsonify(data)

# GET USER BY ID
@user.route("/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user_data = get_user_by_id(user_id)

    if not user_data:
        return {"message": "User không tồn tại"}, 404

    return jsonify(user_data)

# CREATE USER
@user.route("", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data:
        return {"message": "Thiếu dữ liệu"}, 400

    required_fields = ["employee_code", "username", "password"]
    for field in required_fields:
        if not data.get(field):
            return {"message": f"Thiếu {field}"}, 400
    result = create_user(data)
    if isinstance(result, tuple):
        return result
    return jsonify(result), 201
# UPDATE USER
@user.route("/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.get_json()
    if not data:
        return {"message": "Thiếu dữ liệu"}, 400

    updated = update_user(user_id, data)
    if not updated:
        return {"message": "User không tồn tại"}, 404

    return {"message": "Cập nhật user thành công"}

# DELETE USER
@user.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    deleted = delete_user(user_id)
    if not deleted:
        return {"message": "User không tồn tại"}, 404

    return {"message": "Xoá user thành công"}
# CHANGE PASS
@user.route("/change-password", methods=["POST"])
def change_password_api():
    data = request.get_json()

    user_id = data.get("user_id")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not all([user_id, old_password, new_password]):
        return jsonify(
            success=False,
            message="Thiếu dữ liệu"
        ), 400

    success, message = change_password(
        user_id=user_id,
        old_password=old_password,
        new_password=new_password
    )

    if not success:
        return jsonify(
            success=False,
            message=message
        ), 400

    return jsonify(
        success=True,
        message=message
    )


