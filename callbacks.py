# callbacks.py

import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def move_task(tid, new_tab):
    """Move a task and force a rerun so it disappears here."""
    handle.move_task(tid, new_tab)
    st.experimental_rerun()

def delete_task(tid):
    """Delete a task and re-render."""
    handle.delete_task(tid)
    st.experimental_rerun()

def add_placeholder(tab):
    """Add an empty new‐card placeholder."""
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    # clear any old state for this new index
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    """Persist a new placeholder to the DB, then remove it."""
    text = st.session_state.get(f"new_{tab}_{idx}", "").strip()
    if text:
        handle.add_task(text, tab)
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.experimental_rerun()

def delete_new(tab, idx):
    """Remove a new‐card placeholder without saving."""
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.experimental_rerun()
