# handle.py
import psycopg2
import streamlit as st
from constants import TABS

# Map friendly tab names → (table_name, column_name)
TAB_MAP = {
    "Tasks": ("task", "task"),
    "In Progress": ("in_progress", "in_progress"),
    "Done": ("done", "done"),
    "Brainstorm": ("brainstorm", "brainstorm"),
}

def get_connection():
    return psycopg2.connect(st.secrets["postgres"]["connection_string"])

# ──────────────────────────────────────────────
def fetch_tasks_by_tab(tab_name):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT id, {col} FROM {table} ORDER BY id ASC")
        return cur.fetchall()

def add_task(content, tab_name):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"INSERT INTO {table} ({col}) VALUES (%s)", (content,))
        conn.commit()

def delete_task(tab_name, task_id):
    table, _ = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"DELETE FROM {table} WHERE id = %s", (task_id,))
        conn.commit()

def update_task(tab_name, task_id, new_content):
    table, col = TAB_MAP[tab_name]
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"UPDATE {table} SET {col} = %s WHERE id = %s",
                    (new_content, task_id))
        conn.commit()

def move_task(current_tab, task_id, content, direction):
    """
    Copy the task to the next/previous table, then delete it from the current one.
    """
    tabs = list(TABS)
    idx = tabs.index(current_tab)
    new_idx = idx + (1 if direction == "forward" else -1)

    if not (0 <= new_idx < len(tabs)):
        return  # out of bounds, nothing to do

    new_tab = tabs[new_idx]
    # 1) create in new table
    add_task(content, new_tab)
    # 2) delete from current table
    delete_task(current_tab, task_id)
