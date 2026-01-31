from flask import Blueprint, request, jsonify
from app.repositories.project_repo import (
    get_project,
    create_project,
    update_project as update_project_repo,
    get_project_by_id,
    delete_project
)

project = Blueprint("project", __name__, url_prefix="/project")
# GET LIST PROJECT
@project.route("", methods=["GET"])
def list_project():
    role = request.args.get("role", "user")
    employee_code = request.args.get("employee_code")
    monday = request.args.get("monday")
    sunday = request.args.get("sunday")

    if role != "admin" and not employee_code:
        return {"message": "Thiếu employee_code"}, 400

    data = get_project(
        role=role,
        employee_code=employee_code,
        monday=monday,
        sunday=sunday
    )
    return jsonify(data)
# CREATE PROJECT
@project.route("", methods=["POST"])
def add_project():
    data = request.get_json()

    if not data:
        return {"message": "Thiếu dữ liệu"}, 400

    employee_code = data.get("employee_code")
    if not employee_code:
        return {"message": "Thiếu employee_code"}, 400

    project_id = create_project(
        employee_code=employee_code,
        category=data.get("category"),
        description=data.get("description"),
        status=data.get("status")
    )

    return {
        "message": "Tạo project thành công",
        "id": project_id
    }, 201

# GET PROJECT DETAIL

@project.route("/<int:project_id>", methods=["GET"])
def get_project_detail(project_id):
    project_data = get_project_by_id(project_id)

    if not project_data:
        return {"message": "Không tìm thấy project"}, 404

    return jsonify(project_data)

# UPDATE PROJECT
@project.route("/<int:project_id>", methods=["PUT"])
def edit_project(project_id):
    data = request.get_json()
    if not data:
        return {"message": "Thiếu dữ liệu"}, 400

    role = data.get("role", "user")
    employee_code = data.get("employee_code")

    # user bắt buộc có employee_code
    if role != "admin" and not employee_code:
        return {"message": "Thiếu employee_code"}, 400

    updated = update_project_repo(
        project_id=project_id,
        category=data.get("category"),
        description=data.get("description"),
        status=data.get("status"),
        role=role,
        employee_code=employee_code
    )

    if not updated:
        return {"message": "Không có quyền hoặc không tìm thấy project"}, 403

    return {"message": "Cập nhật thành công"}, 200

# DELETE PROJECT
@project.route("/<int:project_id>", methods=["DELETE"])
def remove_project(project_id):
    deleted = delete_project(project_id)

    if not deleted:
        return {"message": "Không tìm thấy project"}, 404

    return {"message": "Đã xoá"}, 200
