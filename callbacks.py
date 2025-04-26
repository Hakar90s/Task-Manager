# callbacks.py

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
    """Add an empty new‐card placeholder."""
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    """Persist a new placeholder (if non‐empty) and remove it."""
    key = f"new_{tab}_{idx}"
    text = st.session_state.get(key, "").strip()
    if text:
        handle.add_task(text, tab)
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.session_state.pop(key, None)

def delete_new(tab, idx):
    """Discard a new‐card placeholder."""
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.session_state.pop(f"new_{tab}_{idx}", None)
