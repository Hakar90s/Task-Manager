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
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row: delete icon (left), spacer, move dropdown + button (right)
    c_del, c_spacer, c_move = st.columns([1,6,3], gap="small")
    with c_del:
        st.button(
            "❌",
            key=f"del_{tid}",
            on_click=callbacks.delete_task,
            args=(tid,),
            use_container_width=True,
            help="Delete this card"
        )
    with c_move:
        # dropdown
        st.selectbox(
            "",
            options=[t for t in TABS if t != tab],
            key=f"move_sel_{tid}",
            label_visibility="collapsed",
        )
        # confirm move
        st.button(
            "🔀",
            key=f"move_btn_{tid}",
            on_click=callbacks.move_existing,
            args=(tid,),
            use_container_width=True,
            help="Move to selected tab"
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
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            # Existing cards
            cards = handle.fetch_tasks_by_tab(tab)
            for tid, content in cards:
                render_existing_card(tab, tid, content)

            # Add New input & button (up to 20)
            if len(cards) < 20:
                input_key = f"new_input_{tab}"
                st.session_state.setdefault(input_key, "")
                st.text_area(
                    label="",
                    key=input_key,
                    placeholder="Enter new task…",
                    height=80,
                    label_visibility="collapsed"
                )
                st.button(
                    "➕ Add New",
                    key=f"add_new_{tab}",
                    on_click=callbacks.add_new_confirm,
                    args=(tab,),
                    use_container_width=True,
                    help="Save new card and get a fresh input"
                )
            else:
                st.warning("🔒 20-card limit reached")

