import os
import json
from deepdiff import DeepDiff
from datetime import datetime, timezone
from fastapi import HTTPException

from config import Config
from direct_queue.local_queue import LocalQueue
from direct_queue.pg_queue import PGQueue


import sys
from helper.logger import Logger

log_message = Logger.get("pndevt", Logger.Level.INFO, sys.stdout)

log_debug = log_message.debug
log_info = log_message.info
log_warning = log_message.warning
log_error = log_message.error


class PendingEventHandler:
    # singleton constructor set
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # to be called once
        cls = type(self)
        if not hasattr(cls, "_init"):
            try:
                # TODO: need to the generalization of schedule_queue creation...
                (queue_type, queue_info) = Config.queue_info()
                if queue_type == "local":
                    self.pending_queue_db = LocalQueue(queue_info)
                elif queue_type == "pg":
                    self.pending_queue_db = PGQueue(queue_info)
                
                cls._init = True
            except Exception as ex:
                raise HTTPException(status_code=500, detail=f"Exception: {ex}")

    def initialize(self):
        try:
            log_info("initialization done..")
        except Exception as ex:
            log_error(f"Initializaiton Error: {ex}")

    def put(self, pending_event: dict):
        try:
            # TODO: check the duplicated event here...
            due = pending_event.get("due")
            assert type(due) == int
            # store the updated schedule event
            self.pending_queue_db.put(due, pending_event)
            return pending_event
        except Exception as ex:
            print(f"Exception: {ex}")
            raise HTTPException(status_code=500, detail=f"Exception: {ex}")
        
    def pick(self, tag= ""):
        try:
            toppick = {}
            now = datetime.now().timestamp()
            pending_list = self.pending_queue_db.get_key_value_list()
            for pending in pending_list:
                (pending_key, pending_event) = pending
                pending_key = int(pending_key)

                # TODO: need to check pending_list is sorted by key
                if pending_key > now:
                    break

                if pending_event["tag"] != tag:
                    continue

                if not toppick or toppick["priority"] < pending_event["priority"]:
                    toppick = pending_event
            
            self.pending_queue_db.pop(toppick["due"]) if toppick else None

            if not toppick:
                raise ValueError
            return toppick
        except ValueError as ex:
            raise HTTPException(status_code=404, detail=f"Pending event not found")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Exception: {ex}")

    def cancel(self, stuff: dict):
        try:
            pending_key_list = self.pending_queue_db.get_key_value_list()
            for pending in pending_key_list:
                (pending_key, pending_event) = pending
                if DeepDiff(stuff, pending_event["stuff"], ignore_order=True) == {}:
                    self.pending_queue_db.pop(pending_key)
                    return pending_event
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Exception: {ex}")
    
    def reset(self, tag: str):
        reset_list = []
        try:
            pending_key_list = self.pending_queue_db.get_key_list()
            for pending in pending_key_list:
                pending_stuff = json.loads(pending["stuff"])
                if pending_stuff["tag"] == tag:
                    self.pending_queue_db.pop(pending["key"])
                    reset_list.append(pending_stuff)
            return reset_list
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Exception: {ex}")
    
    def get_list(self, tag: str = ""):
        result_list = list()
        try:
            key_value_list = self.pending_queue_db.get_key_value_list()
            for key_value in key_value_list:
                (pending_key, pending_event) = key_value
                if tag == pending_event["tag"]:
                    result_list.append(pending_event)
            return result_list
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Exception: {ex}")


  
