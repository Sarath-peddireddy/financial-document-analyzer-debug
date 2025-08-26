import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent
from tools import search_tool, FinancialDocumentTool

from crewai_tools.llms.openai import OpenAI
llm = OpenAI(model="gpt-3.5-turbo") 


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide concise, actionable investment advice based on the user's query.",
    verbose=True,
    memory=False,
    backstory="Expert in market analysis and investment strategy.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Quickly verify if a document is financial in nature.",
    verbose=True,
    memory=False,
    backstory="Experienced in compliance and document verification.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Recommend suitable investment products based on document analysis.",
    verbose=True,
    memory=False,
    backstory="Specialist in investment products and portfolio management.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Assess and summarize key risks from financial documents.",
    verbose=True,
    memory=False,
    backstory="Expert in risk management and financial modeling.",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)