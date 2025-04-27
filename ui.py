import streamlit as st
import handle
import callbacks
from constants import TABS

def render_header():
    st.markdown(
        '<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>',
        unsafe_allow_html=True,
    )

def calc_height(content):
    lines = content.count("\n") + 1
    return max(80, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    """Draw a saved task with delete and move controls."""
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row: delete icon (left) | spacer | move controls (right)
    c_del, c_spacer, c_move = st.columns([1,6,2], gap="small")
    with c_del:
        st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            use_container_width=True,
            help="Delete this card",
        )
    with c_move:
        sel_key = f"move_sel_{tid}"
        st.selectbox(
            "", 
            options=[t for t in TABS if t != tab],
            key=sel_key,
            label_visibility="collapsed",
        )
        st.button(
            "🔀",
            key=f"move_btn_{tid}",
            on_click=callbacks.move_existing,
            args=(tid, st.session_state[sel_key]),
            use_container_width=True,
            help="Move to selected tab",
        )

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

def render_board():
    """Lay out columns with their cards and the Add New input/button."""
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            # Fetch existing cards
            cards = handle.fetch_tasks_by_tab(tab)
            for tid, content in cards:
                render_existing_card(tab, tid, content)

            # Add New input only if under 20 cards
            if len(cards) < 20:
                input_key = f"new_input_{tab}"
                # Initialize session state for the input if needed
                st.session_state.setdefault(input_key, "")
                st.text_area(
                    label="",
                    key=input_key,
                    placeholder="Enter new task…",
                    height=80,
                    label_visibility="collapsed",
                )
                st.button(
                    "➕ Add New",
                    key=f"add_new_{tab}",
                    on_click=callbacks.add_new_confirm,
                    args=(tab,),
                    use_container_width=True,
                    help="Save new card and prepare for next",
                )
            else:
                st.warning("🔒 20-card limit reached in this column.")
