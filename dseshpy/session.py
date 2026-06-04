"""
session
===
Contains session details 
"""
import asyncio
from .drops import Routine
from datetime import datetime
from . import collections, converters
from discord import VoiceState, Member

# the below import and assigning is just for keyboard auto complete help
import pymongo
collections['session'] = pymongo.collection.Collection

class Session:
    """
    A session refers to a study session in discord vc
    """
    def __init__(
        self,
        ownerID: str,
        guildID: str, 
        categoryID: str,
        channelID: str,
        membersLimit: int,
        vcLevel: int = 1,
        vcXP: int = 0,
        rentType: str = "none",
        rentAmount: int = 0,
        isCamSession: bool = False,
        isScreenShareSession: bool = False
    ):
        self.ownerID = ownerID
        self.guildID = guildID
        self.categoryID = categoryID
        self.channelID = channelID
        
        # {total, noacc, ss, cam}
        self.membersCount = {
            "total": 0,
            "noacc": 0,
            "ss": 0,
            "cam": 0
        }
        self.membersLimit = membersLimit
        self.vcLevel = vcLevel
        self.vcXP = vcXP
        self.rentType = rentType
        self.rentAmount = rentAmount
        self.isCamSession = isCamSession
        self.isScreenShareSession = isScreenShareSession
        
        self.drops = {} 
        self.memberRegistry = {} # {userID: currentState}
        self.routineTask = None

    def addDropItem(self, name: str, interval: int, amount: int, factor: float, routine: Routine):
        self.drops[name] = {
            "interval": interval,
            "amount": amount,
            "factor": factor,
            "routine_": routine
        }
    
    def removeDropItem(self, name: str):
        self.drops.pop(name, None)

    async def dropperRoutine(self, channel):
        """
        Centralized loop for all drops. 
        Uses the channel object to send drop notifications.
        """
        try:
            while True:
                # Logic to iterate over self.drops and check intervals with variance
                await asyncio.sleep(60) # Placeholder sleep
                # print(f"Checking drops in {channel.name}...")
                pass
        except asyncio.CancelledError:
            # Cleanup when the last user leaves
            pass

    def startRoutine(self, channel):
        """Starts the routineTask if it is not already running"""
        if not self.routineTask:
            self.routineTask = asyncio.create_task(self.dropperRoutine(channel))

    def stopRoutine(self):
        """Cancels the routineTask and cleans up"""
        if self.routineTask:
            self.routineTask.cancel()
            self.routineTask = None

    async def manage(self, member, before: VoiceState, after: VoiceState):
        """
        Orchestrates member entry/exit and state changes.
        Updates membersCount: {total, noacc, ss, cam}
        """
        activityInfo = converters.convStateToActivity(
            before=before,
            after=after,
            sessionCategory=self.categoryID
        )

        transition = activityInfo.get("studyTransition", "00")
        userID = str(member.id)

        # 1. Handle Join
        if transition == "01":
            self.membersCount["total"] += 1
            # Determine initial state (cam/ss/noacc) and update membersCount
            # self.memberRegistry[userID] = newState

            if self.membersCount["total"] == 1:
                self.startRoutine(after.channel)

        # 2. Handle Leave
        elif transition == "10":
            self.membersCount["total"] -= 1
            # Retrieve last state from memberRegistry and decrement that specific count
            # self.memberRegistry.pop(userID)

            if self.membersCount["total"] == 0:
                self.stopRoutine()

        # 3. Handle State Toggle (Stay in Study VC)
        elif transition == "11":
            # Logic to detect cam/ss toggle and shift counts between noacc, ss, and cam
            pass


    def isFull(self):
        return self.membersCount["total"] >= self.membersLimit

    def boost(self, xp: int):
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
    pass
