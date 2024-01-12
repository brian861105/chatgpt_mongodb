FROM python:3.10

WORKDIR /root

COPY . /root/chatroom-backend/

RUN pip install --no-cache-dir -r chatroom-backend/requirements.txt

EXPOSE 5000

CMD ["python", "chatroom-backend/app/api.py"]
