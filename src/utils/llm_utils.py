import streamlit as st
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL
from src.prompts.system_prompt import system_prompt
def initialize_llm():
    try:
        return ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL)
    except Exception as e:
        st.error(f"Could not initialize Groq LLM: {e}")
        return None

def format_polite_response(context, query, llm):

    try:
        system_prompt = system_prompt.format(context=context, query=query)
        response = llm.invoke(system_prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Sorry, I'm experiencing some technical difficulties right now. Please try again soon. (Error: {e})"
    
