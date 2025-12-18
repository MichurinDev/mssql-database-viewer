-- Создать индексы для ускорения типичных запросов
-- 1) индекс по projects(name)
CREATE INDEX IX_projects_name ON projects([name]);

-- 2) индекс по tasks(project_id)
CREATE INDEX IX_tasks_project_id ON tasks(project_id);

-- 3) частичный/композитный индекс по tasks(status, priority)
CREATE INDEX IX_tasks_status_priority ON tasks(status, priority);
