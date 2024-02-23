from crewai import Task
from textwrap import dedent
from datetime import date

class OutreachTasks():

    def research_company(self, agent, company):
        return Task(description=dedent(f"""
            Analyze Google search results for a specific company and perform in-depth research about them.
            
            Your research should provide concise, precise answers to questions like the following:
            What does the company do?
            What is their audience?
            What products and services do they offer?
            
            The findings from this research will be used to craft an outreach email to a prospective client within the company.
            The information you provide should be as accurate and relevant as possible, as it will directly impact the effectiveness of the outreach strategy.
            Keep in mind that your responses should be designed to fit seamlessly into a professional email.
            Therefore, your answers should be written in a clear, concise, and formal manner.
                                       
            Here is the company that you are researching: {company}

            Remember, your research should be based solely on publicly available Google search results for the company.
            Please refrain from speculating or making assumptions. Your task is to provide factual and verifiable information.
            {self.__reward_section}
            """),
            agent=agent)
    
    def analyze_company(self, agent, business_propositions):
        return Task(description=dedent(f"""
            Using these research findings, identify the biggest problem and use case for the prospect and his company that has the highest ROI.
            Think deeply about the core role and responsibilities of the prospect currently so that you can identify specific problems and use cases they are facing.
            The goal is to find the use case that will get their attention and stop them from scrolling through their emails.
            {self.__reward_section}
                                       
            Here is information about our core business propositions and services:
            {business_propositions}
            """),
            agent=agent)
    
    def write_outreach_email(self, agent, sender_first_name, recipient_first_name, recipient_email_id):
        return Task(description=dedent(f"""
            Using this company analysis, craft and send a personalized outreach email based on detailed research and analysis done on the prospect's company.
            Your goal is to make each contact feel both valued and understood, and to create a genuine connection that paves the way for a fruitful business understanding.
            
            Your task is to use the analysis provided to compose a compelling, personalized outreach email to a prospective client in an informal and friendly tone that conveys genuine interest.
            You MUST focus on a problem and value proposition and not make up tools or solutions. If there is no case study or value proposition, don't use one.
                                       
            Your email must follow these guidelines:
                                       
            **Mimic past email example**: Make sure you follow the logic, voice, and tone from the given past outreach email example as best practice, be almost identical.
                                       
            **Focus on their specific pain points and use case (in one paragraph)**: This is the core part of the message, outline a pain point and use case mentioned below, and be specific: 
            Focus on the prospect, always speak from their point of view, and use the words \"I\", \"Our agency\", \"Flash Marketing and SEO Agency\", always and only focus on the prospect's problem and challenges;
            be facts driven, don't say words like we can be a game-changer or something similar.
                                       
            **Call To Action (CTA)**: Be explicit about your desired next step. \"Would you have time for a quick chat this week?\"
                                       
            **2 Paragraphs in total, less than 150 words**                     
            ------
            **Past outreach email example**
            
            Hey Michael,
                                       
            Noticed that GFS Computers is in the early stages of scaling operations and most likely are coming across challenges in expanding digital presence.
            Local businesses like Garfield Cell Phone Repair and Green Grove Accounting have used our online marketing services to consistently create organic content, expand social media reach, engage with customers, and even establish themselves as experts within their fields.
            This has resulted in 3x increase in monthly revenue, sometimes even going up to five or ten times more, allowing them to focus on product development and further honing their services.
                                       
            Does this sound like something that could GFS Computers? If so, when would be a good time for a quick chat?
                                       
            Thanks,
            Roland
            -------
            The first name of the prospect you will be writing to is {recipient_first_name}
            The recipient email is {recipient_email_id}
            You should write the email from the perspective of {sender_first_name}.
            You should also come up a relevant and personalized email subject that you will use when you send the email.
            {self.__reward_section}
            """), 
            agent=agent)
    
    def __reward_section(self):
        return "If you do your BEST WORK, you'll receive a SUPER SPECIAL reward!"