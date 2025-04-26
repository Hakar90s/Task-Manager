# ui.py

import streamlit as st
import handle
from constants import TABS
import callbacks

def render_header():
    st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

def calc_height(text):
    lines = text.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """Draw a single saved task card."""
    h = calc_height(content)
    st.markdown('<div class="task-card">', unsafe_allow_html=True)
    st.text_area(
        label="",
        value=content,
        key=f"edit_{tid}",
        height=h,
        on_change=callbacks.auto_save,
        args=(tid,),
        label_visibility="collapsed"
    )
    # Move button cycles to next tab
    next_tab = TABS[(TABS.index(tab) + 1) % len(TABS)]
    st.markdown(f'<button class="icon-btn icon-move" title="Move to {next_tab}">➡️</button>', unsafe_allow_html=True)
    st.button("", key=f"move_{tid}", on_click=callbacks.move_task, args=(tid, next_tab))
    # Delete icon
    st.markdown('<button class="icon-btn icon-delete" title="Delete">❌</button>', unsafe_allow_html=True)
    st.button("", key=f"del_{tid}", on_click=callbacks.delete_task, args=(tid,))
    st.markdown('</div>', unsafe_allow_html=True)

def render_new_card(tab, idx):
    """Draw a single new‐card placeholder."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)
    st.text_area(
        label="",
        value="",
        key=f"new_{tab}_{idx}",
        height=80,
        label_visibility="collapsed"
    )
    st.button("💾", key=f"new_save_{tab}_{idx}", on_click=callbacks.save_new, args=(tab, idx))
    st.button("❌", key=f"new_del_{tab}_{idx}", on_click=callbacks.delete_new, args=(tab, idx))
    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    """Lay out all four columns with cards and placeholders."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)
            # Existing tasks
            for _, (tid, content) in enumerate(handle.fetch_tasks_by_tab(tab), start=1):
                render_existing_card(tab, tid, content)
            # Add new button
            st.button("➕ Add New", key=f"add_new_{tab}", on_click=callbacks.add_placeholder, args=(tab,), help="Create a new card")
            # New placeholders
            for idx, _ in enumerate(st.session_state[f"new_boxes_{tab}"]):
                render_new_card(tab, idx)
