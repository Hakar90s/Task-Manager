# style.py

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
    .header-bar h1 { color: #ecf0f1; margin: 0; }
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
      font-size: 16px;
      position: absolute;
      top: 8px;
    }
    .icon-move { right: 32px; }
    .icon-delete { right: 8px; }
    .add-new-btn { margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)
