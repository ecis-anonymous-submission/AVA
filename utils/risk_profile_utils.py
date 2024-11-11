'''
📈 RiskProfileManager Class - Risk Profile Generation for Advisory App
----------------------------------------------------------------------
Technical Overview:
The RiskProfileManager class manages the generation of user-specific risk profiles within the advisory 
app. It utilizes AgentTwo to analyze conversation history and produce a detailed report reflecting the 
user’s risk tolerance and financial disposition. The generate_risk_profile method initiates AgentTwo 
with the appropriate model and API key, leveraging conversation data to create a comprehensive risk 
profile report. This report helps tailor investment advice to each user's unique risk appetite.

In Simple Terms:
The RiskProfileManager is like the app’s risk analyst. It takes what the user has shared in the 
conversation and asks AgentTwo to create a report that shows how much financial risk the user is 
comfortable with. This report is used to give advice that matches the user’s risk preferences.

Attributes:
- None specific to this class; it relies on session state for agent configuration.

Methods:
- generate_risk_profile: Initiates AgentTwo to create a risk profile based on conversation history, 
  helping the app customize advice according to user-specific risk tolerance.
'''

import streamlit as st
# Remove unnecessary import
# from agents.agent_two import AgentTwo

class RiskProfileManager:
    def generate_risk_profile(self, conversation_history, agent_two):
        risk_profile_report = agent_two.generate_risk_profile(conversation_history)
        return risk_profile_report

