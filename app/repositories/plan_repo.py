from sqlalchemy import text
from app.extensions import db
def upsert_plan(project_id, date, content):
    sql = text("""
        INSERT INTO plan (project_id, date, content)
        VALUES (:project_id, :date, :content)
        ON DUPLICATE KEY UPDATE
            content = :content,
            updated_at = NOW();
    """)
    db.session.execute(sql, {
        "project_id": project_id,
        "date": date,
        "content": content
    })
    db.session.commit()





