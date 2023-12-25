import pytest
from src.openaiAPI import ChatGPT


def test_ConnectOpenAI():
    GPT = ChatGPT()
    assert GPT.APIkeyIsValid() == True


def test_Chat():
    GPT = ChatGPT()
    OldMessage = []
    NewMessage = {"role": "user", "content": "Hello World"}

    assert isinstance(GPT.Chat(OldMessage, NewMessage)[-1]["content"], str) == True
