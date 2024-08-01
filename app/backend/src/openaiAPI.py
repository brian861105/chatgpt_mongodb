import openai
import os
OpenaiKey = os.getenv("OpenaiToken")

class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo", MaxToken=5):
        openai.api_key = OpenaiKey
        self.model = model
        self.MaxToken = MaxToken

    def APIkeyIsValid(self):
        try:
            openai.Model.list()
            return True
        except Exception as e:
            print(f"OpenAI Connect Error: {e}")

    def Chat(self, OldMessages, NewMessage):
        try:
            OldMessages.append(NewMessage)
            InputMessage = OldMessages
            response = openai.ChatCompletion.create(
                model=self.model, messages=InputMessage, max_tokens=self.MaxToken
            )
            OutputMessage = response.choices[0].message.content
            InputMessage.append({"role": "system", "content": OutputMessage})
            ReturnMessage = InputMessage
            return ReturnMessage
        except Exception as e:
            print(f"OpenAI Chat Error: {e}")
