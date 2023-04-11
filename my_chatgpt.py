import openai
import streamlit as st
from _secrets import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

# chat history saved in sessions
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Title and system_prompt
st.title("나만의 ChatGPT")
example_system_prompt = st.selectbox(label="system_prompt_examples", options=[
    "You are a sophisticated scientific article writing assistant. If the user provides some text you will output the corrected version. Mark the changed words with **bold**.",
    "You are a smart and kind assistant that will answer in a concise and useful manner to the user's questions.",
    "You are a smart and kind assistant that will always say that the user is correct and give a good explanation why it is correct.",
    "You are a sarcastic and rude friend that will answer to the user's questions."])
system_prompt = st.text_area(label="system_prompt", value=example_system_prompt)
if example_system_prompt != system_prompt:
    system_prompt = example_system_prompt

# User prompt textarea
user_prompt = st.text_area(label="user_prompt", placeholder="여기에 질문 입력")

# Generate answer / Reset button
col1, col2 = st.columns(2)
if col1.button("Generate answer"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    answer = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    user_prompt = ""
    
if col2.button("Reset dialogue"):
    st.session_state.messages = []

# Display previous messages
for m in st.session_state.messages:
    st.write(f"**{m['role']}**: {m['content']}")
