def split_message(split_seperator: str, max_len: int, message: str) -> list:
    message_split = message.split(split_seperator)

    split_message = []
    while len(message_split) > 0:
        buffer = ""
        
        buffer = message_split.pop(0)

        while (len(message_split) > 0) and (len(buffer) + len(split_seperator) + len(message_split[0]) <= max_len):
            buffer = buffer + split_seperator + message_split.pop(0)
        
        split_message.append(buffer)
    
    return split_message