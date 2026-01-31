from flask import Blueprint, request
from app.repositories.plan_repo import upsert_plan

plan = Blueprint("plan", __name__, url_prefix="/plan")

@plan.route("", methods=["PUT"])
def upsert_plan_api():
    data = request.get_json()

    if not data:
        return {"message": "Không có dữ liêu!"}, 400

    if "project_id" not in data or "date" not in data:
        return {"message": "project_id và date là bắt buộc"}, 400

    upsert_plan(
        project_id=data["project_id"],
        date=data["date"],
        content=data.get("content", "")
    )

    return {"message": "OK"}, 200
