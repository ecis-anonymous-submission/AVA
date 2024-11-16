# ui/session_state.py

import streamlit as st

def initialize_session_state():
    """
    Initializes necessary variables in the session state.
    """
    if 'api_keys' not in st.session_state:
        st.session_state['api_keys'] = {}

    # Add other session state initializations if needed
