from enum import Enum

class MessageStatus(Enum):
    NEW = 1
    IN_PROGRESS = 2
    DONE = 3
    ARCHIVED = 4

    @classmethod
    def get_valid_status(cls, status_name: str) -> 'MessageStatus | None':
        try:
            return cls[status_name]
        except KeyError:
            return None