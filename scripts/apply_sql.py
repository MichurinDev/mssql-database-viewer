import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pymssql


def load_env(env_path: Path):
    if env_path.exists():
        load_dotenv(env_path)
    else:
        raise FileNotFoundError(f"Файл .env не найден по пути: {env_path}")


def get_connection_params():
    host = os.getenv("MSSQL_IP") or os.getenv("MSSQL_HOST")
    port = os.getenv("MSSQL_PORT")
    user = os.getenv("MSSQL_USER")
    password = os.getenv("MSSQL_PASSWORD")
    database = os.getenv("MSSQL_DATABASE")
    if not all([host, port, user, password, database]):
        raise ValueError("Не заданы все параметры подключения в .env")
    # pymssql expects host:port as server
    server = f"{host}:{port}"
    return server, user, password, database


def split_sql_statements(sql_text: str):
    # Split on lines that contain only GO (case-insensitive)
    parts = []
    current = []
    for line in sql_text.splitlines():
        if line.strip().upper() == 'GO':
            if current:
                parts.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        parts.append('\n'.join(current))
    return parts


def apply_sql_file(cursor, filepath: Path):
    print(f"Выполняю {filepath}")
    text = filepath.read_text(encoding='utf-8')
    statements = split_sql_statements(text)
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            cursor.execute(stmt)
            print("Успешно выполнено выражение — длина:", len(stmt))
        except Exception as e:
            print(f"Ошибка при выполнении выражения: {e}")
            raise


def main():
    env_path = Path(__file__).resolve().parents[1] / '.env'
    try:
        load_env(env_path)
    except Exception as e:
        print(str(e))
        return

    server, user, password, database = get_connection_params()
    print(f"Подключаюсь к серверу {server}, базе {database} как {user}")

    sql_dir = Path(__file__).resolve().parents[1] / 'schemas' / 'sql'
    if not sql_dir.exists():
        print(f"Папка со скриптами не найдена: {sql_dir}")
        return

    # Если передан путь к файлу в аргументе, применяем только его
    sql_files = []
    if len(sys.argv) > 1:
        arg_path = Path(sys.argv[1])
        if arg_path.is_file():
            sql_files = [arg_path]
        else:
            # попытаться отнести к папке schemas/sql
            candidate = sql_dir / sys.argv[1]
            if candidate.is_file():
                sql_files = [candidate]
            else:
                print(f"Указанный файл не найден: {sys.argv[1]}")
                return
    else:
        sql_files = sorted(sql_dir.glob('*.sql'))
        if not sql_files:
            print("SQL файлы не найдены в папке schemas/sql/")
            return

    conn = pymssql.connect(server=server, user=user, password=password, database=database)
    cursor = conn.cursor()
    try:
        for f in sql_files:
            apply_sql_file(cursor, f)
        conn.commit()
        print("Все скрипты успешно применены.")
    except Exception as e:
        print("Ошибка при применении скриптов:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
