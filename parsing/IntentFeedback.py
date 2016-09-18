from parsing.States import States

def start(state):
    give_reply = False

    if state == States.STARTED:
        give_reply = True

    state = States.LISTENING

    return "I'm listening. When are you guys free?" , give_reply, state

def end(state):
    return "Let's see when we can meet", False , state

def do_nothing(state):
    return "Nothing to do" , False, state

def give_feedback(message, current_state):
    """

    :param message:
    :param current_state:
    :return: [feedback_message_str, should_respond_to_user_bool, new_state ]
    """
    if message == "start":
        return start(current_state)
    elif message == "end":
        return end(current_state)
    else:
        return do_nothing(current_state)