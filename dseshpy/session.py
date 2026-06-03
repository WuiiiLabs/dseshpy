"""
session
===
Contains session details 
"""
from .drops import Routine
from datetime import datetime
from functools import lru_cache
from . import collections
from discord import VoiceState

# the below import and assigning is just for keyboard auto complete help
import pymongo
collections['session'] = pymongo.collection.Collection

class Session:
    """
    A session refers to a study session in discord vc
    It is uniquely known with its 
    It has various properties and functionalities

    Properties:
    ---
    - owner_id
    - guild_id
    - channel_id
    - members_count
    - member_limit
    - vc_level
    - vc_xp
    - rent_type
    - rent_amount
    - isCamSession
    - isScreenShareSession
    """
    def __init__(
        self,
        owner_id: str,
        guild_id: str, 
        channel_id: str,
        members_count: dict,
        members_limit: int,
        vc_level: int,
        vc_xp: int,
        rent_type: str,
        rent_amount: int,
        isCamSession: bool,
        isScreenShareSession: bool
    ):
        self.owner_id = owner_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.members_count = members_count
        self.members_limit = members_limit
        self.vc_level = vc_level
        self.vc_xp = vc_xp
        self.rent_type = rent_type
        self.rent_amount = rent_amount
        self.isCamSession = isCamSession
        self.isScreenShareSession = isScreenShareSession
        self.drops = {}
        self.logs = {}
        self.userCache = {}

    def addDropItem(self, name: str, interval: int, amount: int, factor: float, routine: Routine):
        self.drops[name] = {
            "interval": interval,
            "amount": amount,
            "factor": factor,
            "routine_": routine
        }
    
    def removeDropItem(self, name: str):
        self.drops.pop(name)

    def boost(self, xp: int):
        self.vc_xp += xp
        if self.vc_xp//1000 > self.vc_level*1000:
            self.vc_level += 1

    def isFull(self):
        if self.members_count + 1 > self.members_limit:
            return True
        else:
            return False

    def logActivity(self, before: VoiceState, after: VoiceState):
        pass

class SessionManager:
    """
    A discord study session needs to be managed properly. 
    Thus requiring a need of session manager.
    Individual sessions would be just like random in memory otherwise.

    Sessions can be managed at multiple levels.
    - Global Level
    - Guild Level

    Despite of what level, 
    Session Managers have certain properties and functionalities.

    Properties like:
    ---
    - session_count
    (lets just keep this for now)

    Functionalities like:
    - sync() : To sync to database
    """