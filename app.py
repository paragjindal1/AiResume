from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np



st.set_page_config(layout="wide")

st.title("AI RESUME GENERATOR")

st.write("""this app helps user to build customized Proffessinal resume with latest job apply links """)

st.image("https://raw.githubusercontent.com/paragjindal1/AiResume/refs/heads/main/bg.png")
st.sidebar.title("Fill Important Detail")
st.sidebar.image("https://raw.githubusercontent.com/paragjindal1/AiResume/refs/heads/main/bg.png")

#API KEYS
GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type="password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type="password")
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type="password")

all_API = [GOOGLE_API_KEY,GROQ_API_KEY,TAVILY_API_KEY]

if not all(all_API):
   st.error("Must give api keys")
   st.stop()
elif all(all_API):
   st.success("API KEYS LOADED SUCCESFULLY")
else:
   st.info("Pass all API-KEYS")

# MULTISELECT OPTION
options = ["Delhi", "Mumbai",
           "Pune", "Banglore",
           "Gurugram/Gurgaon"]
location = st.sidebar.multiselect("Select Location",
                                  options = options)

profile_op = ["Data Analysts", "AI Engineer",
              "Gen AI Developer", "Full-Stack Dev",
              "Data Scientist"]
profile = st.sidebar.multiselect("Select Job Profile",
                                 options = profile_op)


# =========GET USER INFO=============
st.markdown("""### GET USER INFO""")
user_info = st.text_area("""Write your Resume Description: """)

# google model
model = ChatGoogleGenerativeAI(
    model = 'gemini-3-flash-preview',
    google_api_key = GOOGLE_API_KEY
)

#tool for search latest news jib

def search_latest_news_jobs(query):
  """this function helps to fetch latest
  news or jibs related article using tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  response = client.search(query)

  return response




#agent
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs]
)



# main agent function 

def main_agent(agent,query):
    """this is the main agent or main agent orchestrate sub agents"""
    # Giving promt to create detailed prompt for code generation

    prompt = """You are Ai assistent and
    below given is a prompt , your
    rask is to give detailed prompt for this.
    you are a proffessional Resume Generator where user
    will give their personal info ,
    you have to create detail Resume for student or professional one,
    it must be with dynamic ui and ux and, with advance CSS profestional Desiging make sure
    to give output in html format only
    no markdown allowed"""

    response = agent.invoke({'messages':[{'role':'user','content':prompt}]})

    detail_prompt = response['messages'][-1].content[-1]['text']

    with open('prompt.txt','w') as f:
      f.write(detail_prompt)

    user_details = f"""Below Given is a user details generate resume based on the chat ,if not given
    Default Resume: python developer
    user details:{query}"""

    final_prompt = prompt + detail_prompt + user_details

    response = agent.invoke({'messages':[{'role':'user','content':final_prompt}]})

    code = response['messages'][-1].content[-1]['text']

    return code


def get_jobs(agent,Location = "Noida,Delhi",Profile = "DATA ANALYSIS,AI ENGINEER"):
  prompt = f"""Based on user given Job profile,
  fetch latest jobs or jobs apply article using naukri , linkindin,indeed, or all popular job apply platforms , show Results with JOB PROFILE NAME,
  LACATION,SALARY,COMAPNY NAME, SHOW jobs related to given {Location} and {Profile}, Out put must be in
  Professinal HTML , naukri theme cards with dynamic DEsign,
  show atleast top 10-20 results with direct apply link"""

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})

  code = response['messages'][-1].content[-1]['text']

  return code


if st.button("Generate Resume"):
    with st.spinner("Agent Running"):
        code = main_agent(agent,user_info)
        st.html(code , width="stretch" ,
                unsafe_allow_javascript=True)
        st.divider()  # to give horizontal div
        job_code = get_jobs(agent,location,profile)
        st.html(job_code , width="stretch" ,
                unsafe_allow_javascript=True)




