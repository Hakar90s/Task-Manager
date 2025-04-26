import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def move_task(tid, new_tab):
    """Move a task and refresh so it disappears from this column."""
    handle.move_task(tid, new_tab)
    st.experimental_rerun()

def delete_task(tid):
    """Delete a task and refresh."""
    handle.delete_task(tid)
    st.experimental_rerun()

def add_placeholder(tab):
    """
    Add an empty new‐card placeholder on first click, truly empty.
    """
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    # clear any old text state for that slot
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")
    st.experimental_rerun()

def save_new(tab, idx):
    """
    Persist the new placeholder (if non‐empty), then remove it.
    """
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.session_state.pop(text_key, None)
    st.experimental_rerun()

def delete_new(tab, idx):
    """
    Discard a new‐card placeholder instantly.
    """
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.experimental_rerun()
