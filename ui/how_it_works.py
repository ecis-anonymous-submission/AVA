# ui/how_it_works.py

import streamlit as st

def display_how_it_works():
    """
    Displays the 'How It Works' section using a Streamlit expander.
    """
    with st.expander("💡 How It Works", expanded=False):
        st.markdown(
            """
            **Instructions to Use AVA:**

            To use AVA, you'll need API credits for OpenAI or Anthropic.

            **Steps to Get Started:**
            1. Obtain API keys for [OpenAI](https://platform.openai.com/docs/overview) or [Anthropic](https://www.anthropic.com/api).
            2. Enter your funded API keys into the input fields below. 
            3. Select your desired models for each agent.
            4. Start interacting with AVA for investment insights.

            **Roles of Agents in AVA:**

            - 🤖 **Agent Zero (Conversation Agent):** Your main point of interaction.
            - 🤖 **Agent One (Evaluation Agent):** Processes your input and classifies it.
            - 🤖 **Agent Two (Risk Profiling Agent):** Creates a detailed risk profile.

            Please note, you will need to explicitly ask for investment advice to trigger a recommendation.

            """
        )
