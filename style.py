import streamlit as st

def apply_styles():
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
      background: none;
      border: none;
      cursor: pointer;
      position: absolute;
      top: 8px;
      padding: 0;
    }
    .icon-move {
      right: 32px;
      font-size: 14px;
    }
    .icon-delete {
      right: 8px;
      font-size: 14px;
    }
    /* shrink the move-select dropdown */
    .task-card select {
      width: 60px !important;
      font-size: 14px;
      padding: 2px 4px;
    }
    .add-new-btn {
      margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
