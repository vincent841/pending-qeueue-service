from pydantic import BaseModel, Field
from typing import List


"""
PendingQueue Type Definitions

"""

class PendingQueue(BaseModel):
    due: int = Field(default=0, title= "timestamp to be fired")
    priority: int = Field(default=0, title="queue priority")
    tag: str = Field(default="", title= "the registered timestamp")
    stuff: dict = Field(default={}, title="user data")

class PendingApiResult(BaseModel):
    event: PendingQueue = Field(default=None, title="pending event")

class PendingApiResults(BaseModel):
    events: List[PendingQueue] = Field(default=[], title="pending event list")


class PendingStuff(BaseModel):
    stuff: dict