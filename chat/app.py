import streamlit as st
import streamlit.components.v1 as components
from utils import llm_utils
from utils import chess_utils
import uuid
from collections import deque
import hashlib

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = deque()
if 'feedback' not in st.session_state:
    st.session_state.feedback = dict()


st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.header("Study section")
#st.sidebar.text("You can ")
with st.sidebar:
   components.html(chess_utils.chess_board, height=550)

@st.cache_data(ttl="6h23s")
def rag(prompt):
    return llm_utils.rag(prompt)
    

def hash_text(text):
    text_bytes = text.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(text_bytes)
    hashed_text = sha256.hexdigest()
    
    return hashed_text

st.title("💬 Chess Assistant")
st.caption("🚀 A Streamlit chatbot powered by Ollama")
#st.write(st.session_state)

messages = st.container(height=350)


def render_messages():
    for idx, message in enumerate(st.session_state.messages):
        messages.chat_message(message['role']).write(message['content'])

def store_feedback(**kwargs):
    if st.session_state.session_id not in st.session_state.feedback:
        st.session_state.feedback[st.session_state.session_id] = [kwargs]
    else:
        st.session_state.feedback[st.session_state.session_id].append(kwargs)

    render_messages()
    messages.success(f"Thank you for your feedback!", icon="✅")
    



if prompt := st.chat_input("How can I assist you, today?"):

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.status(f"Searching information about {prompt[:40]} ..."):
        answer = rag(prompt)
    
    st.session_state.messages.append({'role': 'assistant', 'content': answer})

    render_messages()

    col1, col2, col3 = messages.columns(3)
    fid =  hash_text(prompt+answer)
    data = {
            "question": prompt,
            "answer": answer,
            "feedback_id": fid
        }
    with col1:
        st.write('Please rate last answer') 
    with col2:
        data["rating"] = 'thumbs_down'
        st.button("👎", on_click=store_feedback, kwargs=data)
            
    with col3:
        data["rating"] = 'thumbs_up'
        st.button("👍", on_click=store_feedback, kwargs=data)


    

    
   


