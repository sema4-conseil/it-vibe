from enum import Enum

class MessageStatus(Enum):
    NEW = 1
    IN_PROGRESS = 2
    DONE = 3
    ARCHIVED = 4