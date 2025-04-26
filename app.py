import streamlit as st
from streamlit_sortables import sort_items
import handle

st.set_page_config(page_title="Task Manager Pro", layout="wide")

# --- CALLBACKS ---
def auto_save(task_id):
    # called on every text_area change
    new_text = st.session_state[f"edit_{task_id}"]
    handle.update_task(task_id, new_text)

def delete_existing(task_id):
    handle.delete_task(task_id)

# --- CONSTANTS ---
TABS = ["Tasks", "In Progress", "Done", "Brainstorm"]

# --- 0) DRAG-N-DROP BAR ---
# Build containers for Sortables
original_tab = {}
containers = []
for tab in TABS:
    items = []
    rows = handle.fetch_tasks_by_tab(tab)
    for tid, content in rows:
        # prefix each item with its id so we can parse it back
        items.append(f"{tid}¶{content}")
        original_tab[str(tid)] = tab
    containers.append({"header": tab, "items": items})

# Let users drag between containers
sorted_containers = sort_items(
    containers,
    multi_containers=True,
    key="kanban",
    custom_style="""
    .sortable-component { display: flex; gap: 1rem; }
    .sortable-container { background: #f7f7f7; border-radius: 8px; padding: 8px; width: 100%; }
    .sortable-container-header { font-weight: bold; margin-bottom: 0.5rem; }
    .sortable-item { border: 1px solid #ddd; border-radius: 4px; padding: 6px; background: #fff; margin-bottom: 4px; cursor: grab; }
    """
)

# Process any moves
for container in sorted_containers:
    new_tab = container["header"]
    for item in container["items"]:
        tid, _ = item.split("¶", 1)
        if original_tab.get(tid) != new_tab:
            handle.move_task(int(tid), new_tab)
            original_tab[tid] = new_tab

st.markdown("---")

# --- 1) SHOW ALL TABS SIDE-BY-SIDE WITH TEXT_AREAS AND DELETE ICONS ---
cols = st.columns(len(TABS))
for col, tab in zip(cols, TABS):
    with col:
        st.subheader(tab)
        rows = handle.fetch_tasks_by_tab(tab)
        for pos, (tid, content) in enumerate(rows, start=1):
            # calculate a height based on number of lines (min 80, max 300)
            lines = content.count("\n") + 1
            height = max(80, min(lines * 24, 300))

            # render as a “card”
            st.markdown(
                f"""
                <div style="
                  background:#fff; 
                  border:1px solid #e1e1e1; 
                  border-radius:6px; 
                  padding:8px; 
                  margin-bottom:8px;
                  box-shadow:1px 1px 4px rgba(0,0,0,0.05);
                  position: relative;
                ">
                  <div style="position:absolute; top:8px; right:8px;">
                    <button id="del_{tid}" 
                      style="background:none;border:none;cursor:pointer;font-size:16px;"
                      onclick="document.dispatchEvent(new CustomEvent('delete_{tid}'))"
                    >❌</button>
                  </div>
                  <textarea 
                    id="edit_{tid}" 
                    style="width:100%; height:{height}px; border:none; outline:none; resize: vertical;"
                  >{content}</textarea>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Wire up the delete and auto-save listeners
            st.session_state.setdefault("listeners", {})
            # delete
            if f"delete_{tid}" not in st.session_state["listeners"]:
                def make_del_callback(_tid=tid):
                    delete_existing(_tid)
                st.session_state["listeners"][f"delete_{tid}"] = make_del_callback
                # js binding
                st.markdown(f"""
                <script>
                  document.addEventListener('delete_{tid}', () => {{
                    window.dispatchEvent(new CustomEvent('streamlit:runScript'));
                  }});
                </script>
                """, unsafe_allow_html=True)

            # auto-save on blur (when textarea loses focus)
            if f"edit_{tid}" not in st.session_state["listeners"]:
                def make_save_callback(_tid=tid):
                    auto_save(_tid)
                st.session_state["listeners"][f"edit_{tid}"] = make_save_callback
                st.text_area(
                    "", 
                    value=content, 
                    key=f"edit_{tid}", 
                    height=height,
                    on_change=auto_save,
                    args=(tid,),
                    label_visibility="collapsed"
                )
