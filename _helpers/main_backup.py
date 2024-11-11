"""
This is the main entry point of the AVA application. It sets up the Streamlit app and orchestrates the interaction between the user and the various agents in the RAG pipeline. Specifically, it:

- Initializes the Streamlit interface, including API key input and model selection for each agent.
- Sets up configuration using the Singleton pattern from `configs.config`.
- Instantiates the agents (`AgentZero`, `AgentOne`, `AgentTwo`) and utility managers (`ConversationManager`, `ResearchManager`, `RiskProfileManager`).
- Manages conversation history and session state using `st.session_state`.
- Processes user inputs and directs them through the appropriate agents using the Chain of Responsibility pattern.
- Ensures seamless interaction between the user interface and the backend logic.
"""

import os
import streamlit as st

from configs.config import Config
from agents.agent_zero import AgentZero
from agents.agent_one import AgentOne
from agents.agent_two import AgentTwo
from utils.conversation_utils import ConversationManager
from utils.research_utils import ResearchManager
from utils.risk_profile_utils import RiskProfileManager

# Set up the Streamlit app
st.title("AVA 1.0 - An Agentic RAG Artifact for LLM Investment Advice")

# Set up the OpenAI API key input
api_key = st.text_input("Enter your OpenAI API key", type='password')

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

if api_key:
    st.session_state['api_key'] = api_key
    os.environ["USER_MANAGED_OPENAI_API_KEY"] = api_key  # Set the environment variable

# Check if the API key is set
if st.session_state['api_key'] is None:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Model options
model_options = ['gpt-4', 'gpt-3.5-turbo']

# Dropdown for Agent Zero model selection
agent_zero_model = st.selectbox("Choose the model for conversation agent (Agent Zero):", model_options)
st.session_state['agent_zero_model'] = agent_zero_model

# Dropdown for Agent One model selection
agent_one_model = st.selectbox("Choose the model for the evaluation agent (Agent One):", model_options)
st.session_state['agent_one_model'] = agent_one_model

# Dropdown for Agent Two model selection
agent_two_model = st.selectbox("Choose the model for risk profiling agent (Agent Two):", model_options)
st.session_state['agent_two_model'] = agent_two_model

# Configuration
config = Config()
config.setup()

# Initialize agents
agent_zero = AgentZero(st.session_state['agent_zero_model'], st.session_state['api_key'])
agent_one = AgentOne(st.session_state['agent_one_model'], st.session_state['api_key'])
agent_two = AgentTwo(st.session_state['agent_two_model'], st.session_state['api_key'])

# Initialize managers
conversation_manager = ConversationManager()
research_manager = ResearchManager()
risk_profile_manager = RiskProfileManager()

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    st.session_state['messages'].append({"role": "assistant", "content": "Hi, how can I help you today?"})

# Initialize conversation history for Agent Two
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Initialize risk profile report
if 'risk_profile_report' not in st.session_state:
    st.session_state['risk_profile_report'] = None

# Display conversation history
for message in st.session_state['messages']:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(message['content'])
    else:
        with st.chat_message("assistant"):
            st.markdown(message['content'])

# Input text box for the user
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    # Process the user input
    def process_user_input(user_input):
        # Agent One evaluates the user input
        evaluation_response = agent_one.evaluate_input(user_input)
        st.write(f"**Evaluation Report from Agent One:**\n{evaluation_response}")

        # Append Agent One's evaluation to conversation history
        st.session_state['conversation_history'].append({"role": "agent_one", "content": evaluation_response})

        # Check evaluation response
        if "'Y'" in evaluation_response:
            # The user is requesting investment advice
            with st.spinner('Generating detailed report...'):
                research_summary = research_manager.generate_research_summary()
                st.write(research_summary)
                report_summary_text = research_manager.summarize_report(research_summary)
            assistant_response = conversation_manager.conversation(user_input, agent_zero, report_summary=report_summary_text)
            return assistant_response
        elif "'R'" in evaluation_response:
            # The user is answering a risk profile question
            risk_profile_report = risk_profile_manager.generate_risk_profile(st.session_state['conversation_history'])
            st.session_state['risk_profile_report'] = risk_profile_report
            st.write(f"**Risk Profile Report from Agent Two:**\n{risk_profile_report}")
            st.session_state['conversation_history'].append({"role": "agent_two", "content": risk_profile_report})
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response
        else:
            # Continue interaction with Agent Zero via conversation
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response

    # Process the user input
    process_user_input(user_input)
