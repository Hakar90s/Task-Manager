import streamlit as st
import handle

st.set_page_config(page_title="🗂️ Task Manager Pro", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.header-bar {
  background-color: #2c3e50;
  padding: 1rem;
  border-radius: 0 0 10px 10px;
  margin-bottom: 1rem;
}
.header-bar h1 {
  color: #ecf0f1;
  margin: 0;
}
.task-card {
  background: #fff;
  border: 1px solid #e1e1e1;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 12px;
  position: relative;
}
.task-card textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: vertical;
}
.icon-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.icon-move {
  right: 32px;  /* shift left of delete */
}
.add-new-btn {
  margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

TABS = ["Tasks", "In Progress", "Done", "Brainstorm"]

# --- AUTO-SAVE CALLBACK ---
def auto_save(tid):
    handle.update_task(tid, st.session_state[f"edit_{tid}"])

# --- MOVE CALLBACK ---
def move_task(tid, new_tab):
    handle.move_task(tid, new_tab)

# --- DELETE CALLBACK ---
def delete_task(tid):
    handle.delete_task(tid)

# --- ADD NEW CALLBACK ---
def add_placeholder(tab):
    st.session_state.setdefault(f"new_boxes_{tab}", []).append("")

# --- SAVE NEW CALLBACK ---
def save_new(tab, idx):
    key = f"new_{tab}_{idx}"
    text = st.session_state.get(key, "").strip()
    if text:
        handle.add_task(text, tab)
    st.session_state[f"new_boxes_{tab}"].pop(idx)

# --- DELETE PLACEHOLDER CALLBACK ---
def delete_new(tab, idx):
    st.session_state[f"new_boxes_{tab}"].pop(idx)

# Initialize new-box lists
for tab in TABS:
    st.session_state.setdefault(f"new_boxes_{tab}", [])

# Render columns
cols = st.columns(len(TABS))
for col, tab in zip(cols, TABS):
    with col:
        st.subheader(tab)

        # --- EXISTING TASK CARDS ---
        for _, (tid, content) in enumerate(handle.fetch_tasks_by_tab(tab), start=1):
            # compute height
            lines = content.count("\n") + 1
            height = max(80, min(lines * 24, 300))

            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            # auto-saving textarea
            st.text_area(
                label="",
                value=content,
                key=f"edit_{tid}",
                height=height,
                on_change=auto_save,
                args=(tid,),
                label_visibility="collapsed"
            )

            # Move arrow icon
            st.markdown(f"""
              <button class="icon-btn icon-move" title="Move">
                ➡️
              </button>
            """, unsafe_allow_html=True)
            # We still need a real Select + callback behind it:
            new_tab = st.selectbox(
                "", options=[t for t in TABS if t != tab],
                key=f"move_sel_{tid}"
            )
            if st.button(" ", key=f"move_btn_{tid}", on_click=move_task, args=(tid, new_tab)):
                pass

            # Delete icon
            if st.button("❌", key=f"del_{tid}", on_click=delete_task, args=(tid,)):
                pass

            st.markdown('</div>', unsafe_allow_html=True)

        # --- ADD NEW PLACEHOLDERS ---
        st.button(
            "➕ Add New",
            key=f"add_new_{tab}",
            on_click=add_placeholder,
            args=(tab,),
            help="Create a new card"
        )

        # Render each new-box
        for idx, _ in enumerate(st.session_state[f"new_boxes_{tab}"]):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            # input
            st.text_area(
                label="",
                value="",
                key=f"new_{tab}_{idx}",
                height=80,
                label_visibility="collapsed"
            )

            # save on typing away (you don't need a button)
            if st.session_state.get(f"new_{tab}_{idx}", ""):
                save_new(tab, idx)

            # delete placeholder
            if st.button("❌", key=f"new_del_{tab}_{idx}", on_click=delete_new, args=(tab, idx)):
                pass

            st.markdown('</div>', unsafe_allow_html=True)
