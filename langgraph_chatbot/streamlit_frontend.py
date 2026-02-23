import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid



# ----------- Utility functions ----------

# Generate a unique thread ID for the conversation
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# ---------- Session setup ----------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


# ---------- sidebar ui ----------

st.sidebar.title("LangGraph Chatbot")
st.sidebar.markdown("This is a chatbot interface built with Streamlit and LangGraph.")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads']:
    st.sidebar.text(thread_id)


# loading the conversation history before the main ui,
#  so that the user can see the history while typing new messages.
#  This is important for a good user experience, as it allows the user to keep track of the conversation context.

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# ---------- main ui ----------

user_input = st.chat_input("Type your message here ...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)


    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    
# print(st.session_state['chat_threads'])
    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response['messages'][-1].content

    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)