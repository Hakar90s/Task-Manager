
# style.py
import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* General app styling */
    .stApp {
        background-color: #f9fafc;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(to right, #4776E6, #8E54E9);
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .app-icon {
        font-size: 32px;
        margin-right: 15px;
    }
    
    .header-content h1 {
        color: white;
        font-weight: 600;
        margin: 0;
        font-size: 2rem;
    }
    
    /* Column styling */
    .column-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0 0 15px 0;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
    }
    
    /* Different colors for different columns */
    .stColumn:nth-child(1) .column-header {
        background: #4776E6;
    }
    
    .stColumn:nth-child(2) .column-header {
        background: #FF9966;
    }
    
    .stColumn:nth-child(3) .column-header {
        background: #2ECC71;
    }
    
    .stColumn:nth-child(4) .column-header {
        background: #9B59B6;
    }
    
    /* Task card styling */
    .task-card {
        background: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    .stColumn:nth-child(1) .task-card {
        border-left: 4px solid #4776E6;
    }
    
    .stColumn:nth-child(2) .task-card {
        border-left: 4px solid #FF9966;
    }
    
    .stColumn:nth-child(3) .task-card {
        border-left: 4px solid #2ECC71;
    }
    
    .stColumn:nth-child(4) .task-card {
        border-left: 4px solid #9B59B6;
    }
    
    .task-card:hover {
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .task-card textarea {
        border: none;
        padding: 8px 2px;
        font-size: 0.95rem;
        background: transparent;
        resize: vertical;
        min-height: 60px;
        transition: background 0.2s;
        border-radius: 4px;
    }
    
    .task-card textarea:focus {
        background: #f9f9ff;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Placeholder styling */
    .task-card.placeholder {
        background: #fafbff;
        border-style: dashed;
    }
    
    .task-card.placeholder textarea {
        background: transparent;
    }
    
    .task-card.placeholder textarea:focus {
        background: white;
    }
    
    /* Buttons styling */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
        border: 1px solid rgba(49, 51, 63, 0.2);
        height: 36px;
    }
    
    .stButton button:hover {
        background-color: #f5f5f5;
        border-color: #8E54E9;
        color: #8E54E9;
    }
    
    /* Primary button (Add New) */
    .stButton button[kind="primary"] {
        background-color: #8E54E9;
        color: white;
        border: none;
    }
    
    .stButton button[kind="primary"]:hover {
        background-color: #7a45d8;
        color: white;
    }
    
    /* Move buttons */
    .stColumn:nth-child(1) .stButton button:has(div:contains("➡️")):hover {
        background-color: #ffeee5;
        border-color: #FF9966;
        color: #FF9966;
    }
    
    .stColumn:nth-child(2) .stButton button:has(div:contains("⬅️")):hover {
        background-color: #e5f1ff;
        border-color: #4776E6;
        color: #4776E6;
    }
    
    .stColumn:nth-child(2) .stButton button:has(div:contains("➡️")):hover {
        background-color: #e5fff0;
        border-color: #2ECC71;
        color: #2ECC71;
    }
    
    .stColumn:nth-child(3) .stButton button:has(div:contains("⬅️")):hover {
        background-color: #ffeee5;
        border-color: #FF9966;
        color: #FF9966;
    }
    
    .stColumn:nth-child(3) .stButton button:has(div:contains("➡️")):hover {
        background-color: #f5e5ff;
        border-color: #9B59B6;
        color: #9B59B6;
    }
    
    .stColumn:nth-child(4) .stButton button:has(div:contains("⬅️")):hover {
        background-color: #e5fff0;
        border-color: #2ECC71;
        color: #2ECC71;
    }
    
    /* Delete buttons */
    .stButton button:has(div:contains("🗑️")) {
        background-color: white;
        color: #777;
    }
    
    .stButton button:has(div:contains("🗑️")):hover {
        background-color: #fff5f5;
        border-color: #ff6b6b;
        color: #ff6b6b;
    }
    
    /* Warning message */
    .stAlert {
        padding: 8px;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    
    /* Hide the default Streamlit footer */
    footer {
        visibility: hidden;
    }
    
    /* Custom scrollbar for columns */
    .element-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .element-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .element-container::-webkit-scrollbar-thumb {
        background: #c5c5c5;
        border-radius: 10px;
    }
    
    .element-container::-webkit-scrollbar-thumb:hover {
        background: #a5a5a5;
    }
    
    /* Improve mobile responsiveness */
    @media screen and (max-width: 992px) {
        .header-content h1 {
            font-size: 1.5rem;
        }
        
        .app-icon {
            font-size: 24px;
        }
        
        .column-header {
            font-size: 1rem;
            padding: 8px 5px;
        }
        
        .task-card {
            padding: 8px;
        }
        
        .task-card textarea {
            font-size: 0.9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
