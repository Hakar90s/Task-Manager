# ui.py

import streamlit as st
from constants import TABS
import callbacks

def render_header():
    st.markdown(
        '<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>',
        unsafe_allow_html=True,
    )

def calc_height(text):
    lines = text.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """
    Draw a saved task as a card with:
    - a small move-select at the top-left
    - a small delete icon at the top-right
    - an auto-saving textarea
    """
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row: move-select | delete icon
    c_move, c_del, c_text = st.columns([1,1,8], gap="small")
    with c_move:
        # dropdown to choose new tab
        options = [t for t in TABS if t != tab]
        def _on_move(tid=tid):
            new_tab = st.session_state[f"move_sel_{tid}"]
            callbacks.move_task(tid, new_tab)
        st.selectbox(
            label="",
            options=options,
            key=f"move_sel_{tid}",
            on_change=_on_move,
            label_visibility="collapsed",
        )
    with c_del:
        if st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            use_container_width=True,
        ):
            pass

    # Body: auto-saving textarea
    with c_text:
        st.text_area(
            label="",
            value=content,
            key=f"edit_{tid}",
            height=calc_height(content),
            on_change=callbacks.auto_save,
            args=(tid,),
            label_visibility="collapsed",
        )

    st.markdown('</div>', unsafe_allow_html=True)

def render_new_card(tab, idx):
    """
    Draw a new-card placeholder with:
    - auto-save on textarea change
    - a delete icon below
    No manual save button.
    """
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Text area (auto-save on change)
    def _on_new(tab=tab, i=idx):
        callbacks.save_new(tab, i)
    st.text_area(
        label="",
        value="",
        key=f"new_{tab}_{idx}",
        height=80,
        on_change=_on_new,
        label_visibility="collapsed",
    )

    # Delete icon below
    if st.button(
        "❌",
        key=f"new_del_{tab}_{idx}",
        on_click=callbacks.delete_new,
        args=(tab, idx),
        use_container_width=True,
    ):
        pass

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    """Lay out all columns with their cards and the Add New button."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            # Existing tasks
            for tid, content in __import__("handle").fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # Add New (single click)
            if st.button(
                "➕ Add New",
                key=f"add_new_{tab}",
                on_click=callbacks.add_placeholder,
                args=(tab,),
            ):
                pass

            # New placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
