from enum import Enum


class OrderStatus(Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    WAITING = "WAITING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"