FROM python:3.10

WORKDIR /root

COPY . /root/chatroom-backend/

RUN pip install --no-cache-dir -r chatroom-backend/requirements.txt
RUN 
EXPOSE 80 5000

CMD ["sh", "-c", "sh chatroom-backend/tmp/key.sh && python chatroom-backend/app/api.py"]
