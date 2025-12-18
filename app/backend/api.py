from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Optional

from .crud.db import SessionLocal, engine, Base
from .crud import crud as crud_mod
from . import schemas
from .models import models


app = FastAPI(title="MSSQL Database Viewer API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    # создать таблицы, если их ещё нет
    Base.metadata.create_all(bind=engine)


# --- Проекты ---
@app.post("/projects/", response_model=schemas.ProjectRead)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Создать проект"""
    proj = crud_mod.create_project(db, data.dict())
    return proj


@app.get("/projects/", response_model=List[schemas.ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Фильтр по имени проекта (подстрока)"),
    min_budget: Optional[float] = Query(None, description="Минимум бюджета"),
    max_budget: Optional[float] = Query(None, description="Максимум бюджета"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    sort_by: Optional[str] = Query(None, description="Сортировать по полю (name,budget,start_date)"),
    sort_dir: Optional[str] = Query("asc", description="Направление сортировки: asc или desc"),
    limit: Optional[int] = Query(100, ge=1),
    offset: Optional[int] = Query(0, ge=0),
):
    """Список проектов с фильтрацией и сортировкой"""
    q = db.query(models.Project)
    if name:
        q = q.filter(models.Project.name.ilike(f"%{name}%"))
    if min_budget is not None:
        q = q.filter(models.Project.budget >= min_budget)
    if max_budget is not None:
        q = q.filter(models.Project.budget <= max_budget)
    if is_active is not None:
        q = q.filter(models.Project.is_active == is_active)
    if sort_by:
        col = getattr(models.Project, sort_by, None)
        if col is not None:
            if sort_dir == "desc":
                q = q.order_by(col.desc())
            else:
                q = q.order_by(col.asc())
    q = q.offset(offset).limit(limit)
    return q.all()


@app.get("/projects/aggregate")
def projects_aggregate(db: Session = Depends(get_db)):
    """Простейшие агрегаты по проектам: count, sum бюджета"""
    total = db.query(func.count(models.Project.id)).scalar()
    sum_budget = db.query(func.sum(models.Project.budget)).scalar()
    return {"count": total or 0, "sum_budget": float(sum_budget or 0)}


@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    proj = crud_mod.get_project(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@app.put("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    proj = crud_mod.update_project(db, project_id, data.dict(exclude_unset=True))
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    ok = crud_mod.delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return JSONResponse({"ok": True})


# --- Задачи ---
@app.post("/tasks/", response_model=schemas.TaskRead)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Создать задачу"""
    return crud_mod.create_task(db, data.dict())


@app.get("/tasks/", response_model=List[schemas.TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("asc"),
    limit: Optional[int] = Query(100, ge=1),
    offset: Optional[int] = Query(0, ge=0),
):
    """Список задач с фильтрами и сортировкой"""
    q = db.query(models.Task)
    if project_id is not None:
        q = q.filter(models.Task.project_id == project_id)
    if status:
        q = q.filter(models.Task.status == status)
    if priority:
        q = q.filter(models.Task.priority == priority)
    if sort_by:
        col = getattr(models.Task, sort_by, None)
        if col is not None:
            q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())
    q = q.offset(offset).limit(limit)
    return q.all()


@app.get("/tasks/aggregate")
def tasks_aggregate(db: Session = Depends(get_db)):
    """Агрегаты по задачам: count, среднее время"""
    total = db.query(func.count(models.Task.id)).scalar()
    avg_time = db.query(func.avg(models.Task.time_estimation)).scalar()
    return {"count": total or 0, "avg_time": float(avg_time or 0)}


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    t = crud_mod.get_task(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    t = crud_mod.update_task(db, task_id, data.dict(exclude_unset=True))
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    ok = crud_mod.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse({"ok": True})


# --- Комментарии ---
@app.post("/comments/", response_model=schemas.CommentRead)
def create_comment(data: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud_mod.create_comment(db, data.dict())


@app.get("/comments/", response_model=List[schemas.CommentRead])
def list_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()


@app.get("/comments/{comment_id}", response_model=schemas.CommentRead)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    c = crud_mod.get_comment(db, comment_id)
    if not c:
        raise HTTPException(status_code=404, detail="Comment not found")
    return c


@app.put("/comments/{comment_id}", response_model=schemas.CommentRead)
def update_comment(comment_id: int, data: schemas.CommentUpdate, db: Session = Depends(get_db)):
    c = crud_mod.update_comment(db, comment_id, data.dict(exclude_unset=True))
    if not c:
        raise HTTPException(status_code=404, detail="Comment not found")
    return c


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    ok = crud_mod.delete_comment(db, comment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Comment not found")
    return JSONResponse({"ok": True})


# --- Вложения ---
@app.post("/attachments/", response_model=schemas.AttachmentRead)
def create_attachment(data: schemas.AttachmentCreate, db: Session = Depends(get_db)):
    return crud_mod.create_attachment(db, data.dict())


@app.get("/attachments/", response_model=List[schemas.AttachmentRead])
def list_attachments(db: Session = Depends(get_db)):
    return db.query(models.Attachment).all()


@app.get("/attachments/{attachment_id}", response_model=schemas.AttachmentRead)
def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    a = crud_mod.get_attachment(db, attachment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return a


@app.put("/attachments/{attachment_id}", response_model=schemas.AttachmentRead)
def update_attachment(attachment_id: int, data: schemas.AttachmentUpdate, db: Session = Depends(get_db)):
    a = crud_mod.update_attachment(db, attachment_id, data.dict(exclude_unset=True))
    if not a:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return a


@app.delete("/attachments/{attachment_id}")
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    ok = crud_mod.delete_attachment(db, attachment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return JSONResponse({"ok": True})


# --- Отчёты и демонстрации функций ---
@app.get("/reports/tasks_with_project")
def tasks_with_project(db: Session = Depends(get_db), left: bool = True):
    """Отчёт: задачи с данными проектов. По умолчанию LEFT JOIN."""
    if left:
        q = db.query(models.Task, models.Project).join(models.Project, models.Task.project_id == models.Project.id, isouter=True)
    else:
        # INNER JOIN
        q = db.query(models.Task, models.Project).join(models.Project, models.Task.project_id == models.Project.id)
    results = []
    for task, proj in q.all():
        results.append({
            "task_id": task.id,
            "task_name": task.name,
            "project_id": proj.id if proj else None,
            "project_name": proj.name if proj else None,
        })
    return results


@app.get("/reports/project_task_count")
def project_task_count(db: Session = Depends(get_db)):
    """Отчёт: количество задач на проект (LEFT JOIN + GROUP BY)."""
    q = db.query(models.Project.id, models.Project.name, func.count(models.Task.id).label("task_count")).outerjoin(models.Task).group_by(models.Project.id, models.Project.name)
    return [{"project_id": r[0], "project_name": r[1], "task_count": int(r[2])} for r in q.all()]


@app.get("/demo/sets")
def demo_set_operations(db: Session = Depends(get_db)):
    """Демонстрация операций множеств: UNION между именами проектов и задач."""
    from sqlalchemy import union_all, select

    p = select(models.Project.name.label("name"))
    t = select(models.Task.name.label("name"))
    u = union_all(p, t)
    rows = db.execute(u).fetchall()
    return [r[0] for r in rows]


@app.get("/demo/functions")
def demo_functions(db: Session = Depends(get_db)):
    """Демонстрация встроенных функций: UPPER, LEN."""
    q = db.query(models.Project.id, func.upper(models.Project.name), func.length(models.Project.name)).limit(50)
    return [{"id": r[0], "name_upper": r[1], "name_len": r[2]} for r in q.all()]
