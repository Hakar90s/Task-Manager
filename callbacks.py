# callbacks.py
import uuid
import streamlit as st
import handle
from constants import TABS

# ──────────────────────────────────────────────
def _force_refresh():
    """Trigger a full rerun so UI always matches state."""
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# ─────────── Existing‑card handlers ───────────
def auto_save(tab, tid):
    handle.update_task(tab, tid, st.session_state[f"edit_{tid}"])
    _force_refresh()

def delete_task(tab, tid):
    handle.delete_task(tab, tid)
    _force_refresh()

def move_card(tab, tid, content, direction):
    handle.move_task(tab, tid, content, direction)
    _force_refresh()

# ────────── Placeholder‑card handlers ─────────
def add_placeholder(tab):
    box_id = str(uuid.uuid4())
    key = f"new_boxes_{tab}"
    # re‑assign list (change detection)
    st.session_state[key] = st.session_state.get(key, []) + [box_id]
    st.session_state[f"new_box_{tab}_{box_id}"] = ""
    _force_refresh()

def delete_placeholder(tab, box_id):
    key = f"new_boxes_{tab}"
    st.session_state[key] = [bid for bid in st.session_state.get(key, []) if bid != box_id]
    st.session_state.pop(f"new_box_{tab}_{box_id}", None)
    _force_refresh()

def add_new_confirm(tab, box_id):
    text = st.session_state.get(f"new_box_{tab}_{box_id}", "").strip()
    if text:
        handle.add_task(text, tab)
    delete_placeholder(tab, box_id)   # includes refresh

def move_placeholder(tab, box_id, direction):
    tabs = TABS
    idx = tabs.index(tab)
    new_idx = idx + (1 if direction == "forward" else -1)
    if not (0 <= new_idx < len(tabs)):
        return                      # out of bounds – nothing to do

    new_tab = tabs[new_idx]

    # ---- remove from current column ----
    cur_key = f"new_boxes_{tab}"
    st.session_state[cur_key] = [bid for bid in st.session_state.get(cur_key, []) if bid != box_id]

    # ---- add to target column ----
    new_key = f"new_boxes_{new_tab}"
    st.session_state[new_key] = st.session_state.get(new_key, []) + [box_id]

    # ---- migrate its text ----
    old_txt_key = f"new_box_{tab}_{box_id}"
    new_txt_key = f"new_box_{new_tab}_{box_id}"
    st.session_state[new_txt_key] = st.session_state.get(old_txt_key, "")
    st.session_state.pop(old_txt_key, None)

    _force_refresh()
