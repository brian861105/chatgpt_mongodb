from Database import DatabaseManager

database = DatabaseManager()
# print(database.CreateSession(UserId="TestForFront"))
# print(database.ReadSession(UserId="TestForFront",SessionId="f5f9b6cf-51e4-4864-8c9d-52695c14283d"))
# print(database.UpoloadMessage(UserId="TestForFront",SessionId="52ff81a6-b623-4d56-bbc3-b81dcaa16c52",NewMessage="hello"))
print(database.ReadUser(UserId="TestForFront"))

# [Log] requestData: – {name: "new title", messages: [], SessionId: "f5f9b6cf-51e4-4864-8c9d-52695c14283d"} (chatroom, line 117)