from crewai import Task
from agents import financial_analyst, verifier
from tools import search_tool, FinancialDocumentTool

analyze_financial_document = Task(
    description="Analyze the uploaded financial document and answer the user's query. Use the provided PDF and, if needed, search the internet for context.",
    expected_output="""
{
  "summary": "Brief summary of the document",
  "insights": ["Key insight 1", "Key insight 2"],
  "recommendations": ["Investment recommendation 1", "Investment recommendation 2"],
  "risks": ["Risk 1", "Risk 2"],
  "references": ["https://example-finance1.com", "https://example-finance2.com"]
}
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="Review the financial data and provide actionable investment recommendations.",
    expected_output="""
{
  "advice": ["Buy/Sell/Hold recommendations with brief justifications"],
  "products": ["Suggested investment products"],
  "strategies": ["Investment strategies"],
  "references": ["https://example-investment.com"]
}
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="Identify and summarize key risks from the financial document.",
    expected_output="""
{
  "risks": ["Risk 1", "Risk 2"],
  "mitigation": ["Mitigation strategy 1", "Mitigation strategy 2"]
}
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Verify if the uploaded file is a financial document. Respond with a confidence score and reasoning.",
    expected_output="""
{
  "is_financial_document": true,
  "confidence": 0.95,
  "reasoning": "Detected financial terms and structure."
}
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)