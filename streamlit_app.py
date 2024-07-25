import streamlit as st
import json
from typing import Sequence, List
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import AgentRunner
from llama_index.agent.openai import OpenAIAgentWorker, OpenAIAgent

import os
import openai
import nest_asyncio

################################
########### CONFIG #############
################################

os.environ['OPENAI_API_KEY'] = st.secrets["API_KEY"]
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(model="gpt-3.5-turbo")

###################################
########### FUNCTIONS #############
###################################
    
def say_hi():
    st.session_state.clicked = True

def do_simple_math():
    st.session_state.sample_math = True

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
tools = [multiply_tool, add_tool]


######## Bootstraping agent
agent = OpenAIAgent.from_tools(tools, llm=llm, verbose=True)



# #### Chatbot config
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])


#############################
########### GUI #############
#############################

st.header("Experiment #0.1 💬 📚")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'sample_math' not in st.session_state:
    st.session_state.sample_math = False


######## Sidebar
st.sidebar.header("Tests")
st.sidebar.markdown(
    "LllamaIndex eperiment"
)

st.sidebar.button('Say HI!', on_click=say_hi)

st.sidebar.button('Show Math skills', on_click=do_simple_math)

#
st.sidebar.header("💬 Chatbot")


###### Main content
# Write Results
with st.expander("Moreinfo"):
    st.write('lorem ipsum')
    if openai_api_key:
        st.write("Zmienna OPENAI_API_KEY jest ustawiona.")
    else:
        st.write("Zmienna OPENAI_API_KEY nie jest ustawiona.")

if st.session_state.clicked:
    st.write(">>> Response from agent:", str(agent.chat("Hi")))

if st.session_state.sample_math:
    st.write(">>> Do math: ", str(agent.chat("What is (121 * 3) + 42?")))


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
