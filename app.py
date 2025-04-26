import streamlit as st
from streamlit_sortables import sort_items
import handle

st.set_page_config(page_title="🗂️ Task Manager Pro", layout="wide")

# --- Custom Header ---
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
  padding: 8px;
  margin-bottom: 8px;
  position: relative;
}
.task-card textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: vertical;
}
.task-card .icon-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

TABS = ["Tasks", "In Progress", "Done", "Brainstorm"]

# === 1) DRAG & DROP DETECTION ===
# Build initial containers
original_tab = {}
containers = []
for tab in TABS:
    items = []
    for tid, _ in handle.fetch_tasks_by_tab(tab):
        items.append(str(tid))
        original_tab[str(tid)] = tab
    containers.append({"header": tab, "items": items})

# Let user drag between columns
sorted_containers = sort_items(
    containers,
    multi_containers=True,
    key="kanban-board"
)

# Detect moved tasks
for cont in sorted_containers:
    new_tab = cont["header"]
    for tid in cont["items"]:
        if original_tab.get(tid) != new_tab:
            handle.move_task(int(tid), new_tab)
            st.experimental_rerun()

st.markdown("---")

# === 2) SHOW ALL COLUMNS WITH AUTO-SAVING TEXTAREAS & ICONS ===
cols = st.columns(len(TABS))
for col, tab in zip(cols, TABS):
    with col:
        st.subheader(tab)

        # existing tasks
        for pos, (tid, content) in enumerate(handle.fetch_tasks_by_tab(tab), start=1):
            # dynamic height
            lines = content.count("\n") + 1
            height = max(80, min(lines * 24, 300))

            # wrap in a card
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            # auto-saving textarea
            # callback factory
            def make_save_cb(tid):
                return lambda: handle.update_task(tid, st.session_state[f"edit_{tid}"])

            st.text_area(
                label=None,
                value=content,
                key=f"edit_{tid}",
                height=height,
                on_change=make_save_cb(tid)
            )

            # delete icon
            if st.button("❌", key=f"del_{tid}", on_click=lambda t=tid: handle.delete_task(t) or st.experimental_rerun()):
                pass

            st.markdown('</div>', unsafe_allow_html=True)

        # new placeholders
        if f"new_boxes_{tab}" not in st.session_state:
            st.session_state[f"new_boxes_{tab}"] = []

        # Add New button
        if st.button("➕ Add New", key=f"add_new_{tab}"):
            if len(st.session_state[f"new_boxes_{tab}"]) < 20:
                st.session_state[f"new_boxes_{tab}"].append("")
                st.experimental_rerun()

        # render placeholders
        for idx, val in enumerate(st.session_state[f"new_boxes_{tab}"]):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            # callback factory for saving new
            def make_new_save_cb(tab, i):
                return lambda: (
                    handle.add_task(st.session_state[f"new_{tab}_{i}"].strip(), tab)
                    if st.session_state[f"new_{tab}_{i}"].strip() else None,
                    st.session_state[f"new_boxes_{tab}"].pop(i),
                    st.experimental_rerun()
                )

            st.text_area(
                label=None,
                value=val,
                key=f"new_{tab}_{idx}",
                height=80
            )

            # delete placeholder
            if st.button("❌", key=f"new_del_{tab}_{idx}", on_click=lambda t=tab, i=idx: st.session_state[f"new_boxes_{t}"].pop(i) or st.experimental_rerun()):
                pass

            # save placeholder
            if st.button("💾", key=f"new_save_{tab}_{idx}", on_click=make_new_save_cb(tab, idx)):
                pass

            st.markdown('</div>', unsafe_allow_html=True)
