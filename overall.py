from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from config import *

def summarize_overall(text_summary, image_summary, personality, max_sentences = 5):
    """
    Generate an overall summary using LangChain and GPT-4.
    Input: text_summary (str), image_summary (str), max_sentences (int)
    Output: overall_summary (str)
    """
    combined_summary = f"Text Summary: {text_summary}\nImage Summary: {image_summary}"
    
    if personality == 'Kindergarden':
        template = """System: Provide a helpful overall summary in {max_sentences} sentences. Do this without letting us know that this is a 
        combined summary between the text summary and image summary. We want the summary to look complete and not two separated summaries. 
        Also, do not specifically describe what was seen in the video, but instead incorporate this information seamlessly into the text summary. 
        Can you give the summary as if you were someone working in a kindergarden trying to explain it to a child. And also, do not use past tense.
        It is very important that you always answer in a polite manner!

        Human: {combined_summary}
        AI"""
    
    elif personality == 'Mafiaboss':
        template = """System: Provide a helpful overall summary in {max_sentences} sentences. Do this without letting us know that this is a 
        combined summary between the text summary and image summary. We want the summary to look complete and not two separated summaries. 
        Also, do not specifically describe what was seen in the video, but instead incorporate this information seamlessly into the text summary. 
        Can you give the summary as if you were a 1950s mafia boss born and raised in the streets of Brooklyn, New York. 
        And also, do not use past tense.
        It is very important that you always answer in a polite manner!

        Human: {combined_summary}
        AI"""

    elif personality == 'Professor':
        template = """System: Provide a helpful overall summary in {max_sentences} sentences. Do this without letting us know that this is a 
        combined summary between the text summary and image summary. We want the summary to look complete and not two separated summaries. 
        Also, do not specifically describe what was seen in the video, but instead incorporate this information seamlessly into the text summary. 
        Can you give the summary as if you were a professor working at a university, trying to explain it to your university students. 
        And also, do not use past tense.
        It is very important that you always answer in a polite manner!

        Human: {combined_summary}
        AI"""

    prompt = PromptTemplate.from_template(template)
    agent = AzureChatOpenAI(
        api_version= API_VERSION,
        azure_endpoint = ENDPOINT,
        api_key = API_KEY,
        deployment_name = DEPLOYMENT_NAME
    )
    
    chain = LLMChain(
        llm = agent,
        prompt = prompt
    )

    overall_summary = chain.run(reference = "", combined_summary = combined_summary, max_sentences = max_sentences)
    return overall_summary.strip()