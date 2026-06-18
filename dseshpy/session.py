"""
session
===
Contains session details 
"""
import asyncio
from .drops import Routine
from datetime import datetime
from . import collections
from converters import (
    convStateToActivity,
)
from discord import VoiceState, Member

# the below import and assigning is just for keyboard auto complete help
import pymongo
session = collections['session']
session_collection = pymongo.collection.Collection

class Session:
    """
    A session refers to a study session in discord vc
    """
    def __init__(
        self,
        owner_id: str,
        guild_id: str, 
        category_id: str,
        channel_id: str,
        members: dict = {},
        members_limit: int = None,
        members_count: dict = {
            "total": 0,
            "noact": 0,
            "ss": 0,
            "cam": 0
        },
        vc_level: int = 1,
        vc_xp: int = 0,
        rent_type: str = "free",
        rent_amount: int = 0,
        is_cam_session: bool = False,
        is_screen_share_session: bool = False,
        routine_callback_mean_time: int = 30
    ):
        self.owner_id = owner_id
        self.guild_id = guild_id
        self.category_id = category_id
        self.channel_id = channel_id
        
        self.members_count = members_count
        self.members_limit = members_limit
        self.vc_level = vc_level
        self.vc_xp = vc_xp
        self.rent_type = rent_type
        self.rent_amount = rent_amount
        self.is_cam_session = is_cam_session
        self.is_screen_share_session = is_screen_share_session
        
        self.members = members
        self.routine_callback_mean_time = routine_callback_mean_time

    async def manage(self, member: Member, before: VoiceState, after: VoiceState):
        activity_info = convStateToActivity(
            member=member,
            before=before,
            after=after,
            session_category=self.category_id
        )
        study_trans = activity_info["transitions"]["study"]

        # join the study channel
        if study_trans == '01':
            self.transfer_session(activity=activity_info)
        elif study_trans == '11':
            self.add_to_session(activity=activity_info)
        elif study_trans == '10':
            self.remove_from_session(activity=activity_info)

    def add_to_session(self, activity: dict):
        user_id = activity["user_id"]
        is_ss = activity['transitions']['ss'][-1] == '1'
        is_cam = activity['transitions']['cam'][-1] == '1'
        is_first_member = self.members_count["total"] == 0

        # Creating user data payload
        user_data = {
            "start_time": datetime.now(),
            "cam": is_cam,
            "ss": is_ss,
            "session_goal": ""
        }

        try:
            # If this fails, we don't update RAM, keeping them in sync
            if is_first_member:
                # Use insert_one or update_one with upsert
                # Include the initial counts here
                update_query = {
                    "$set": {
                        "members": {user_id: user_data},
                        "members_count": {
                            "total": 1,
                            "ss": is_ss,
                            "cam": is_cam,
                            "noact": 1 if (not is_ss and not is_cam) else 0
                        }
                    }
                }
            else:
                update_query = {
                    "$inc": {
                        "members_count.total": 1,
                        "members_count.ss": is_ss,
                        "members_count.cam": is_cam,
                        "members_count.noact": 1 if (not is_ss and not is_cam) else 0
                    },
                    "$set": {f"members.{user_id}": user_data}
                }

            session_collection.update_one(
                {"channel_id": activity['channel_id'], "guild_id": activity["guild_id"]},
                update_query,
                upsert=True
            )

            # If DB succeeds, update RAM (The only way to ensure they stay together)
            self.members[user_id] = user_data
            self.members_count["total"] += 1
            if is_ss: self.members_count["ss"] += 1
            if is_cam: self.members_count["cam"] += 1
            if not is_ss and not is_cam: self.members_count["noact"] += 1

        except Exception as e:
            print(f"Failed to add member to session: {e}")
            # Rethrow so the caller knows the state is unstable
            raise  
 
    def complete_session(self, activity: dict):
        pass

    def transfer_session(self, activity: dict):
        pass

    def is_full(self):
        return self.members_count["total"] >= self.members_limit

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
