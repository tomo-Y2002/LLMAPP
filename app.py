import streamlit as st
import yaml
from openai import OpenAI

with open("config.yaml", encoding="utf-8")as f:
  configs = yaml.safe_load(f)
OPENAI_KEY = configs["OPENAI_KEY"]
client = OpenAI(
  api_key = OPENAI_KEY
)

st.title("Chat Bot")

# initializing
if "messages" not in st.session_state:
  st.session_state.messages = []

# display part
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up ?") :
  with st.chat_message("user"):
    st.markdown(prompt)
  st.session_state.messages.append({"role":"user", "content":prompt})
  with st.chat_message("assistant"):
    stream = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
      ],
      stream=True,
    )
    response = st.write_stream(stream)
  st.session_state.messages.append({"role":"assistant", "content":response})
