"""Файл демо удалён — не используется в проекте.

Оставлен как маркер; реальных демонстраций больше нет.
"""

# Файл демо удалён — используйте app.backend.api и main.py для запуска.
        "size_kb": 1
    })
    print('status', r.status_code, 'body', r.json())

    # list projects
    print('Listing projects...')
    r = requests.get(f"{BASE}/projects/")
    print('status', r.status_code, 'body', r.json())


if __name__ == '__main__':
    demo()
