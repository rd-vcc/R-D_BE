from sqlalchemy import text
from app.extensions import db

# GET LIST PROJECT
def get_project(role, employee_code=None, monday=None, sunday=None):
    sql = """
        SELECT
            p.id,
            p.employee_code,
            u.full_name,
            p.category,
            p.description,
            p.status,
            pl.id AS plan_id,
            pl.content AS plan_content,
            pl.date AS plan_date
        FROM project p
        JOIN users u ON p.employee_code = u.employee_code
        LEFT JOIN plan pl
            ON pl.project_id = p.id
            AND pl.date BETWEEN :monday AND :sunday
    """
    params = {}
    conditions = []

    if monday and sunday:
        conditions.append("""
            (pl.date BETWEEN :monday AND :sunday OR pl.id IS NULL)
        """)
        params["monday"] = monday
        params["sunday"] = sunday

    if role != "admin":
        conditions.append("p.employee_code = :employee_code")
        params["employee_code"] = employee_code

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY p.id ASC"

    result = db.session.execute(text(sql), params)
    return [dict(r._mapping) for r in result]
# GET PROJECT BY ID
def get_project_by_id(project_id):
    sql = text("""
        SELECT
            p.*,
            u.full_name
        FROM project p
        JOIN users u ON p.employee_code = u.employee_code
        WHERE p.id = :id
    """)
    result = db.session.execute(sql, {"id": project_id}).fetchone()
    return dict(result._mapping) if result else None

# CREATE PROJECT
def create_project(employee_code, category, description, status):
    sql = text("""
        INSERT INTO project (employee_code, category, description, status)
        VALUES (:employee_code, :category, :description, :status)
    """)
    result = db.session.execute(sql, {
        "employee_code": employee_code,
        "category": category,
        "description": description,
        "status": status
    })
    db.session.commit()
    return result.lastrowid

# UPDATE PROJECT
def update_project(
    project_id,
    category,
    description,
    status,
    role,
    employee_code=None
):
    try:
        if role == "admin":
            sql = text("""
                UPDATE project
                SET
                    employee_code = COALESCE(:employee_code, employee_code),
                    category = :category,
                    description = :description,
                    status = :status
                WHERE id = :id
            """)
            params = {
                "id": project_id,
                "employee_code": employee_code,
                "category": category,
                "description": description,
                "status": status
            }
        else:
            sql = text("""
                UPDATE project
                SET
                    category = :category,
                    description = :description,
                    status = :status
                WHERE id = :id
                  AND employee_code = :employee_code
            """)
            params = {
                "id": project_id,
                "employee_code": employee_code,
                "category": category,
                "description": description,
                "status": status
            }

        result = db.session.execute(sql, params)
        db.session.commit()

        return result.rowcount > 0

    except Exception as e:
        db.session.rollback()
        raise e

# DELETE PROJECT
def delete_project(project_id):
    db.session.execute(
        text("DELETE FROM plan WHERE project_id = :id"),
        {"id": project_id}
    )
    result = db.session.execute(
        text("DELETE FROM project WHERE id = :id"),
        {"id": project_id}
    )

    db.session.commit()
    return result.rowcount > 0




