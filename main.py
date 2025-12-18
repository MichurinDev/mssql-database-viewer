"""Единая точка входа для запуска бэкенда.

Запускает Uvicorn-сервер с приложением FastAPI из `app.backend.api`.
Пример запуска:
    python main.py
или
    python -m main
"""
import uvicorn


def main():
    # Запускаем сервер на localhost:8000
    uvicorn.run("app.backend.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
