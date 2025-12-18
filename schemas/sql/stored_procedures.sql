-- Хранимые процедуры для демонстрации
GO

-- 1) Процедура без параметров: возвращает все активные проекты
CREATE PROCEDURE sp_get_active_projects
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * FROM projects WHERE is_active = 1;
END
GO

-- 2) Процедура с входным параметром: возвращает задачи для проекта
CREATE PROCEDURE sp_get_tasks_for_project
    @proj_id INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * FROM tasks WHERE project_id = @proj_id;
END
GO

-- 3) Процедура с выходным параметром: возвращает количество задач в проекте
CREATE PROCEDURE sp_count_tasks_for_project
    @proj_id INT,
    @out_count INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT @out_count = COUNT(*) FROM tasks WHERE project_id = @proj_id;
END
GO
