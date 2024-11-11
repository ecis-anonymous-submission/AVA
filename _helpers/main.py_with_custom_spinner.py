"""
This is the main entry point of the AVA application. It sets up the Streamlit app and orchestrates the interaction between the user and the various agents in the RAG pipeline. Specifically, it:

- Initializes the Streamlit interface, including API key input and model selection for each agent.
- Sets up configuration using the Singleton pattern from `configs.config`.
- Instantiates the agents (`AgentZero`, `AgentOne`, `AgentTwo`) and utility managers (`ConversationManager`, `ResearchManager`, `RiskProfileManager`).
- Manages conversation history and session state using `st.session_state`.
- Processes user inputs and directs them through the appropriate agents using the Chain of Responsibility pattern.
- Ensures seamless interaction between the user interface and the backend logic.

**Updates:**

- Enhanced model selection to include both GPT and Claude models.
- Improved UI to request the appropriate API keys based on the selected models.
- Integrated a custom spinner animation for a better user experience.
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

# Embed the custom CSS for the spinner
spinner_css = """
<style>
.spinner {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}

.spinner span {
  position: absolute;
  top: 50%;
  left: var(--left);
  width: 35px;
  height: 7px;
  background: #000;
  animation: dominos 1s ease infinite;
  box-shadow: 2px 2px 3px 0px black;
}

.spinner span:nth-child(1) {
  --left: 80px;
  animation-delay: 0.125s;
}

.spinner span:nth-child(2) {
  --left: 70px;
  animation-delay: 0.3s;
}

.spinner span:nth-child(3) {
  --left: 60px;
  animation-delay: 0.425s;
}

.spinner span:nth-child(4) {
  --left: 50px;
  animation-delay: 0.54s;
}

.spinner span:nth-child(5) {
  --left: 40px;
  animation-delay: 0.665s;
}

.spinner span:nth-child(6) {
  --left: 30px;
  animation-delay: 0.79s;
}

.spinner span:nth-child(7) {
  --left: 20px;
  animation-delay: 0.915s;
}

.spinner span:nth-child(8) {
  --left: 10px;
}

@keyframes dominos {
  50% {
    opacity: 0.7;
  }

  75% {
    transform: rotate(90deg);
  }

  80% {
    opacity: 1;
  }
}
</style>
"""

# Inject CSS into the app
st.markdown(spinner_css, unsafe_allow_html=True)

# Function to display the spinner
def show_spinner():
    spinner_html = """
    <div class="spinner">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    """
    return spinner_html

# Set up the Streamlit app
st.title("AVA 1.0 - An Agentic RAG Artifact for LLM Investment Advice")

# Model options for GPT and Claude
gpt_models = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4o'
]

claude_models = [
    'claude-3-opus-20240229',
    'claude-3-sonnet-20240229'
]

all_models = gpt_models + claude_models

# Initialize session state for API keys
if 'api_keys' not in st.session_state:
    st.session_state['api_keys'] = {}

# Dropdown for Agent Zero model selection
agent_zero_model = st.selectbox("Choose the model for conversation agent (Agent Zero):", all_models)
st.session_state['agent_zero_model'] = agent_zero_model

# Dropdown for Agent One model selection
agent_one_model = st.selectbox("Choose the model for the evaluation agent (Agent One):", all_models)
st.session_state['agent_one_model'] = agent_one_model

# Dropdown for Agent Two model selection
agent_two_model = st.selectbox("Choose the model for risk profiling agent (Agent Two):", all_models)
st.session_state['agent_two_model'] = agent_two_model

# Determine which API keys are needed based on selected models
selected_models = {
    'agent_zero': agent_zero_model,
    'agent_one': agent_one_model,
    'agent_two': agent_two_model
}

required_api_keys = set()
for model in selected_models.values():
    if model in gpt_models:
        required_api_keys.add('openai')
    if model in claude_models:
        required_api_keys.add('anthropic')

# Prompt for API keys based on required models
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

# Configuration
config = Config()
config.setup()

# Initialize agents with the appropriate API keys
def get_api_key_for_model(model_name):
    if model_name in gpt_models:
        return st.session_state['api_keys']['openai']
    elif model_name in claude_models:
        return st.session_state['api_keys']['anthropic']
    else:
        return None

agent_zero_api_key = get_api_key_for_model(agent_zero_model)
agent_zero = AgentZero(agent_zero_model, agent_zero_api_key)

agent_one_api_key = get_api_key_for_model(agent_one_model)
agent_one = AgentOne(agent_one_model, agent_one_api_key)

agent_two_api_key = get_api_key_for_model(agent_two_model)
agent_two = AgentTwo(agent_two_model, agent_two_api_key)

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
            spinner_placeholder = st.empty()
            with spinner_placeholder.container():
                st.markdown(show_spinner(), unsafe_allow_html=True)
                research_summary = research_manager.generate_research_summary()
                st.write(research_summary)
                report_summary_text = research_manager.summarize_report(
                    research_summary,
                    agent_zero_model,
                    agent_zero_api_key
                )
            spinner_placeholder.empty()
            assistant_response = conversation_manager.conversation(user_input, agent_zero, report_summary=report_summary_text)
            return assistant_response
        elif "'R'" in evaluation_response:
            # The user is answering a risk profile question
            spinner_placeholder = st.empty()
            with spinner_placeholder.container():
                st.markdown(show_spinner(), unsafe_allow_html=True)
                risk_profile_report = risk_profile_manager.generate_risk_profile(
                    st.session_state['conversation_history'],
                    agent_two
                )
                st.session_state['risk_profile_report'] = risk_profile_report
                st.write(f"**Risk Profile Report from Agent Two:**\n{risk_profile_report}")
            spinner_placeholder.empty()
            st.session_state['conversation_history'].append({"role": "agent_two", "content": risk_profile_report})
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response
        else:
            # Continue interaction with Agent Zero via conversation
            assistant_response = conversation_manager.conversation(user_input, agent_zero)
            return assistant_response

    # Process the user input
    process_user_input(user_input)