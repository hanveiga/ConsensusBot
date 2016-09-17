from enum import Enum

class States(Enum):
    STARTED    = 1  # Initial state of bot
    LISTENING  = 2  # Bot listening for dates
    REQUESTING = 3  # Bot requesting approval

