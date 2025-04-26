# app.py

import streamlit as st
from style import apply_styles
from ui import render_header, render_board
from constants import TABS

st.set_page_config(page_title="🗂️ Task Manager Pro", layout="wide")
apply_styles()
render_header()

# initialize placeholders
for tab in TABS:
    st.session_state.setdefault(f"new_boxes_{tab}", [])

render_board()
