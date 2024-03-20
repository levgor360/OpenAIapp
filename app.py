import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("Future forecaster")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    # define user's input
    st.session_state.messages.append({"role": "user", "content": prompt})
    # display user's message in chat interface
    st.chat_message("user").write(prompt)
    # API request
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # Save generated output to variable 'msg
    msg = response.choices[0].message.content
    # Save response to the dictionary st.session_state.messages. The dictionary has values "role" and "content"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    # Display the generated response by pulling the "msg" section
    st.chat_message("assistant").write(msg)
