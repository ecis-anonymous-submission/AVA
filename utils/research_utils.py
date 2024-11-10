'''
📊 ResearchManager Class - Financial Data Retrieval and Summary Generation for Advisory App
------------------------------------------------------------------------------------------
Technical Overview:
The ResearchManager class is responsible for gathering and summarizing financial data on companies 
to support investment advice within the advisory app. It processes a CSV file of company data, filters 
companies based on financial health (e.g., Piotroski F-Score), and retrieves additional financial metrics 
from Yahoo Finance via the YFinance API. The generate_research_summary method compiles these 
data points into a detailed research summary, while the summarize_report method provides a concise 
overview using an LLM. This setup allows the app to deliver informed, data-driven insights to users.

In Simple Terms:
The ResearchManager is like the app’s financial data researcher. It reads a list of companies, picks the 
strongest ones, and gathers extra details from Yahoo Finance. Then it makes a summary of these details, 
so the app can give users well-researched investment advice without overwhelming them with too much 
information.

Attributes:
- None specific to this class; it relies on session state for configurations and API key.

Methods:
- generate_research_summary: Compiles a comprehensive report on selected companies, including 
  financial metrics and company information from Yahoo Finance.
- summarize_report: Converts the research summary into a concise, user-friendly report using an LLM 
  to ensure clarity and relevance in user interactions.
'''

import os
import streamlit as st
from llmware.resources import CustomTable
from llmware.web_services import YFinance

class ResearchManager:
    def generate_research_summary(self, local_library_path="data"):
        """Processes a CSV of companies and retrieves financial data from Yahoo Finance."""
        # Path to the CSV file
        fp = os.path.join(os.getcwd(), local_library_path)
        fn = "companies.csv"

        # Validate CSV
        analysis = CustomTable().validate_csv(fp, fn, delimiter=',', encoding='utf-8-sig')

        table_name = "companies_table"
        db_name = "sqlite"

        # Initialize the CustomTable object
        ct = CustomTable(db=db_name, table_name=table_name)

        # Load the CSV
        output = ct.load_csv(fp, fn)

        # Insert the rows into the database
        ct.insert_rows()

        # Retrieve companies data from the database
        companies = ct.rows

        # Filter companies with f_score > 8
        filtered_companies = [row for row in companies if float(row.get('f_score', 0)) > 8]

        research_summary = {}

        for row in filtered_companies:
            company_name = row['name']
            ticker = row['ticker']
            f_score = row.get('f_score', 'N/A')
            research_summary[company_name] = {'f_score': f_score}

            # Fetch data from Yahoo Finance
            ticker_core = ticker.split(":")[-1]
            yf = YFinance().get_stock_summary(ticker=ticker_core)
            yf2 = YFinance().get_financial_summary(ticker=ticker_core)
            yf3 = YFinance().get_company_summary(ticker=ticker_core)

            research_summary[company_name].update({
                "current_stock_price": yf.get("currentPrice", "N/A"),
                "high_ltm": yf.get("fiftyTwoWeekHigh", "N/A"),
                "low_ltm": yf.get("fiftyTwoWeekLow", "N/A"),
                "trailing_pe": yf.get("trailingPE", "N/A"),
                "forward_pe": yf.get("forwardPE", "N/A"),
                "volume": yf.get("volume", "N/A"),
                "market_cap": yf2.get("marketCap", "N/A"),
                "price_to_sales": yf2.get("priceToSalesTrailing12Months", "N/A"),
                "revenue_growth": yf2.get("revenueGrowth", "N/A"),
                "ebitda": yf2.get("ebitda", "N/A"),
                "gross_margin": yf2.get("grossMargins", "N/A"),
                "currency": yf2.get("currency", "N/A"),
                "sector": yf3.get("sector", "N/A"),
                "website": yf3.get("website", "N/A"),
                "industry": yf3.get("industry", "N/A"),
                "employees": yf3.get("fullTimeEmployees", "N/A"),
                "officers": [
                    (officer.get("name", "N/A"), officer.get("title", "N/A"), officer.get("age", "N/A"), officer.get("totalPay", "N/A"))
                    for officer in yf3.get("companyOfficers", [])
                ]
            })

        return research_summary

    def summarize_report(self, research_summary):
        # Convert research_summary to text
        report_text = ""
        for company, details in research_summary.items():
            report_text += f"Company: {company}\n"
            for key, value in details.items():
                report_text += f"{key}: {value}\n"
            report_text += "\n"

        # Load the model for summarization
        from llmware.prompts import Prompt
        prompter = Prompt().load_model(st.session_state['agent_zero_model'], api_key=st.session_state['api_key'])

        # Summarize the report
        with st.spinner('Summarizing the report...'):
            summary_prompt = f"Please provide a concise summary of the following research report:\n\n{report_text}"
            response = prompter.prompt_main(summary_prompt)
            report_summary_text = response['llm_response']

        return report_summary_text.strip()
