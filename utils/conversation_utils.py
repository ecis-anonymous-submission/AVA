'''
💬 ConversationManager Class - Conversation Handling for Advisory App
---------------------------------------------------------------------
Technical Overview:
The ConversationManager class manages the flow of dialogue between the user and AgentZero. It combines 
user input, optional report summaries, and risk profile reports to generate a coherent assistant response. 
The conversation method retrieves the latest risk profile report, if available, and passes relevant context 
to AgentZero to generate a response. The response is then cleaned, stored in session state, and displayed 
on the interface, ensuring continuity and consistency in user interactions. This class helps centralize 
dialogue management, facilitating clear communication within the app.

In Simple Terms:
The ConversationManager is like the chat handler. It takes what the user says, combines it with any extra 
information like risk reports, and gets a response from AgentZero. This response is cleaned up, saved to 
the chat history, and shown to the user, making sure the conversation feels smooth and on-topic.

Attributes:
- None specific to this class; it relies on session state for data storage.

Methods:
- conversation: Manages the chat flow by combining user input, reports, and agent responses, cleaning 
  the output, and saving it to the chat history for seamless interaction.
'''

import re
import streamlit as st

class ConversationManager:
    def conversation(self, user_input, agent_zero, report_summary=None):
        # Get risk profile report if available
        risk_profile_report = st.session_state.get('risk_profile_report', None)
        
        # Generate assistant response
        assistant_response = agent_zero.generate_response(user_input, report_summary, risk_profile_report)
        
        # Clean up the response
        assistant_response = re.sub("[\n\n]", "\n", assistant_response).strip()
        st.session_state['messages'].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Append Agent Zero's response to conversation history
        st.session_state['conversation_history'].append({"role": "assistant", "content": assistant_response})

        return assistant_response
