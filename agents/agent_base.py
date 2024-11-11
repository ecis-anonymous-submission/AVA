'''
🌐 AgentBase Class for Interactive Financial Advisory App
---------------------------------------------------------
Technical Overview:
This is the foundational class for all agents in the advisory app’s pipeline. It manages the configuration and
setup of agents by handling model loading and serves as a template for mandate retrieval and input processing.
The class is designed to be subclassed, with specific mandates and processing behaviors defined by each agent 
subclass. The load_model method initializes the LLM model, while get_mandate and process_input methods act as 
placeholders for subclass-specific implementations.

In Simple Terms:
AgentBase is like a blueprint for agents in the app! It helps each agent get ready by loading the right model
and leaves room for each agent to specify its own rules (mandates) and actions. Think of it as a starter kit 
for agents to be easily added to the app with unique capabilities.

Attributes:
- model_name: The name of the LLM model each agent will use.
- api_key: Access key for LLM model requests.
- prompter: Instance of the loaded model to manage interactions with user inputs.

Methods:
- __init__: Initializes model configuration.
- load_model: Loads the chosen model using LLMWare’s API.
- get_mandate: Placeholder for mandate retrieval (to be defined by each agent).
- process_input: Placeholder for input processing (to be defined by each agent).
'''

class AgentBase:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key
        self.prompter = None
        self.load_model()

    def load_model(self):
        from llmware.prompts import Prompt
        self.prompter = Prompt().load_model(self.model_name, api_key=self.api_key)

    def get_mandate(self):
        raise NotImplementedError("Subclasses must implement get_mandate method.")

    def process_input(self, input_text):
        raise NotImplementedError("Subclasses must implement process_input method.")
