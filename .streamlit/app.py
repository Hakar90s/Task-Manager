import streamlit as st
import handle

st.set_page_config(page_title="Task Manager Pro", layout="wide")

# CSS for header and cards
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
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 12px;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar"><h1>🗂️ Task Manager Pro</h1></div>', unsafe_allow_html=True)

TABS = ["Tasks", "In Progress", "Done", "Brainstorm"]

# Callback functions
def save_existing(task_id):
    text = st.session_state[f"edit_{task_id}"].strip()
    handle.update_task(task_id, text)

def move_existing(task_id):
    new_tab = st.session_state[f"move_to_{task_id}"]
    handle.move_task(task_id, new_tab)

def delete_existing(task_id):
    handle.delete_task(task_id)

def add_new_box(tab):
    key = f"new_boxes_{tab}"
    if len(st.session_state[key]) < 20:
        st.session_state[key].append("")

def save_new(tab, idx):
    input_key = f"new_{tab}_{idx}"
    text = st.session_state[input_key].strip()
    if text:
        handle.add_task(text, tab)
    st.session_state[f"new_boxes_{tab}"].pop(idx)

def delete_new(tab, idx):
    st.session_state[f"new_boxes_{tab}"].pop(idx)

# Initialize new-box placeholders
for tab in TABS:
    key = f"new_boxes_{tab}"
    if key not in st.session_state:
        st.session_state[key] = []

panels = st.tabs(TABS)

for ti, tab in enumerate(TABS):
    with panels[ti]:
        st.subheader(tab)

        # Existing tasks
        tasks = handle.fetch_tasks_by_tab(tab)
        for pos, (tid, content) in enumerate(tasks, start=1):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns([4,1,1,1,1])

            c1.text_input(f"Task {pos}", value=content, key=f"edit_{tid}")
            c2.button("💾", key=f"save_{tid}", on_click=save_existing, args=(tid,))
            c3.selectbox("", options=[t for t in TABS if t != tab], key=f"move_to_{tid}")
            c4.button("➡️", key=f"move_{tid}", on_click=move_existing, args=(tid,))
            c5.button("🗑️", key=f"del_{tid}", on_click=delete_existing, args=(tid,))
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # New-box placeholders
        key = f"new_boxes_{tab}"
        boxes = st.session_state[key]

        c_add, _ = st.columns([1,3])
        c_add.button("➕ Add New", key=f"add_new_{tab}", on_click=add_new_box, args=(tab,))

        for idx in range(len(boxes)):
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            b1, b2, b3 = st.columns([4,1,1])
            input_key = f"new_{tab}_{idx}"
            b1.text_input(f"New #{idx+1}", value=boxes[idx], key=input_key)
            b2.button("💾", key=f"new_save_{tab}_{idx}", on_click=save_new, args=(tab, idx))
            b3.button("🗑️", key=f"new_del_{tab}_{idx}", on_click=delete_new, args=(tab, idx))
            st.markdown('</div>', unsafe_allow_html=True)
