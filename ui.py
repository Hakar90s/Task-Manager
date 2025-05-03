
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
    # Calculate optimal height based on content length
    lines = content.count("\n") + 1
    return max(90, min(lines * 24, 300))

def render_existing_card(tab, tid, content):
    tab_index = TABS.index(tab)
    
    st.markdown(f'<div class="task-card" id="task-{tid}">', unsafe_allow_html=True)
    
    # Text area for content
    st.text_area(
        label="",
        value=content,
        key=f"edit_{tid}",
        height=calc_height(content),
        on_change=callbacks.auto_save,
        args=(tab, tid),
        label_visibility="collapsed",
    )
    
    # Action buttons row
    cols = st.columns([1, 1, 2])
    
    # Move backward button
    with cols[0]:
        if tab_index > 0:
            st.button(
                "⬅️",
                key=f"back_{tab}_{tid}",
                on_click=callbacks.move_card,
                args=(tab, tid, st.session_state.get(f"edit_{tid}", ""), "backward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index - 1]}",
            )
    
    # Move forward button
    with cols[1]:
        if tab_index < len(TABS) - 1:
            st.button(
                "➡️",
                key=f"fwd_{tab}_{tid}",
                on_click=callbacks.move_card,
                args=(tab, tid, st.session_state.get(f"edit_{tid}", ""), "forward"),
                use_container_width=True,
                help=f"Move to {TABS[tab_index + 1]}",
            )
    
    # Delete button
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
    """Render a new-task placeholder that auto-saves on change."""
    tab_index = TABS.index(tab)
    
    st.markdown('<div class="task-card placeholder">', unsafe_allow_html=True)
    
    # Text area for content
    st.text_area(
        label="",
        key=f"new_box_{tab}_{box_id}",
        placeholder="Enter new task…",
        height=calc_height(""),
        on_change=callbacks.add_new_confirm,
        args=(tab, box_id),
        label_visibility="collapsed",
    )
    
    # Action buttons row
    cols = st.columns([1, 1, 2])
    
    # Move backward button
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
    
    # Move forward button
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
    
    # Delete placeholder
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
    # Create columns for board layout
    cols = st.columns(len(TABS))
    
    for col, tab in zip(cols, TABS):
        with col:
            # Column header
            st.markdown(f"<div class='column-header'>{tab}</div>", unsafe_allow_html=True)
            
            # Column container with scrolling
            with st.container():
                # 1) Existing cards
                cards = handle.fetch_tasks_by_tab(tab)
                for tid, content in cards:
                    render_existing_card(tab, tid, content)

                # 2) Placeholder cards
                boxes = st.session_state.get(f"new_boxes_{tab}", [])
                for box_id in boxes:
                    render_placeholder(tab, box_id)

                # 3) "➕ Add New" button (up to 20 total)
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
