import sqlite3

def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_task(user_id, task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, task) VALUES (?, ?)",
        (user_id, task)
    )

    conn.commit()
    conn.close()


def get_tasks(user_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, task FROM tasks WHERE user_id = ?",
        (user_id,)
    )

    tasks = cursor.fetchall()

    conn.close()
    return tasks


def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()
    

def clear_tasks(user_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()