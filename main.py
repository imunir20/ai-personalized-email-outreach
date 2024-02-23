# Wrap in a streamlit interface
# Ability to upload CSV files and read leads from there
# Potentially add custom tool to writer agent to send an email if basic crew functionality works fine

# Add in Ollama support
# Setup API keys

import streamlit as st
import pandas as pd

from crewai import Crew
from textwrap import dedent
from outreach_agents import OutreachAgents
from outreach_tasks import OutreachTasks

from dotenv import load_dotenv

load_dotenv()

class OutreachCrew():
    
    def __init__(self, sender_first_name, recipient_first_name, recipient_email_id, company):
        self.sender_first_name = sender_first_name
        self.recipient_first_name = recipient_first_name
        self.recipient_email_id = recipient_email_id
        self.company = company
        # Can be customized for your specific business services/products/propositions
        self.business_propositions = """
        1. Social Media Marketing: Expands the social media reach of a company through creating original content in the form of videos, posts, articles. Increases engagement with customers and helps reach customers through platforms like Facebook, Instagram, and TikTok. Targets a wide variety of demographics.
        2. Search Engine Optimization (SEO): Improves the ranking of a company on popular search engines like Google so that the company is found more likely on relevant keywords. Includes optimization of Google My Business profile (GMB), website relevance. Useful for local businesses dependent on traffic that comes through internet searches, like \"[type of business] near me\"
        3. Paid Ads Expertise: Build and monitor paid ads campaigns through a variety of platforms like Google Ads, Facebook Ads, Instagram Ads, TikTok Ads. Optimizes campaigns to target potential customers that may not be of their typical demographic. Increases return on investment by double at least.
        """
    
    def run(self):
        agents = OutreachAgents()
        tasks = OutreachTasks()

        company_researcher = agents.company_researcher()
        business_analyst = agents.business_analyst()
        outreach_email_writer = agents.outreach_email_writer()

        research_task = tasks.research_company(company_researcher, self.company)
        analysis_task = tasks.analyze_company(business_analyst, self.business_propositions)
        email_task = tasks.write_outreach_email(outreach_email_writer, self.sender_first_name, self.recipient_first_name, self.recipient_email_id)

        crew = Crew(
            agents=[
                company_researcher, business_analyst, outreach_email_writer
            ],
            tasks=[
                research_task, analysis_task, email_task
            ],
            verbose=True
        )

        result = crew.kickoff()
        return result
    
if __name__ == "__main__":

    # Streamlit app usage
    st.title("AI Automated Personalized Email Outreach")

    with st.form('form'):
        sender_first_name = st.sidebar.text_input(':pencil: Your First Name', placeholder='John')
        emailUser = st.sidebar.text_input(':email: Email', placeholder='johndoe@gmail.com')
        emailPwd = st.sidebar.text_input(':lock: Password', type='password')
        recipient_first_name = None
        recipient_email_id = None
        recipient_company = None

        df = None
        upFile = st.file_uploader("Upload lead list (.csv)")
        if upFile is not None and upFile.name[-3:] == 'csv':
            df = pd.read_csv(upFile).to_dict('records')
            try:
                recipient_first_name = df[0]['first_name']
                recipient_email_id = df[0]['email']
                recipient_company = df[0]['company']
            except:
                st.exception('Invalid CSV!')

        startButton = st.form_submit_button('Begin Outreach')

        if startButton:
            progress_text = "Conducting research and preparing to send personalized email to your leads..."
            with st.spinner(progress_text):
                outreach_crew = OutreachCrew(sender_first_name, recipient_first_name, recipient_email_id, recipient_company)
                result = outreach_crew.run()
                # time.sleep(1)
                # st.info(df)
            st.success("Your email was sent!")



    # Basic CLI usage of outreach system
            
    # print("## Welcome to the Email Outreach Crew")
    # print('--------------------------------------')
    # sender_first_name = input(dedent('What is your first name? '))
    # recipient_first_name = input(dedent('What is the first name of the prospect you wish to contact? '))
    # recipient_email_id = input(dedent('What is their email? '))
    # recipient_company = input(dedent('For what company do they work for? '))

    # outreach_crew = OutreachCrew(sender_first_name, recipient_first_name, recipient_email_id, recipient_company)
    # result = outreach_crew.run()
    # print("\n\n############################")
    # print("## Here is your outreach email to the prospect")
    # print("#############################\n")
    # print(result)

