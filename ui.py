import streamlit as st
import handle
import callbacks
from constants import TABS

def render_header():
    st.markdown(
        '<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>',
        unsafe_allow_html=True,
    )

def calc_height(text):
    lines = text.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """Draw a saved task with a small move‐dropdown at top‐left and delete icon at top‐right."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row: move‐select | delete icon
    col_move, col_del, col_text = st.columns([1,1,8], gap="small")
    with col_move:
        options = [t for t in TABS if t != tab]
        def _on_move(tid=tid):
            new_tab = st.session_state[f"move_sel_{tid}"]
            callbacks.move_task(tid, new_tab)
        st.selectbox(
            label="🔀",
            options=options,
            key=f"move_sel_{tid}",
            on_change=_on_move,
            label_visibility="visible"
        )
    with col_del:
        st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            use_container_width=True
        )
    with col_text:
        st.text_area(
            label="",
            value=content,
            key=f"edit_{tid}",
            height=calc_height(content),
            on_change=callbacks.auto_save,
            args=(tid,),
            label_visibility="collapsed"
        )

    st.markdown('</div>', unsafe_allow_html=True)

def render_new_card(tab, idx):
    """Draw a new‐card placeholder that auto‐saves on edit, with delete below."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Auto‐saving textarea
    def _on_new(tab=tab, i=idx):
        callbacks.save_new(tab, i)
    st.text_area(
        label="",
        value="",
        key=f"new_{tab}_{idx}",
        height=80,
        on_change=_on_new,
        label_visibility="collapsed"
    )

    # small delete icon below
    if st.button(
        "❌",
        key=f"new_del_{tab}_{idx}",
        on_click=callbacks.delete_new,
        args=(tab, idx),
        use_container_width=True
    ):
        pass

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    """Lay out the four columns with cards and the Add New button."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)
            # existing tasks
            for tid, content in handle.fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # add new on first click
            st.button(
                "➕ Add New",
                key=f"add_new_{tab}",
                on_click=callbacks.add_placeholder,
                args=(tab,),
                use_container_width=True
            )

            # new placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
