# ui/api_keys.py

import streamlit as st
import os

def prompt_for_api_keys(required_api_keys):
    """
    Prompts the user for necessary API keys based on the selected models.

    Args:
        required_api_keys (set): A set of required API key names ('openai', 'anthropic').
    """
    # Initialize session state for API keys
    if 'api_keys' not in st.session_state:
        st.session_state['api_keys'] = {}

    # Prompt for API keys
    if 'openai' in required_api_keys:
        openai_api_key = st.text_input("Enter your OpenAI API key", type='password')
        if openai_api_key:
            st.session_state['api_keys']['openai'] = openai_api_key
            os.environ["USER_MANAGED_OPENAI_API_KEY"] = openai_api_key  # Set the environment variable

    if 'anthropic' in required_api_keys:
        anthropic_api_key = st.text_input("Enter your Anthropic API key", type='password')
        if anthropic_api_key:
            st.session_state['api_keys']['anthropic'] = anthropic_api_key
            os.environ["USER_MANAGED_ANTHROPIC_API_KEY"] = anthropic_api_key  # Set the environment variable

    # Check if the necessary API keys are set
    missing_keys = [key for key in required_api_keys if key not in st.session_state['api_keys']]
    if missing_keys:
        st.warning(f"Please enter your {', '.join(missing_keys)} API key(s) to continue.")
        st.stop()
