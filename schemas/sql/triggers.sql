-- Триггеры для демонстрации (T-SQL)
GO

-- AFTER INSERT на таблицу tasks: логируем добавление в вспомогательную таблицу audit_tasks
IF OBJECT_ID('audit_tasks') IS NULL
BEGIN
    CREATE TABLE audit_tasks (
        id INT IDENTITY(1,1) PRIMARY KEY,
        task_id INT,
        action NVARCHAR(50),
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

CREATE TRIGGER trg_tasks_after_insert
ON tasks
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO audit_tasks (task_id, action)
    SELECT id, 'INSERT' FROM inserted;
END
GO

-- AFTER UPDATE на tasks: логируем изменения
CREATE TRIGGER trg_tasks_after_update
ON tasks
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO audit_tasks (task_id, action)
    SELECT id, 'UPDATE' FROM inserted;
END
GO

-- AFTER DELETE на tasks: логируем удаление
CREATE TRIGGER trg_tasks_after_delete
ON tasks
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO audit_tasks (task_id, action)
    SELECT id, 'DELETE' FROM deleted;
END
GO

-- INSTEAD OF INSERT на представлении (пример): создаём простую view и триггер INSTEAD OF
-- DROP VIEW если существует, затем создаём новую
IF OBJECT_ID('v_project_summaries') IS NOT NULL
BEGIN
    DROP VIEW v_project_summaries;
END
GO

CREATE VIEW v_project_summaries AS
SELECT p.id AS project_id, p.name, COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name;
GO

CREATE TRIGGER trg_v_project_summaries_instead_of_insert
ON v_project_summaries
INSTEAD OF INSERT
AS
BEGIN
    -- Через view вставлять напрямую нельзя, но для демонстрации: создадим проект при вставке в view
    INSERT INTO projects (name, description)
    SELECT name, NULL FROM inserted;
END
GO
