import traceback

from pending_event.pending_event_handler import PendingEventHandler

import sys
from helper.logger import Logger


log_message = Logger.get("apimtd", Logger.Level.INFO, sys.stdout)

log_debug = log_message.debug
log_info = log_message.info
log_warning = log_message.warning
log_error = log_message.error


def api_put(input_req):
    log_info(f"request put: {input_req}")
    pending_event_handler = PendingEventHandler()
    return pending_event_handler.put(input_req)

def api_pick(tag: str = ""):
    log_info(f"request pick: {tag}")
    pending_event_handler = PendingEventHandler()
    return pending_event_handler.pick(tag)

def api_cancel(stuff: dict):
    log_info(f"request cancle: {stuff}")
    pending_event_handler = PendingEventHandler()
    return pending_event_handler.cancel(stuff)

def api_get_list(tag: str = ""):
    log_info(f"request cancle: {tag}")
    pending_event_handler = PendingEventHandler()
    return pending_event_handler.get_list(tag)

def api_reset(tag: str):
    log_info(f"request reset: {tag}")
    pass
