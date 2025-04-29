import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    """Save edits to an existing card instantly."""
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def delete_task(tid):
    """Delete a card."""
    handle.delete_task(tid)

def add_placeholder(tab):
    """Add an empty new-card input for the given tab."""
    key = f"new_input_{tab}"
    # Initialize if needed
    st.session_state.setdefault(key, "")

def add_new_confirm(tab):
    """
    Save the new-card input, clear it, and append
    a blank slot if still under 20 cards.
    """
    input_key = f"new_input_{tab}"
    text = st.session_state.get(input_key, "").strip()
    if text:
        handle.add_task(text, tab)
    # Clear for next entry
    st.session_state[input_key] = ""

def move_existing(tid):
    """Move an existing card to the selected tab."""
    sel_key = f"move_sel_{tid}"
    new_tab = st.session_state.get(sel_key)
    if new_tab:
        handle.move_task(tid, new_tab)

