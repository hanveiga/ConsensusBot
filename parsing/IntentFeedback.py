
def start(listening):
    give_reply = False

    if listening == False:
        give_reply = True

    listening = True
    return "Let's start a meeting schedule" , give_reply, listening

def end(listening):
    return "Let's see when we can meet", False , listening

def do_nothing(listening):
    return "Nothing to do" , False, listening

def give_feedback(message, is_listening):
    """

    :param message:
    :param is_listening:
    :return: [feedback_message_str, should_respond_to_user_bool, is_listen_boolean ]
    """
    if message == "start":
        return start(is_listening)
    elif message == "end":
        return end(is_listening)
    else:
        return do_nothing(is_listening)