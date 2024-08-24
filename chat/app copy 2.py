import streamlit as st
import streamlit.components.v1 as components
from utils import llm_utils
import uuid
from collections import deque
import hashlib

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = deque()
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

def clear_chat():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages.clear()
    st.session_state.feedback.clear()

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
st.sidebar.header("This is the sidebar")
st.sidebar.text("This is some text in the sidebar")

with st.sidebar:
   components.html(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat and Chess</title>
    <link rel="stylesheet"
      href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css"
      integrity="sha384-q94+BZtLrkL1/ohfjR8c6L+A6qzNH9R2hBLwyoAfu3i/WCvQjzL2RQJ3uNHDISdU"
      crossorigin="anonymous">
      <style>
         #board { width: 350px; }
    </style>
</head>
<body>
    <div id="board"></div>
    <button id="clearBoardBtn">Clear Board</button>
    <button id="startPositionBtn">Start Position</button>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"
    integrity="sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2"
    crossorigin="anonymous"></script>

    <script src="static/js/chessboard-1.0.0.js"></script>
    <!--<script src="static/chessboard.js"></script> -->

    <script>
        var customPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

        var board = Chessboard('board', {
            draggable: true,
            position: 'start',  // Sets the starting position with all pieces
            onSnapEnd: onSnapEnd,
            dropOffBoard: 'trash',  // Option to allow dropping pieces off the board
            sparePieces: true       // Option to enable spare pieces
        })

        $('#clearBoardBtn').on('click', board.clear)
        $('#startPositionBtn').on('click', board.start)

        function onSnapEnd () {
           board.position(board.fen());
        }

    </script>
</body>
</html>
        """, height=480
    )


@st.cache_data
def rag(prompt):
    return llm_utils.llm(prompt)

def store_feedback(question, answer, feedback):
    fid =  hash_text(question+answer)
    data = {
        "question": question,
        "answer": answer,
        "rating": feedback,
        "feedback_id": fid
    }    
    st.session_state.feedback[st.session_state.session_id].append(data)
    st.markdown(f"Thank you for your feedback.")

def hash_text(text):
    text_bytes = text.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(text_bytes)
    hashed_text = sha256.hexdigest()
    
    return hashed_text

st.title("💬 Chess Assistant")
st.caption("🚀 A Streamlit chatbot powered by Ollama")
st.write(st.session_state.feedback)

messages = st.container(height=350)

for msg in st.session_state.messages:
    messages.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("How can I assist you, today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.chat_message("user").write(prompt)
    with st.status(f"Searching information about {prompt[:40]} ..."):
        answer = rag(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    messages.chat_message("assistant").write(answer)
    
    sentiment_mapping = ["one", "two", "three", "four", "five"]

    col1, col2, col3= st.columns(3)
    with col1:
        st.write('Please rate this experience') 
    with col2:
        if st.button("👎", key=f"thumbs_down"):
            store_feedback(prompt, answer, "thumbs_down")
    with col3:
        if st.button("👍", key=f"thumbs_up"):
            store_feedback(prompt, answer, "thumbs_up")
    
    

    
   


