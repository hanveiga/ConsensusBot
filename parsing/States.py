from enum import Enum

class States(Enum):
    STARTED    = 1  # Initial state of bot
    LISTENING  = 2  # Bot listening for dates
    FINALIZING = 3  # Bot requesting approval

class Responses(Enum):
    AGREE      = 1
    DISAGREE   = 2
    FORFEIT    = 3

response_text = {
    Responses.AGREE    : "Yes",
    Responses.DISAGREE : "No",
    Responses.FORFEIT  : "You guys go on!",
}
