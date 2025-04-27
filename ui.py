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
    """
    Draw a saved task with:
    - small delete icon at top-left
    - small move icon at top-right that toggles a dropdown
    - auto-saving textarea
    """
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Initialize the show_move flag
    flag_key = f"show_move_{tid}"
    show = st.session_state.setdefault(flag_key, False)

    # Top row: delete icon on left, move icon on right
    col_del, col_spacer, col_move = st.columns([1,8,1], gap="small")
    with col_del:
        if st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            help="Delete this card",
            use_container_width=True,
        ):
            pass
    with col_move:
        if not show:
            # show the dropdown icon
            if st.button(
                "⋯",
                key=f"show_move_btn_{tid}",
                on_click=callbacks.toggle_move_selector,
                args=(tid,),
                help="Move this card",
                use_container_width=True,
            ):
                pass
        else:
            # show the selectbox + confirm icon
            sel_key = f"move_sel_{tid}"
            st.selectbox(
                label="",
                options=[t for t in TABS if t != tab],
                key=sel_key,
                label_visibility="collapsed",
            )
            if st.button(
                "➤",
                key=f"confirm_move_{tid}",
                on_click=callbacks.confirm_move,
                args=(tid,),
                help="Confirm move",
                use_container_width=True,
            ):
                pass

    # Body: auto-saving textarea
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
        label_visibility="collapsed",
    )

    # delete icon below
    if st.button(
        "❌",
        key=f"new_del_{tab}_{idx}",
        on_click=callbacks.delete_new,
        args=(tab, idx),
        help="Discard this new card",
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

            # existing tasks
            for tid, content in handle.fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # add new
            if st.button(
                "➕ Add New",
                key=f"add_new_{tab}",
                on_click=callbacks.add_placeholder,
                args=(tab,),
                use_container_width=True,
            ):
                pass

            # new placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
