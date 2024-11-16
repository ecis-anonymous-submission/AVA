import yfinance as yf
import pandas as pd
import os

'''
📊 **Piotroski F-Score Calculation Using Open Source APIs** 📈

The **Piotroski F-score** is a financial metric developed by Joseph Piotroski to evaluate the financial health and 
performance of companies. It uses **9 key criteria** grouped into 3 categories: **profitability**, 
**leverage/liquidity/source of funds**, and **operating efficiency**.

---

### 💡 **Calculation Breakdown:**
1️⃣ **Profitability (4 Points)**:
   - ✅ **Positive Net Income**: Net income > 0.
   - 💵 **Positive Operating Cash Flow**: Operating cash flow > 0.
   - 📈 **Increasing ROA (Return on Assets)**: ROA is higher than the previous year.
   - 🔄 **Operating Cash Flow > Net Income**: Indicates strong cash generation.

2️⃣ **Leverage, Liquidity, and Source of Funds (3 Points)**:
   - 💳 **Decrease in Long-Term Debt**: Long-term debt decreased year-over-year.
   - 🚀 **Increase in Current Ratio**: Current assets to liabilities ratio has improved.
   - 🔒 **No New Shares Issued**: Net issuance of shares is ≤ 0.

3️⃣ **Operating Efficiency (2 Points)**:
   - 📊 **Increase in Gross Margin**: Gross profit margin has improved.
   - 🏭 **Increase in Asset Turnover**: Revenue to total assets ratio has increased.

🔢 **Maximum Score**: 9 points, with higher scores indicating better financial health and performance.

---

### 🔧 **How This Script Works with Open Source APIs:**
This script uses **`yfinance`** to gather the required data:

1. **📥 yfinance**:
   - 📑 **Balance Sheet**: Retrieves `Current Assets`, `Current Liabilities`, and `Long-Term Debt`.
   - 🧾 **Income Statement**: Provides `Net Income`, `Gross Profit`, and `Total Revenue`.
   - 💸 **Cash Flow Statement**: Fetches `Operating Cash Flow` and `Issuance/Repurchase of Stock`.

---

### 🛠️ **Step-by-Step Process:**
1️⃣ Fetch financial data for the last two years using **`yfinance`**.
2️⃣ Compute key financial ratios (e.g., ROA, Current Ratio, Gross Margin, Asset Turnover).
3️⃣ Evaluate each of the **9 Piotroski F-score criteria** based on the data.
4️⃣ Aggregate the scores to calculate the final **Piotroski F-score**.
5️⃣ Save the results, including raw data and scores, to a **CSV file** for easy analysis. 📂

---

### 🌟 **Why Use This Script?**
- **Cost-Effective**: Utilizes free and open-source APIs.
- **Scalable**: Analyze multiple companies at once.
- **Insightful**: Quickly assess financial health with a proven methodology.

📁 **Output**:
The enriched CSV includes:
- Raw financial data
- Calculated Piotroski F-score
- Insights to compare the financial health of different companies.

🚀 Use this script to make data-driven decisions and enhance your financial analysis toolkit!
'''

# Read company list. These are the companies for which we want to calculate the f-score.
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'equity_list.csv')
current_csv = pd.read_csv(file_path)

# Function to fetch data from yfinance
def get_yfinance_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        print(f"Fetching data for '{ticker}'...")

        # Fetch data for the last two years
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # Check if data is empty
        if financials.empty or balance_sheet.empty or cashflow.empty:
            print(f"No financial data found for ticker '{ticker}'. Please check if the ticker is correct.")
            return {}

        dates_financials = financials.columns
        dates_balance_sheet = balance_sheet.columns
        dates_cashflow = cashflow.columns

        # Ensure we have at least two years of data
        if len(dates_financials) < 2 or len(dates_balance_sheet) < 2 or len(dates_cashflow) < 2:
            print(f"Not enough data for ticker '{ticker}'. At least two years of data are required.")
            return {}

        date_t = dates_financials[0]  # most recent year
        date_t1 = dates_financials[1]  # prior year

        data = {}

        # Net Income
        data['netIncome_t'] = financials.loc['Net Income', date_t] if 'Net Income' in financials.index else 0
        data['netIncome_t1'] = financials.loc['Net Income', date_t1] if 'Net Income' in financials.index else 0

        # Total Assets
        data['totalAssets_t'] = balance_sheet.loc['Total Assets', date_t] if 'Total Assets' in balance_sheet.index else 0
        data['totalAssets_t1'] = balance_sheet.loc['Total Assets', date_t1] if 'Total Assets' in balance_sheet.index else 0

        # Current Assets
        data['currentAssets_t'] = balance_sheet.loc['Current Assets', date_t] if 'Current Assets' in balance_sheet.index else 0
        data['currentAssets_t1'] = balance_sheet.loc['Current Assets', date_t1] if 'Current Assets' in balance_sheet.index else 0

        # Current Liabilities
        data['currentLiabilities_t'] = balance_sheet.loc['Current Liabilities', date_t] if 'Current Liabilities' in balance_sheet.index else 0
        data['currentLiabilities_t1'] = balance_sheet.loc['Current Liabilities', date_t1] if 'Current Liabilities' in balance_sheet.index else 0

        # Operating Cash Flow
        data['operatingCashFlow_t'] = cashflow.loc['Operating Cash Flow', date_t] if 'Operating Cash Flow' in cashflow.index else 0
        data['operatingCashFlow_t1'] = cashflow.loc['Operating Cash Flow', date_t1] if 'Operating Cash Flow' in cashflow.index else 0

        # Long Term Debt
        data['longTermDebt_t'] = balance_sheet.loc['Long Term Debt', date_t] if 'Long Term Debt' in balance_sheet.index else 0
        data['longTermDebt_t1'] = balance_sheet.loc['Long Term Debt', date_t1] if 'Long Term Debt' in balance_sheet.index else 0

        # Shares Outstanding (current only)
        data['sharesOutstanding'] = stock.info.get('sharesOutstanding', 0)

        # Gross Profit
        data['grossProfit_t'] = financials.loc['Gross Profit', date_t] if 'Gross Profit' in financials.index else 0
        data['grossProfit_t1'] = financials.loc['Gross Profit', date_t1] if 'Gross Profit' in financials.index else 0

        # Revenue
        data['revenue_t'] = financials.loc['Total Revenue', date_t] if 'Total Revenue' in financials.index else 0
        data['revenue_t1'] = financials.loc['Total Revenue', date_t1] if 'Total Revenue' in financials.index else 0

        # Issuance and Repurchase of Stock
        data['issuanceOfStock_t'] = cashflow.loc['Issuance Of Capital Stock', date_t] if 'Issuance Of Capital Stock' in cashflow.index else 0.0
        data['repurchaseOfStock_t'] = cashflow.loc['Repurchase Of Capital Stock', date_t] if 'Repurchase Of Capital Stock' in cashflow.index else 0.0

        # Ensure values are floats
        data['issuanceOfStock_t'] = float(data['issuanceOfStock_t'])
        data['repurchaseOfStock_t'] = float(data['repurchaseOfStock_t'])

        data['netIssuanceOfStock_t'] = data['issuanceOfStock_t'] + data['repurchaseOfStock_t']

        # Compute ratios
        data['roa_t'] = data['netIncome_t'] / data['totalAssets_t'] if data['totalAssets_t'] != 0 else 0
        data['roa_t1'] = data['netIncome_t1'] / data['totalAssets_t1'] if data['totalAssets_t1'] != 0 else 0

        # Current Ratio
        data['currentRatio_t'] = data['currentAssets_t'] / data['currentLiabilities_t'] if data['currentLiabilities_t'] != 0 else 0
        data['currentRatio_t1'] = data['currentAssets_t1'] / data['currentLiabilities_t1'] if data['currentLiabilities_t1'] != 0 else 0

        # Gross Margin
        data['grossMargin_t'] = data['grossProfit_t'] / data['revenue_t'] if data['revenue_t'] != 0 else 0
        data['grossMargin_t1'] = data['grossProfit_t1'] / data['revenue_t1'] if data['revenue_t1'] != 0 else 0

        # Asset Turnover
        data['assetTurnover_t'] = data['revenue_t'] / data['totalAssets_t'] if data['totalAssets_t'] != 0 else 0
        data['assetTurnover_t1'] = data['revenue_t1'] / data['totalAssets_t1'] if data['totalAssets_t1'] != 0 else 0

        return data
    except Exception as e:
        print(f"An error occurred while fetching data for ticker '{ticker}': {e}")
        return {}

# Function to compute the Piotroski F-score
def calculate_f_score(data):
    score = 0

    # Profitability
    # 1. Positive Net Income
    if data.get('netIncome_t', 0) > 0:
        score += 1

    # 2. Positive Operating Cash Flow
    if data.get('operatingCashFlow_t', 0) > 0:
        score += 1

    # 3. ROA increasing year over year
    if data.get('roa_t', 0) > data.get('roa_t1', 0):
        score += 1

    # 4. Operating Cash Flow > Net Income
    if data.get('operatingCashFlow_t', 0) > data.get('netIncome_t', 0):
        score += 1

    # Leverage, Liquidity, and Source of Funds
    # 5. Decrease in Long-Term Debt
    if data.get('longTermDebt_t', 0) < data.get('longTermDebt_t1', 0):
        score += 1

    # 6. Increase in Current Ratio
    if data.get('currentRatio_t', 0) > data.get('currentRatio_t1', 0):
        score += 1

    # 7. No New Shares Issued
    if data.get('netIssuanceOfStock_t', 0) <= 0:
        score += 1

    # Operating Efficiency
    # 8. Increase in Gross Margin
    if data.get('grossMargin_t', 0) > data.get('grossMargin_t1', 0):
        score += 1

    # 9. Increase in Asset Turnover
    if data.get('assetTurnover_t', 0) > data.get('assetTurnover_t1', 0):
        score += 1

    # The maximum possible score is 9
    return score

# Enrich the CSV with fundamental data
enriched_data = []
for index, row in current_csv.iterrows():
    ticker = row['ticker']
    yf_data = get_yfinance_data(ticker)
    if not yf_data:
        print(f"Skipping ticker '{ticker}' due to insufficient data.\n")
        continue  # Skip if data is insufficient
    f_score = calculate_f_score(yf_data)
    # Optionally drop the original 'f_score' to avoid confusion
    row = row.drop('f_score', errors='ignore')
    enriched_row = {
        **row,
        **yf_data,
        'f_score': f_score  # Changed 'calculated_f_score' to 'f_score'
    }
    enriched_data.append(enriched_row)
    print(f"Calculated Piotroski F-score for '{ticker}': {f_score}\n")

# Define the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, 'companies.csv')

# Create a new DataFrame and save it to CSV
enriched_csv = pd.DataFrame(enriched_data)
enriched_csv.to_csv(output_file, index=False)

print(f"\nEnriched fundamentals data saved to '{output_file}'.")

# Open the CSV file in Numbers on Mac (optional)
os.system(f"open -a 'Numbers' {output_file}")
