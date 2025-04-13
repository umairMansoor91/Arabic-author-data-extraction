import streamlit as st

def add_rtl_support():
    """Add RTL support for Arabic text in the Streamlit app"""
    st.markdown("""
    <style>
        .stTextArea textarea {
            direction: rtl;
        }
        .css-183lzff {
            direction: rtl;
        }
        
        /* Additional styling for better Arabic text display */
        .arabic-text {
            font-family: 'Amiri', 'Scheherazade New', serif;
            font-size: 18px;
            line-height: 1.5;
            direction: rtl;
            text-align: right;
        }
        
        /* Style for JSON display */
        .json-display {
            direction: ltr;
            text-align: left;
            font-family: monospace;
        }
    </style>
    
    <!-- Add Arabic font support -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri&family=Scheherazade+New&display=swap">
    """, unsafe_allow_html=True)

def create_author_card(author, content, json_data=None):
    """
    Create a styled card for author information
    
    Args:
        author (str): Author identifier
        content (str): Author content text
        json_data (str, optional): JSON structured data if available
    """
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px;">
        <h3>{author}</h3>
        <div class="arabic-text">{content}</div>
        
        {f'<div class="json-display"><pre>{json_data}</pre></div>' if json_data else ''}
    </div>
    """, unsafe_allow_html=True)

def show_error_message(message):
    """Show a styled error message"""
    st.markdown(f"""
    <div style="background-color: #ffebee; color: #c62828; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <strong>Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def show_success_message(message):
    """Show a styled success message"""
    st.markdown(f"""
    <div style="background-color: #e8f5e9; color: #2e7d32; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <strong>Success:</strong> {message}
    </div>
    """, unsafe_allow_html=True)