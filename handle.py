# handle.py
import psycopg2
import streamlit as st
from constants import TABS

# Mapping tabs to DB table and column
TAB_MAP = {
    "Tasks": ("task", "task"),
    "In Progress": ("in_progress", "in_progress"),
    "Done": ("done", "done"),
    "Brainstorm": ("brainstorm", "brainstorm"),
}

def get_connection():
    try:
        return psycopg2.connect(st.secrets["postgres"]["connection_string"])
    except KeyError:
        st.error("❌ Missing `postgres.connection_string` in your Streamlit secrets.")
        st.stop()
    except psycopg2.OperationalError as e:
        st.error("❌ Could not connect to the PostgreSQL database. Please check your connection string.")
        st.exception(e)
        st.stop()

# Fetch tasks for a given tab
def fetch_tasks_by_tab(tab_name):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT id, {col} FROM {table} ORDER BY id ASC")
        return cur.fetchall()

# Add new task
def add_task(content, tab_name):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"INSERT INTO {table} ({col}) VALUES (%s)", (content,))
        conn.commit()

# Delete a task by ID
def delete_task(tab_name, task_id):
    table, _ = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"DELETE FROM {table} WHERE id = %s", (task_id,))
        conn.commit()

# Update an existing task
def update_task(tab_name, task_id, new_content):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"UPDATE {table} SET {col} = %s WHERE id = %s", (new_content, task_id))
        conn.commit()

# Move task between tabs
def move_task(current_tab, task_id, content, direction):
    tabs = list(TABS)
    idx = tabs.index(current_tab)
    new_idx = idx + (1 if direction == "forward" else -1)

    if not (0 <= new_idx < len(tabs)):
        return  # No tab to move to

    new_tab = tabs[new_idx]
    add_task(content, new_tab)
    delete_task(current_tab, task_id)
