import json
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html


class SearchTools():

    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results"""
        top_result_to_return = 2
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with the SERPER API KEY that was supplied."
        else:
            results = response.json()['organic']
            resultStrings = []
            for result in results[:top_result_to_return]:
                try:
                    resultStrings.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next

            return '\n'.join(resultStrings)


class BrowserTools():
    
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with.',
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary and nothing else.\n\nCONTENT\n---------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)

        return "\n\n".join(summaries)
    
class EmailTools():

    @tool("Send emails to a single recipient")
    def send_email(recipient_email_id, email_subject, email_message):
        """Useful to send an email with a message inside from a sender to a recipient"""
        # Hardcoded some variables for now
        sender_email_id = ''                      # Enter sender email here
        sender_password = ''   # Enter the APP password for the sender email here

        message = MIMEMultipart()
        message["From"] = sender_email_id
        message["To"] = recipient_email_id
        message["Subject"] = email_subject

        message.attach(MIMEText(email_message, "plain"))
        text = message.as_string()

        with smtplib.SMTP('smtp.gmail.com', 587) as server:       # Can be further customized for all sorts of email providers beyond gmail
            # Start TLS for security
            server.starttls()
            # Authentication
            server.login(sender_email_id, sender_password)
            # Send the email
            server.sendmail(sender_email_id, recipient_email_id, text)