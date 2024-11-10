'''
⚙️ Config Class - Configuration Setup for Interactive Financial Advisory App
--------------------------------------------------------------------------
Technical Overview:
The Config class centralizes setup configurations for the advisory app, managing key settings for 
database and vector storage. This setup method imports configuration modules from the LLMWare 
library, specifically configuring the active database to SQLite for local storage and enabling Milvus Lite, 
a lightweight vector database optimized for smaller datasets. These configurations are foundational for 
storing and retrieving data efficiently within the app’s agentic pipeline, supporting both structured and 
vector-based data management.

In Simple Terms:
The Config class is like the app's settings hub. It sets up the main storage (SQLite) and enables a 
specialized storage (Milvus Lite) for handling certain types of data. This makes the app ready to store 
and quickly access information, so all the agents can work efficiently.

Attributes:
- None specific to this class; the setup method handles external configurations.

Methods:
- setup: Configures the active database and enables Milvus Lite, setting up storage systems to manage 
  the app’s data requirements effectively.
'''

class Config:
    def setup(self):
        from llmware.configs import LLMWareConfig, MilvusConfig
        # Configuration
        LLMWareConfig().set_active_db("sqlite")
        MilvusConfig().set_config("lite", True)  # Enable Milvus Lite
