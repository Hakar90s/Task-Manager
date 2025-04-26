import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def move_task(tid, new_tab):
    """Move a task."""
    handle.move_task(tid, new_tab)

def delete_task(tid):
    """Delete a task."""
    handle.delete_task(tid)

def add_placeholder(tab):
    """Add an empty new‐card placeholder on first click."""
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    # clear any stray input state
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    """Persist a new placeholder (if non‐empty) and remove it."""
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    # safely remove placeholder
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
