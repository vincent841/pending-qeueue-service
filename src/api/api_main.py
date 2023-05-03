from fastapi import FastAPI
from typing import List

from api.api_method import (
    api_put,
    api_pick,
    api_get,
    api_cancel,
    api_get_list,
    api_reset
)

from api.api_data_type import PendingQueue, PendingApiResult, PendingStuff, PendingApiResults
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
    register a pending event
    
    """
    return {"event": api_put(inputs.dict())}

@fast_api.get("/pending-event/{id}")
async def get_pending_evebt(
    id: str = "",
) -> PendingQueue:
    """
    get the list of pending events with a specific tag
    
    """
    return api_get(id)


@fast_api.get("/pending-events")
async def get_pending_list(
    tag: str = "",
) -> List[PendingQueue]:
    """
    get the list of pending events with a specific tag
    
    """
    return api_get_list(tag)


@fast_api.post("/pending-queue/pick")
async def pick_pending_queue(
    tag: str = "",
) -> PendingApiResult:
    """
    pick a pending event considering both due and priority
    
    """
    return {"event": api_pick(tag)}


@fast_api.post("/pending-queue/cancel")
async def cacnel_pending_queues(pending_stuff: PendingStuff) -> PendingApiResult:
    """
    delete pending events
    """
    cancel_input = pending_stuff.dict()
    return {"event": api_cancel(cancel_input["stuff"])}


@fast_api.post("/pending-queue/reset")
async def reset_pending_queues(tag: str) -> PendingApiResults:
    """
    clear pending events with the specific tag
    """
    return {"events": api_reset(tag)}




