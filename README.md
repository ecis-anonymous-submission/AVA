
📊 AVA 1.1: An Agentic RAG Artifact for LLM Investment Advice 🤖💰

📝 **Introduction**  
AVA 1.1 is an open-source financial advisory app that redefines equity investment guidance by combining multiple Large Language Models (LLMs) with real-time data retrieval, making it a pioneer in the agentic finance space. Using an innovative agent-based architecture within a Retrieval-Augmented Generation (RAG) pipeline, AVA 1.1 offers dynamically informed, ethically sound investment insights that adapt seamlessly to user needs. Crafted to integrate new agents and mandates effortlessly, AVA 1.1 stands out for its modular, scalable design—perfectly suited for researchers, developers, and financial experts aiming to explore agentic AI’s impact on modern investment advisory.

🏛️ **Architecture Overview**  
The app utilizes a multi-agent framework organized using design patterns like Factory Method, Strategy, Singleton, and Chain of Responsibility. The key agents are:

- **Agent Zero (Conversation Agent)** 🤵: Interacts directly with the user, gathers necessary information, and provides investment advice.
- **Agent One (Evaluation Agent)** 📊: Analyzes user inputs to categorize them as general inquiries, risk profile answers, or investment advice requests.
- **Agent Two (Risk Profiling Agent)** 📝: Generates a structured risk profile report based on the conversation history with Agent Zero.

This architecture ensures that each agent has a single responsibility, promoting clean code and easy maintenance. Together, they deliver tailored, accurate advice aligned with your risk tolerance and financial goals. 🎯

🔑 **Key Features**  
- **Modular Structure Harnessing Conventional Design Patterns 🧩**: Implements design patterns for scalability and ease of maintenance.
  - Factory Method: Dynamically creates agents.
  - Strategy Pattern: Encapsulates mandates and algorithms.
  - Singleton Pattern: Manages configuration settings.
  - Chain of Responsibility: Controls the flow between agents.
- **Agent-Based Interaction 🤖**: Simulates a multi-agent environment where each agent has a specific task, enhancing robustness.
- **Retrieval-Augmented Generation (RAG) 🔄**: Integrates real-time data sources like Yahoo Finance for accurate, up-to-date advice.
- **Risk Profiling 📉**: Generates personalized risk profiles to offer advice based on the user’s tolerance and financial situation.
- **User-Friendly Interface 🖥️**: Built with Streamlit, offering an intuitive user experience.

🛠️ **Dependencies**  
- Python 3.7+
- Streamlit
- Pandas
- YFinance
- LLMWare Library
- OpenAI API

🏗️ **Setup Instructions**  
1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/ava-1.1.git
cd ava-1.1
```

2️⃣ **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Set Up OpenAI API Key 🔑**
Obtain an API key from OpenAI. You’ll be prompted to enter it when running the app.

🚀 **Run the Application**
```bash
streamlit run main.py
```

💡 **Usage Instructions**  
- **Launch the App**: Running the command will open the app in a new browser window.
- **Enter API Key**: Input your OpenAI API key in the provided field.
- **Select Models for Agents**: Choose models (e.g., GPT-4, GPT-3.5) for each agent from dropdowns.
- **Start the Conversation**: Type your messages in the chat input box. Agent Zero will guide you through your investment needs.
- **Receive Advice**: Request investment advice, and the app will provide recommendations based on Piotroski F-score analysis. 📊
- **View Risk Profile**: Agent Two generates a risk profile report, viewable in-app.

⚙️ **Underlying Methods**  

**Design Patterns Implemented 🧠**
- **Factory Method Pattern 🏭**: Allows for dynamic creation of agents, facilitating scalability when adding new agents to the system.
- **Strategy Pattern 🎯**: Encapsulates mandates and algorithms within agent classes, promoting interchangeable behaviors.
- **Singleton Pattern 🔒**: Ensures only one instance of the configuration manager exists, maintaining consistent settings across the application.
- **Chain of Responsibility 🔗**: Manages the flow of operations between agents, allowing for flexible pipeline adjustments.

**Agentic Architecture 🤖**  
Each agent has a distinct role:
- **Agent Zero**: User interaction & rapport-building.
- **Agent One**: Input evaluation & routing.
- **Agent Two**: Risk profile generation.

**Retrieval-Augmented Generation (RAG) 🔄**  
- **Data Retrieval**: Yahoo Finance provides real-time financial data using the yfinance library.
- **Data Integration**: The data is merged with the LLM’s responses to give current investment advice.

**Financial Data Processing**  
- **CSV Processing**: Handles a CSV file with company info and Piotroski F-scores.
- **Database Integration**: Uses SQLite for efficient data access.

📂 **Code Structure**
```markdown
project/
├── main.py
├── agents/
│   ├── __init__.py
│   ├── agent_base.py
│   ├── agent_zero.py
│   ├── agent_one.py
│   ├── agent_two.py
│   └── ... (additional agents)
├── prompts/
│   ├── __init__.py
│   ├── agent_zero_mandate.txt
│   ├── agent_one_mandate.txt
│   ├── agent_two_mandate.txt
│   └── ... (additional mandates)
├── utils/
│   ├── __init__.py
│   ├── conversation_utils.py
│   ├── research_utils.py
│   ├── risk_profile_utils.py
│   └── ... (additional utilities)
├── configs/
│   ├── __init__.py
│   └── config.py
├── data/
│   └── companies.csv
└── requirements.txt
```

- **main.py**: Main application script orchestrating agents and managers.
- **agents/**: Contains agent classes, each with a specific responsibility.
- **prompts/**: Stores mandates for each agent in plain text files for easy editing.
- **utils/**: Utility modules for conversation management, research processing, and risk profiling.
- **configs/**: Configuration management using the Singleton pattern.
- **data/companies.csv**: CSV file with company data and Piotroski F-scores.

⚒️ **Customization**
- **Adding New Agents** 🆕: Simply create a new agent class in the agents/ directory, subclassing AgentBase, and add its mandate in the prompts/ directory.
- **Editing Mandates** 📝: Modify the agent mandates directly in the prompts/ directory for quick updates.
- **Adjusting Pipeline Flow** 🔄: Modify main.py to change the sequence of agent interactions, thanks to the Chain of Responsibility pattern.
- **Model Selection** 🎛️: Tailor the models used for each agent to improve performance.

🚧 **Limitations**
- **LLM Dependency**: Quality depends on the language model selected.
- **Data Currency**: There may be delays or inaccuracies in the data retrieved.
- **Scope**: Currently limited to publicly listed equity investments.

⚖️ **Ethical Considerations**
- **Financial Responsibility**: Advice is for informational purposes only—please consult a professional for financial decisions.
- **User Data**: Be cautious about sharing sensitive financial info.

🛠️ **Future Work**
- **Enhanced Risk Profiling**: Incorporate advanced risk models.
- **Expanded Investment Options**: Add support for bonds, ETFs, mutual funds.
- **Regulatory Compliance**: Ensure features comply with financial regulations.
- **Improved Modularity**: Continue refining the architecture for even greater scalability.

🎓 **Conclusion**
AVA 1.1 demonstrates how applying design patterns to an agent-based system within a RAG pipeline can significantly improve scalability and maintainability. It sets a solid foundation for the development of AI-driven financial advisory services in both academic and professional contexts.

🔍 **References**
- **Design Patterns**: Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*.
- **Retrieval-Augmented Generation**: Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
- **Piotroski F-Score**: Piotroski, J.D. (2000). *Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers*.
