
import streamlit as st
from style import apply_styles
from ui import render_header, render_board
from constants import TABS

st.set_page_config(page_title="🗂️ Task Manager Pro", layout="wide")

apply_styles()
render_header()

# initialize placeholder lists
for tab in TABS:
    st.session_state.setdefault(f"new_boxes_{tab}", [])
    
# Initialize selected task state if needed
if "selected_task" not in st.session_state:
    st.session_state.selected_task = None
    
if "show_move_dialog" not in st.session_state:
    st.session_state.show_move_dialog = False

render_board()
