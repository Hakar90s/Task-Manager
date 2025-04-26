import streamlit as st
from streamlit_sortables import sort_items
import handle

st.set_page_config(page_title="🗂️ Task Manager Pro", layout="wide")

# --- Custom CSS (header + cards) ---
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
  padding: 8px 32px 8px 8px;  /* extra right padding for icons */
  margin-bottom: 8px;
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
  top: 6px;
  right: 6px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.icon-move {
  right: 30px;  /* move icon just left of delete */
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

TABS = ["Tasks", "In Progress", "Done", "Brainstorm"]


# --- 1) DRAG & DROP SETUP ---
# Build initial containers from the DB
original_positions = {}
containers = []
for tab in TABS:
    ids = []
    for tid, _ in handle.fetch_tasks_by_tab(tab):
        ids.append(str(tid))
        original_positions[str(tid)] = tab
    containers.append({"header": tab, "items": ids})

# Let user drag between columns
sorted_containers = sort_items(
    containers,
    multi_containers=True,
    key="kanban-board"
)

# Persist moves back to the DB
for cont in sorted_containers:
    new_tab = cont["header"]
    for tid in cont["items"]:
        if original_positions.get(tid) != new_tab:
            handle.move_task(int(tid), new_tab)
            original_positions[tid] = new_tab
# no manual rerun needed—Streamlit auto-refreshes on drag end


st.markdown("---")


# --- 2) RENDER ALL COLUMNS WITH AUTO-SAVE & ICONS ---
cols = st.columns(len(TABS))
for col, tab in zip(cols, TABS):
    with col:
        st.subheader(tab)

        # EXISTING TASKS
        for pos, (tid, content) in enumerate(handle.fetch_tasks_by_tab(tab), start=1):
            # adjust height to content
            lines = content.count("\n") + 1
            height = max(80, min(lines * 24, 300))

            # card wrapper
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            # auto-saving textarea
            def make_autosave(tid):
                return lambda: handle.update_task(tid, st.session_state[f"edit_{tid}"])

            st.text_area(
                label=None,
                value=content,
                key=f"edit_{tid}",
                height=height,
                on_change=make_autosave(tid),
                label_visibility="collapsed"
            )

            # move icon (just a visual hint; actual move is via drag)
            st.markdown(f"""
              <button class="icon-btn icon-move" title="Drag to move">⬍</button>
            """, unsafe_allow_html=True)

            # delete icon
            if st.button("❌", key=f"del_{tid}", on_click=lambda t=tid: handle.delete_task(t)):
                pass

            st.markdown('</div>', unsafe_allow_html=True)

        # NEW PLACEHOLDERS
        if f"new_boxes_{tab}" not in st.session_state:
            st.session_state[f"new_boxes_{tab}"] = []

        # Add New
        st.button(
            "➕ Add New",
            key=f"add_new_{tab}",
            on_click=lambda t=tab: st.session_state[f"new_boxes_{t}"].append("")
        )

        # render each placeholder
        boxes = st.session_state[f"new_boxes_{tab}"]
        for idx, val in enumerate(boxes):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)

            def make_new_save(tab, i):
                return lambda: (
                    handle.add_task(st.session_state[f"new_{tab}_{i}"].strip(), tab)
                    if st.session_state[f"new_{tab}_{i}"].strip() else None,
                    boxes.pop(i)
                )

            def make_new_del(tab, i):
                return lambda: boxes.pop(i)

            st.text_area(
                label=None,
                value=val,
                key=f"new_{tab}_{idx}",
                height=80,
                label_visibility="collapsed"
            )
            st.button("💾", key=f"new_save_{tab}_{idx}", on_click=make_new_save(tab, idx))
            st.button("❌", key=f"new_del_{tab}_{idx}", on_click=make_new_del(tab, idx))

            st.markdown('</div>', unsafe_allow_html=True)
