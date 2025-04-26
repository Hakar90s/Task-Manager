# callbacks.py

import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edited text immediately."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def move_task(tid, new_tab):
    """Move a task, then refresh so it disappears from this column."""
    handle.move_task(tid, new_tab)
    st.experimental_rerun()

def delete_task(tid):
    """Delete a task and refresh."""
    handle.delete_task(tid)
    st.experimental_rerun()

def add_placeholder(tab):
    """
    Add an empty new‐card placeholder.
    Clears any stray session_state for that new index,
    then forces a rerun so the UI shows it immediately.
    """
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    # clear old input state if it exists
    st.session_state.pop(f"new_{tab}_{idx}", None)
    # add placeholder
    st.session_state[key].append("")
    st.experimental_rerun()

def save_new(tab, idx):
    """
    Persist placeholder to the DB (if non-empty),
    clear its session state, remove it, and rerun.
    """
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    # clean up both the placeholder and its saved text
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    st.session_state.pop(text_key, None)
    st.experimental_rerun()

def delete_new(tab, idx):
    """
    Discard a placeholder without saving.
    Clears its session key and reruns immediately.
    """
    # remove placeholder
    st.session_state[f"new_boxes_{tab}"].pop(idx)
    # clear any typed text
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.experimental_rerun()
