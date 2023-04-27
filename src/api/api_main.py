from fastapi import FastAPI
from typing import List

from api.api_method import (
    api_put,
    api_pick,
    api_cancel,
    api_get_list,
)

from api.api_data_type import PendingQueue, PendingApiResult, PendingStuff
from pending_event.pending_event_handler import PendingEventHandler


fast_api = FastAPI(
    title="PendingQueue Serivce API",
    description="This service registers pending queues and manages registered ones.",
    contact={
        "name": "hatiolab",
        "url": "https://www.hatiolab.com",
        "email": "jinwon@hatiolab.com",
    },
)


@fast_api.on_event("startup")
async def startup_event():
    schedule_handler = PendingEventHandler()
    schedule_handler.initialize()


@fast_api.on_event("shutdown")
async def shutdown_event():
    pass


@fast_api.post("/pending-event")
async def put_pending_queue(inputs: PendingQueue) -> PendingApiResult:
    """
    register a schedule event
    """
    return {"event": api_put(inputs.dict())}

@fast_api.get("/pending-event")
async def pick_pending_queue(
    tag: str = "",
) -> PendingApiResult:
    """
    list all registered events
    """
    return {"event": api_pick(tag)}

@fast_api.get("/pending-events")
async def get_pending_list(
    tag: str = "",
) -> List[PendingQueue]:
    """
    get the list of pending events
    """
    return api_get_list(tag)

@fast_api.post("/cancel")
async def delete_pending_queues(pending_stuff: PendingStuff) -> PendingApiResult:
    """
    delete pending events
    """
    cancel_input = pending_stuff.dict()
    return {"event": api_cancel(cancel_input["stuff"])}




