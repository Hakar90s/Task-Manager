import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edits to an existing card instantly."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def delete_task(tid):
    """Delete a card."""
    handle.delete_task(tid)

def move_existing(tid, new_tab):
    """Move an existing card to another tab."""
    handle.move_task(tid, new_tab)

def add_new_confirm(tab):
    """
    Save the text from the new-card input, then clear it.
    Respects the 20-card limit (UI enforces hiding the input).
    """
    key = f"new_input_{tab}"
    text = st.session_state.get(key, "").strip()
    if text:
        handle.add_task(text, tab)
    # Clear for next entry
    st.session_state[key] = ""
