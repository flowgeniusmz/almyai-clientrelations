import streamlit as st
from openai import OpenAI
from functions import pagesetup as ps

ps.set_title("AlmyAI", "Client Relations Assistant")
ps.set_page_overview("Overview", "**Client Relations Assistant** provides a way to quickly ask about the troubleshooting for client relations")
messages1 = [
  {"role": "assistant", "content": "Hi"},
  {"role": "user", "content": "whats 2563476up"}
]

messages2 = [
  {"role": "assistant", "content": "Hi3"},
  {"role": "user", "content": "whats u3333333333242342342342p"}
]

messages3 = [
  {"role": "assistant", "content": "Hi"},
  {"role": "user", "content": "whats up33333333333333"}
]

messages4 = [
  {"role": "assistant", "content": "Hi"},
  {"role": "user", "content": "whats upadfadsfads"}
]

def displaychat(varMessages):
  for msg in varMessages:
    role = msg['role']
    content = msg['content']
    st.chat_message(role).markdown(content)
    

ps.set_blue_header("Operating Manual")
displaychat(messages1)
st.divider()

ps.set_blue_header("AAO")
displaychat(messages2)
st.divider()

ps.set_blue_header("Operating Manual")
displaychat(messages3)
st.divider()

ps.set_blue_header("Process Flow")
displaychat(messages4)
st.divider()
