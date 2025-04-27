import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def delete_task(tid):
    """Delete a task."""
    handle.delete_task(tid)
    # no explicit rerun—Streamlit auto-refreshes

def add_placeholder(tab):
    """Add an empty new‐card placeholder."""
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    """Persist a new placeholder (if non‐empty) and remove it."""
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(text_key, None)

def delete_new(tab, idx):
    """Discard a new‐card placeholder."""
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(f"new_{tab}_{idx}", None)

def toggle_move_selector(tid):
    """Toggle the move‐dropdown visibility for this task."""
    key = f"show_move_{tid}"
    st.session_state[key] = not st.session_state.get(key, False)

def perform_move(tid):
    """Move the task to the selected tab."""
    sel_key = f"move_sel_{tid}"
    new_tab = st.session_state.get(sel_key)
    if new_tab:
        handle.move_task(tid, new_tab)
    st.session_state[f"show_move_{tid}"] = False
