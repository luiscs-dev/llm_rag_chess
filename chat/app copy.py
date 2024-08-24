import streamlit as st
import streamlit.components.v1 as components
from utils import llm_utils
import uuid
from collections import deque

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

messages = st.container(height=350)

def render_messages(messages):
    for idx, message in enumerate(st.session_state.messages):
        messages.chat_message(message['role']).write(message['content'])
        if message['role'] == 'assistant':
            col1, col2 = st.columns(2, vertical_alignment="bottom")
            with col2: 
                if messages.button("👍", key=f"thumbs_up_{idx}"):
                    st.session_state.feedback[idx] = 'thumps_up'
            with col1:
                if messages.button("👎", key=f"thumbs_down_{idx}"):
                    st.session_state.feedback[idx] = 'thumps_down'

@st.cache_data
def rag(prompt):
    return llm_utils.llm(prompt)

if prompt := st.chat_input("How can I assist you, today?"):

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.status("Searching information ...", prompt[:20]):
        answer = rag(prompt)
        st.session_state.messages.append({'role': 'assistant', 'content': answer})

    render_messages(messages)

if st.button("Clear Chat"):
    clear_chat()
