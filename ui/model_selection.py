# ui/model_selection.py

import streamlit as st

def model_selection(gpt_models, claude_models):
    """
    Displays model selection dropdowns for each agent and stores the selections in session state.

    Args:
        gpt_models (list): List of GPT model names.
        claude_models (list): List of Claude model names.

    Returns:
        dict: A dictionary with selected models for each agent.
    """
    all_models = gpt_models + claude_models

    # Dropdown for Agent Zero model selection
    agent_zero_model = st.selectbox("Choose the model for conversation agent (Agent Zero):", all_models)
    st.session_state['agent_zero_model'] = agent_zero_model

    # Dropdown for Agent One model selection
    agent_one_model = st.selectbox("Choose the model for the evaluation agent (Agent One):", all_models)
    st.session_state['agent_one_model'] = agent_one_model

    # Dropdown for Agent Two model selection
    agent_two_model = st.selectbox("Choose the model for risk profiling agent (Agent Two):", all_models)
    st.session_state['agent_two_model'] = agent_two_model

    return {
        'agent_zero': agent_zero_model,
        'agent_one': agent_one_model,
        'agent_two': agent_two_model
    }
