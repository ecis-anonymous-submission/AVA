'''
🌐 AgentTwo Class - Risk Profiling Agent for Interactive Financial Advisory App
------------------------------------------------------------------------------
Technical Overview:
AgentTwo functions as a risk profiling agent within the advisory app's agentic pipeline. It is responsible 
for analyzing the user’s conversation history and generating a detailed risk profile report. This agent 
retrieves a predefined mandate from an external text file, guiding its interpretation of the user’s 
interaction history. By combining the mandate with the conversation details, AgentTwo produces a 
comprehensive risk profile, enabling the app to provide personalized investment advice based on the 
user's risk tolerance and financial goals. This profiling step is crucial for tailoring advice to individual 
client profiles.

In Simple Terms:
AgentTwo is a specialized agent that reads through the user’s conversation and creates a risk profile 
report. This report helps the app understand the user’s comfort with risk, so it can offer advice that fits 
their financial preferences. AgentTwo uses a set of rules (mandate) and the user’s words to make this 
profile, making it a key part of personalizing the advice given.

Attributes:
- Inherits all attributes from AgentBase, including model_name, api_key, and prompter.

Methods:
- get_mandate: Retrieves the agent’s risk profiling criteria from a text file, outlining how to interpret 
  conversation history.
- generate_risk_profile: Combines the mandate with the user’s conversation history, creating a prompt 
  to generate a detailed risk profile report, which informs the app about the user’s risk tolerance.
'''

from .agent_base import AgentBase
import os

class AgentTwo(AgentBase):
    def get_mandate(self):
        with open(os.path.join('prompts', 'agent_two_mandate.txt'), 'r') as f:
            return f.read()

    def generate_risk_profile(self, conversation_history):
        agent_two_mandate = self.get_mandate()

        # Prepare the conversation history as text
        conversation_text = ""
        for message in conversation_history:
            role = message['role']
            content = message['content']
            if role == "user":
                conversation_text += f"User: {content}\n"
            elif role == "assistant":
                conversation_text += f"Assistant: {content}\n"

        # Prepare the input for Agent Two
        risk_profile_input = f"{agent_two_mandate}\n\nConversation:\n{conversation_text}\n\nGenerate the risk profile report."

        # Get the response from Agent Two
        response = self.prompter.prompt_main(risk_profile_input)
        risk_profile_report = response['llm_response'].strip()
        return risk_profile_report

