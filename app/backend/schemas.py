from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = None


class ProjectRead(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    project_id: int
    name: str
    priority: Optional[str] = None
    status: Optional[str] = None
    period_of_execution: Optional[date] = None
    time_estimation: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    period_of_execution: Optional[date] = None
    time_estimation: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    task_id: int
    author: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None
    is_edit: Optional[bool] = False
    rating: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    author: Optional[str] = None
    message: Optional[str] = None
    is_edit: Optional[bool] = None
    rating: Optional[int] = None


class CommentRead(CommentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AttachmentBase(BaseModel):
    comment_id: int
    file_name: Optional[str] = None
    type: Optional[str] = None
    size_kb: Optional[int] = None
    created_at: Optional[datetime] = None
    is_visible: Optional[bool] = True


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentUpdate(BaseModel):
    file_name: Optional[str] = None
    type: Optional[str] = None
    size_kb: Optional[int] = None
    is_visible: Optional[bool] = None


class AttachmentRead(AttachmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
