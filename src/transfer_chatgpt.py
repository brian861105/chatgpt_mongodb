def transfer_chat(message):
    result = []
    for i in range(0, len(message)):
        if (i % 2):
            result.append({"role": "user", "content": message[i]})
        else:
            result.append({"role": "assistant", "content": message[i]})
    return result

    