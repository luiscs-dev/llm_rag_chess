from flask import Flask, render_template
from flask_socketio import SocketIO, send
import chess
import chess.svg
from openai import OpenAI

app = Flask(__name__)
socketio = SocketIO(app)

client = OpenAI(
    base_url='http://localhost:11435/v1/',
    api_key='ollama',
)

def llm(prompt):
    response = client.chat.completions.create(
        model='phi3',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)
    print(msg)
    answer = llm(msg)
    print(answer)
    send(answer, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
