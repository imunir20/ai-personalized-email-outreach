from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

from outreach_tools import SearchTools, BrowserTools, EmailTools

class OutreachAgents():
    #def __init__(self):
        #self.llm = Ollama(model="gemma:7b")
        #self.llm =  ChatOpenAI(model_name="gpt-3.5-turbo-0125")

    def company_researcher(self):
        return Agent(
            role="Company Researcher",
            goal="Scrape information and gather insights about a company",
            backstory="An expert in performing thorough research about all sorts of companies using the internet",
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True,
            allow_delegation=False,
            #llm=self.llm
        )
    
    def business_analyst(self):
        return Agent(
            role="Expert Business Analyst",
            goal="Identify and provide solutions for the biggest pain points and bottlenecks preventing a company from reaching its full revenue and productivity potential",
            backstory="A highly experienced business analysts that can pinpoint a company's weaknesses and suggest appropriate solutions to maximize their productivity and earning potential",
            verbose=True,
            allow_delegation=False,
            #llm=self.llm
        )
    
    def outreach_email_writer(self):
        return Agent(
            role="Expert Outreach Email Writer",
            goal="Write and send a highly personalized outreach emails using the given research to a given high-ranking official of a company",
            backstory="An expert in writing and sending personalized outreach emails based on meticulous research that entice company executives to respond",
            tools=[EmailTools.send_email],
            verbose=True,
            allow_delegation=False,
            #llm=self.llm
        )