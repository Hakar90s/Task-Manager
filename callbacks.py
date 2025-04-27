import streamlit as st
import handle
from constants import TABS

def auto_save(tid):
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

def delete_task(tid):
    handle.delete_task(tid)

def add_placeholder(tab):
    key = f"new_boxes_{tab}"
    idx = len(st.session_state.setdefault(key, []))
    st.session_state.pop(f"new_{tab}_{idx}", None)
    st.session_state[key].append("")

def save_new(tab, idx):
    text_key = f"new_{tab}_{idx}"
    text = st.session_state.get(text_key, "").strip()
    if text:
        handle.add_task(text, tab)
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(text_key, None)

def delete_new(tab, idx):
    boxes = st.session_state.get(f"new_boxes_{tab}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    st.session_state.pop(f"new_{tab}_{idx}", None)

def move_existing(tid, new_tab):
    handle.move_task(tid, new_tab)

def move_new(tab_from, idx, tab_to):
    # take text from placeholder
    key = f"new_{tab_from}_{idx}"
    text = st.session_state.pop(key, "")
    # remove from source
    boxes = st.session_state.get(f"new_boxes_{tab_from}", [])
    if idx < len(boxes):
        boxes.pop(idx)
    # add to destination
    dest = f"new_boxes_{tab_to}"
    new_idx = len(st.session_state.setdefault(dest, []))
    st.session_state[dest].append(text)
    # seed new textarea
    st.session_state[f"new_{tab_to}_{new_idx}"] = text
