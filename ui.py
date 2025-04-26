import streamlit as st
import handle
import callbacks
from constants import TABS

def render_header():
    st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

def calc_height(text):
    lines = text.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """Draw a saved task as a card with small move/delete icons."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Move arrow (cycles to the next tab)
    next_tab = TABS[(TABS.index(tab) + 1) % len(TABS)]
    st.button(
        "➡️",
        key=f"move_{tid}",
        on_click=callbacks.move_task,
        args=(tid, next_tab),
        help=f"Move to {next_tab}",
    )

    # Delete icon
    st.button(
        "❌",
        key=f"del_{tid}",
        on_click=callbacks.delete_task,
        args=(tid,),
        help="Delete this card",
    )

    # Auto-saving text area
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
    """Draw a new-card placeholder."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    st.text_area(
        label="",
        value="",
        key=f"new_{tab}_{idx}",
        height=80,
        label_visibility="collapsed",
    )

    st.button(
        "💾",
        key=f"new_save_{tab}_{idx}",
        on_click=callbacks.save_new,
        args=(tab, idx),
        help="Save this new card",
    )
    st.button(
        "❌",
        key=f"new_del_{tab}_{idx}",
        on_click=callbacks.delete_new,
        args=(tab, idx),
        help="Discard this card",
    )

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    """Lay out all four columns with their cards and the Add New button."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            # Existing tasks
            for tid, content in handle.fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # Add New (single click)
            st.button(
                "➕ Add New",
                key=f"add_new_{tab}",
                on_click=callbacks.add_placeholder,
                args=(tab,),
                help="Create a new card",
            )

            # New placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
