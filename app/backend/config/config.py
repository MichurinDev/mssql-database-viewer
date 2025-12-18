import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

env_path = find_dotenv()
if not env_path:  # Функция поиска переменных окружения
    print("Warning: .env not found — будут использованы переменные окружения окружения (если заданы)")
else:
    load_dotenv(env_path)  # Загрузка переменных окружения

root_path = Path(__file__).resolve().parents[1]

# MSSQL
MSSQL_IP=os.getenv("MSSQL_IP")
MSSQL_PORT=os.getenv("MSSQL_PORT")
MSSQL_USER=os.getenv("MSSQL_USER")
MSSQL_PASSWORD=os.getenv("MSSQL_PASSWORD")
MSSQL_DATABASE=os.getenv("MSSQL_DATABASE")
