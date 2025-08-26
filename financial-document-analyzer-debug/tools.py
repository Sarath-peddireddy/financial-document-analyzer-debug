import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools.tools.serper_dev_tool import SerperDevTool
from crewai_tools.tools.pdf_tool import Pdf  

search_tool = SerperDevTool()

class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """Read and clean text from a PDF file."""
        docs = Pdf(file_path=path).load()
        full_report = ""
        for data in docs:
            content = data.page_content.replace("\n\n", "\n").strip()
            full_report += content + "\n"
        return full_report

class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        processed_data = financial_document_data.replace("  ", " ")
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"