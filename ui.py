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

    # Top row: delete | spacer | move-dropdown + confirm
    c_del, c_spacer, c_move = st.columns([1,6,2], gap="small")
    with c_del:
        st.button("❌", key=f"del_{tid}", on_click=callbacks.delete_task, args=(tid,), use_container_width=True)
    with c_move:
        sel_key = f"move_sel_{tid}"
        st.selectbox("", options=[t for t in TABS if t != tab], key=sel_key, label_visibility="collapsed")
        st.button("🔀", key=f"move_btn_{tid}", on_click=callbacks.move_existing, args=(tid, st.session_state[sel_key]), use_container_width=True)

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
    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Top row: delete | spacer | move-dropdown + confirm
    c_del, c_spacer, c_move = st.columns([1,6,2], gap="small")
    with c_del:
        st.button("❌", key=f"new_del_{tab}_{idx}", on_click=callbacks.delete_new, args=(tab, idx), use_container_width=True)
    with c_move:
        sel_key = f"move_new_sel_{tab}_{idx}"
        st.selectbox("", options=[t for t in TABS if t != tab], key=sel_key, label_visibility="collapsed")
        st.button("🔀", key=f"move_new_btn_{tab}_{idx}", on_click=callbacks.move_new, args=(tab, idx, st.session_state[sel_key]), use_container_width=True)

    st.text_area(
        label="",
        value=st.session_state.get(f"new_{tab}_{idx}", ""),
        key=f"new_{tab}_{idx}",
        height=80,
        on_change=lambda t=tab, i=idx: callbacks.save_new(t, i),
        label_visibility="collapsed",
    )

    st.markdown('</div>', unsafe_allow_html=True)

def render_board():
    cols = st.columns(len(TABS), gap="small")
    for col, tab in zip(cols, TABS):
        with col:
            st.subheader(tab)

            for tid, content in handle.fetch_tasks_by_tab(tab):
                render_existing_card(tab, tid, content)

            st.button("➕ Add New", key=f"add_new_{tab}", on_click=callbacks.add_placeholder, args=(tab,), use_container_width=True)

            for idx, _ in enumerate(st.session_state.get(f"new_boxes_{tab}", [])):
                render_new_card(tab, idx)
