from sqlalchemy.orm import Session
from ..models.models import Project, Task, Comment, Attachment
from .db import SessionLocal
from typing import Optional, Dict, Any


# --- Project CRUD ---
def create_project(session: Session, data: Dict[str, Any]) -> Project:
    proj = Project(**data)
    session.add(proj)
    session.commit()
    session.refresh(proj)
    return proj


def get_project(session: Session, project_id: int) -> Optional[Project]:
    return session.get(Project, project_id)


def update_project(session: Session, project_id: int, data: Dict[str, Any]) -> Optional[Project]:
    proj = session.get(Project, project_id)
    if not proj:
        return None
    for k, v in data.items():
        setattr(proj, k, v)
    session.commit()
    session.refresh(proj)
    return proj


def delete_project(session: Session, project_id: int) -> bool:
    proj = session.get(Project, project_id)
    if not proj:
        return False
    session.delete(proj)
    session.commit()
    return True


# --- Task CRUD ---
def create_task(session: Session, data: Dict[str, Any]) -> Task:
    t = Task(**data)
    session.add(t)
    session.commit()
    session.refresh(t)
    return t


def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)


def update_task(session: Session, task_id: int, data: Dict[str, Any]) -> Optional[Task]:
    t = session.get(Task, task_id)
    if not t:
        return None
    for k, v in data.items():
        setattr(t, k, v)
    session.commit()
    session.refresh(t)
    return t


def delete_task(session: Session, task_id: int) -> bool:
    t = session.get(Task, task_id)
    if not t:
        return False
    session.delete(t)
    session.commit()
    return True


# --- Comment CRUD ---
def create_comment(session: Session, data: Dict[str, Any]) -> Comment:
    c = Comment(**data)
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


def get_comment(session: Session, comment_id: int) -> Optional[Comment]:
    return session.get(Comment, comment_id)


def update_comment(session: Session, comment_id: int, data: Dict[str, Any]) -> Optional[Comment]:
    c = session.get(Comment, comment_id)
    if not c:
        return None
    for k, v in data.items():
        setattr(c, k, v)
    session.commit()
    session.refresh(c)
    return c


def delete_comment(session: Session, comment_id: int) -> bool:
    c = session.get(Comment, comment_id)
    if not c:
        return False
    session.delete(c)
    session.commit()
    return True


# --- Attachment CRUD ---
def create_attachment(session: Session, data: Dict[str, Any]) -> Attachment:
    a = Attachment(**data)
    session.add(a)
    session.commit()
    session.refresh(a)
    return a


def get_attachment(session: Session, attachment_id: int) -> Optional[Attachment]:
    return session.get(Attachment, attachment_id)


def update_attachment(session: Session, attachment_id: int, data: Dict[str, Any]) -> Optional[Attachment]:
    a = session.get(Attachment, attachment_id)
    if not a:
        return None
    for k, v in data.items():
        setattr(a, k, v)
    session.commit()
    session.refresh(a)
    return a


def delete_attachment(session: Session, attachment_id: int) -> bool:
    a = session.get(Attachment, attachment_id)
    if not a:
        return False
    session.delete(a)
    session.commit()
    return True
