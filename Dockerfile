FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY chat/requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /app/chat/

COPY ./chat /app/chat/

COPY chat/static/js/*.js /usr/local/lib/python3.9/site-packages/streamlit/static/static/js/
COPY chat/static/img/ /usr/local/lib/python3.9/site-packages/streamlit/static/static/img/

WORKDIR /app/chat

CMD ["streamlit", "run", "app.py"]