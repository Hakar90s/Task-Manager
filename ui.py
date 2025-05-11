import streamlit as st
import handle
import callbacks
from constants import TABS

def render_header():
    st.markdown(
        """
        <div class="header-container">
            <div class="header-content">
                <div class="app-icon">🗂️</div>
                <h1>Task Manager Pro</h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def calc_height(content):
    lines = content.count("\n") + 1
    return max(90, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    tab_index = TABS.index(tab)
    
    st.markdown(f'<div class="task-card" id="task-{tid}">', unsafe_allow_html=True)
    
    # Ensure unique key by including tab
    key = f"edit_{tab}_{tid}"

    st.text_area(
        label="",
        value=content,
        key=key,
        height=calc_height(content),
        on_change=callbacks.auto_save,
        args=(tab, tid),
        label_visibility="collapsed",
    )

    cols = st.columns([1, 1, 2])

    with cols[0]:
        if tab_index > 0:
            st.button(
                "⬅️",
                key=f"back_{tab}_{tid}",
                on_click=callbacks.move_card,
                args=(tab, tid, st.session_state.get(key, ""), "backward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index - 1]}",
            )

    with cols[1]:
        if tab_index < len(TABS) - 1:
            st.button(
                "➡️",
                key=f"fwd_{tab}_{tid}",
                on_click=callbacks.move_card,
                args=(tab, tid, st.session_state.get(key, ""), "forward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index + 1]}",
            )

    with cols[2]:
        st.button(
            "🗑️ Delete",
            key=f"del_{tab}_{tid}",
            on_click=callbacks.delete_task,
            args=(tab, tid),
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

def render_placeholder(tab, box_id):
    tab_index = TABS.index(tab)

    st.markdown('<div class="task-card placeholder">', unsafe_allow_html=True)

    st.text_area(
        label="",
        key=f"new_box_{tab}_{box_id}",
        placeholder="Enter new task…",
        height=calc_height(""),
        on_change=callbacks.add_new_confirm,
        args=(tab, box_id),
        label_visibility="collapsed",
    )

    cols = st.columns([1, 1, 2])

    with cols[0]:
        if tab_index > 0:
            st.button(
                "⬅️",
                key=f"ph_back_{tab}_{box_id}",
                on_click=callbacks.move_placeholder,
                args=(tab, box_id, "backward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index - 1]}",
            )

    with cols[1]:
        if tab_index < len(TABS) - 1:
            st.button(
                "➡️",
                key=f"ph_fwd_{tab}_{box_id}",
                on_click=callbacks.move_placeholder,
                args=(tab, box_id, "forward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index + 1]}",
            )

    with cols[2]:
        st.button(
            "🗑️ Discard",
            key=f"ph_del_{tab}_{box_id}",
            on_click=callbacks.delete_placeholder,
            args=(tab, box_id),
            use_container_width=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    cols = st.columns(len(TABS))
    for col, tab in zip(cols, TABS):
        with col:
            st.markdown(f"<div class='column-header'>{tab}</div>", unsafe_allow_html=True)

            with st.container():
                cards = handle.fetch_tasks_by_tab(tab)
                for tid, content in cards:
                    render_existing_card(tab, tid, content)

                boxes = st.session_state.get(f"new_boxes_{tab}", [])
                for box_id in boxes:
                    render_placeholder(tab, box_id)

                total = len(cards) + len(boxes)
                if total < 20:
                    st.button(
                        "➕ Add New",
                        key=f"add_new_{tab}",
                        on_click=callbacks.add_placeholder,
                        args=(tab,),
                        use_container_width=True,
                        type="primary",
                    )
                else:
                    st.warning("🔒 20-card limit reached")
