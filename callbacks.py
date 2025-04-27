import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def delete_task(tid):
    """Delete a task."""
    handle.delete_task(tid)

def add_placeholder(tab):
    """Add an empty new-card placeholder immediately."""
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    # Clear any leftover text state
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    """Persist a new placeholder; then remove it from the placeholder list."""
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(text_key, None)

def delete_new(tab, idx):
    """Discard a new-card placeholder."""
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(f"new_{tab}_{idx}", None)

def move_existing(tid, tab):
    """Move an existing task and update DB."""
    handle.move_task(tid, tab)

def move_new(tab_from, idx, tab_to):
    """Move a placeholder from one tab to another."""
    # Extract text
    key = f\"new_{tab_from}_{idx}\"
    text = st.session_state.pop(key, \"\")
    # Remove placeholder from source
    boxes = st.session_state.get(f\"new_boxes_{tab_from}\", [])
    if idx < len(boxes):
        boxes.pop(idx)
    # Append to destination
    dest = f\"new_boxes_{tab_to}\"
    new_idx = len(st.session_state.setdefault(dest, []))
    st.session_state[dest].append(text)
    # Set text state in new location
    st.session_state[f\"new_{tab_to}_{new_idx}\"] = text
