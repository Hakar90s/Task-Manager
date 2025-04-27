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
    Draw a saved task as a card with:
    - a tiny delete icon at top-left
    - a tiny move icon at top-right that, when clicked, reveals a dropdown + confirmation icon
    - an auto-saving textarea
    """
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row layout: delete | spacer | move area
    col_del, col_spacer, col_move = st.columns([1,8,2], gap="small")
    # Delete icon
    with col_del:
        if st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            use_container_width=True,
            help="Delete this card"
        ):
            pass

    # Move icon or dropdown
    flag_key = f"show_move_{tid}"
    show = st.session_state.get(flag_key, False)
    with col_move:
        if not show:
            if st.button(
                "🔽",
                key=f"toggle_move_{tid}",
                on_click=callbacks.toggle_move_selector,
                args=(tid,),
                use_container_width=True,
                help="Choose where to move"
            ):
                pass
        else:
            # dropdown to select destination
            st.selectbox(
                label="",
                options=[t for t in TABS if t != tab],
                key=f"move_sel_{tid}",
                label_visibility="collapsed",
            )
            # confirmation icon
            if st.button(
                "🔀",
                key=f"confirm_move_{tid}",
                on_click=callbacks.perform_move,
                args=(tid,),
                use_container_width=True,
                help="Move to selected tab"
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
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

def render_new_card(tab, idx):
    """Draw a new‐card placeholder that auto-saves on edit, with delete below."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Auto-saving textarea for new card
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

    # delete icon below
    if st.button(
        "❌",
        key=f"new_del_{tab}_{idx}",
        on_click=callbacks.delete_new,
        args=(tab, idx),
        use_container_width=True,
        help="Discard this new card"
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
            for tid, content in handle.fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            # Add New (single click)
            if st.button(
                "➕ Add New",
                key=f"add_new_{tab}",
                on_click=callbacks.add_placeholder,
                args=(tab,),
                use_container_width=True,
                help="Create a new card"
            ):
                pass

            # New placeholders
            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
