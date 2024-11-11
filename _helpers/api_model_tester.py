# _helper/all_model_tester.py

import streamlit as st
from llmware.models import ModelCatalog

def load_all_models():
    """Fetch all available models from the catalog."""
    models = ModelCatalog().list_all_models()
    model_names = [model["model_name"] for model in models]
    return model_names

def all_model_chat_ui():
    st.title("Model Tester")

    # Step 1: Select a Model
    all_models = load_all_models()
    model_name = st.selectbox("Select a Model", all_models)

    # Step 2: Input API Key (if applicable for selected model)
    api_key = st.text_input("Enter API Key (if required)", type="password")

    if model_name:
        # Step 3: Load the Model with optional API Key
        if api_key:
            model = ModelCatalog().load_model(model_name, api_key=api_key)
        else:
            model = ModelCatalog().load_model(model_name)

        # Step 4: Initialize Chat UI
        st.subheader(f"Chat with {model_name}")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        user_input = st.chat_input("Type your message here...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                try:
                    # Model inference
                    model_response = model.inference(user_input)
                    bot_response = model_response["llm_response"]
                    st.markdown(bot_response)
                except Exception as e:
                    st.error("An error occurred with the model: " + str(e))
                    bot_response = "Error: Unable to generate response."

            # Save conversation history
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    all_model_chat_ui()
