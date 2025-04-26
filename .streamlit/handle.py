import psycopg2
import streamlit as st

def get_connection():
    """Return a new connection to the Neon Postgres database."""
    return psycopg2.connect(st.secrets["postgres"]["connection_string"])

def fetch_tasks_by_tab(tab_name):
    """Fetch (id, content) for all tasks in the given tab."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, content FROM tasks WHERE tab = %s ORDER BY created_at ASC",
        (tab_name,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_task(content, tab_name):
    """Insert a new task into the specified tab."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (content, tab) VALUES (%s, %s)",
        (content, tab_name)
    )
    conn.commit()
    cur.close()
    conn.close()

def move_task(task_id, new_tab):
    """Move an existing task to another tab."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET tab = %s WHERE id = %s",
        (new_tab, task_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_task(task_id, new_content):
    """Update the text of an existing task."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET content = %s WHERE id = %s",
        (new_content, task_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )
    conn.commit()
    cur.close()
    conn.close()
