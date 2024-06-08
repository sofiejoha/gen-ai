from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI

def summarize_overall(text_summary, image_summary, max_sentences=5):
    """
    Generate an overall summary using LangChain and GPT-4.
    Input: text_summary (str), image_summary (str), max_sentences (int)
    Output: overall_summary (str)
    """
    combined_summary = f"Text Summary: {text_summary}\nImage Summary: {image_summary}"
    template = """System: Provide a helpful overall summary in {max_sentences} sentences.
    Human: {combined_summary}
    AI"""
    prompt = PromptTemplate.from_template(template)
    agent = AzureChatOpenAI(
        api_version="2023-12-01-preview",
        azure_endpoint="https://gpt-course.openai.azure.com",
        api_key="72e0e504082a45f594cc2308b8d01ca9",
        deployment_name="gpt-4"
    )
    chain = LLMChain(
        llm=agent,
        prompt=prompt
    )
    overall_summary = chain.run(reference="", combined_summary=combined_summary, max_sentences=max_sentences)
    return overall_summary.strip()