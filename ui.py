import streamlit as st
from constants import TABS
import callbacks

def render_header():
    st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

def calc_height(text):
    lines = text.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """Draw a saved task with small move/delete icons."""
    h = calc_height(content)
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # icon columns + text column
    icon1, icon2, textcol = st.columns([0.5, 0.5, 9])
    with icon1:
        next_tab = TABS[(TABS.index(tab) + 1) % len(TABS)]
        if st.button("➡️", key=f"move_{tid}", help=f"Move to {next_tab}",
                     on_click=callbacks.move_task, args=(tid, next_tab)):
            pass
    with icon2:
        if st.button("❌", key=f"del_{tid}", help="Delete this card",
                     on_click=callbacks.delete_task, args=(tid,)):
            pass
    with textcol:
        st.text_area(
            label="",
            value=content,
            key=f"edit_{tid}",
            height=h,
            on_change=callbacks.auto_save,
            args=(tid,),
            label_visibility="collapsed"
        )

    st.markdown('</div>', unsafe_allow_html=True)

def render_new_card(tab, idx):
    """Draw a new‐card placeholder with save/delete icons."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    icon1, icon2, textcol = st.columns([0.5, 0.5, 9])
    with textcol:
        st.text_area(
            label="",
            value="",
            key=f"new_{tab}_{idx}",
            height=80,
            label_visibility="collapsed"
        )
    with icon1:
        if st.button("💾", key=f"new_save_{tab}_{idx}", help="Save this new card",
                     on_click=callbacks.save_new, args=(tab, idx)):
            pass
    with icon2:
        if st.button("❌", key=f"new_del_{tab}_{idx}", help="Discard this card",
                     on_click=callbacks.delete_new, args=(tab, idx)):
            pass

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    """Lay out all four columns with their cards and the Add New button."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            # existing tasks
            for tid, content in __import__('handle').fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # add new
            if st.button("➕ Add New", key=f"add_new_{tab}",
                         on_click=callbacks.add_placeholder, args=(tab,),
                         help="Create a new card"):
                pass

            # render placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
