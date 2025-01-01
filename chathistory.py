import streamlit as st
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, history):
    context = ""
    for user_role, user_text, bot_role, bot_text in history:
        context = f"{user_role}: {user_text}\n{bot_role}: {bot_text}\n"

    context = f"You: {question}\nBot:"
    response = chat.send_message(context, stream=True)
    response_text = ''.join(chunk.text for chunk in response)
    return response_text

def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
        
    return []

def save_chat_history(file_path, chat_history):
    with open(file_path, 'w') as file:
        json.dump(chat_history, file)

CHAT_HISTORY_FILE = "chat_history.json"

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = load_chat_history(CHAT_HISTORY_FILE)


st.set_page_config(page_title="Q&A")
st.header("Your Chatbot")

input = st.text_input("Input your question: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input, st.session_state['chat_history'])
    st.session_state['chat_history'].append(("You", input, "Bot", response))
    save_chat_history(CHAT_HISTORY_FILE, st.session_state['chat_history'])

st.subheader("Your chatbot")

for user_role, user_text, bot_role, bot_text in st.session_state["chat_history"]:
    with st.container():
        st.markdown(f"""
        {user_role}: {user_text}
        {bot_role}: {bot_text}
""", unsafe_allow_html=True)