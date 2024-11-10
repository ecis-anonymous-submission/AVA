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
