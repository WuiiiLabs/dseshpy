"""
Converters.py
===

This file provides translators of repeated checkins.
"""
from discord import (
    VoiceState, 
    CategoryChannel, 
    Member,
)
from checks import (
    isVcInCategory
)

def convStateToActivity(
    member: Member,
    before: VoiceState, 
    after: VoiceState, 
    session_category: CategoryChannel
):
    details = {}
    if before.channel:
        channel_transition = "1"
        details['beforeChannel'] = str(before.channel.id)

        if before.self_stream:
            stream_transition = "1"
        else:
            stream_transition = "0"

        if before.self_video:
            video_transition = "1"
        else:
            video_transition = "0"

        if before.self_video or before.self_stream:
            activity_transition = "1"
        else: 
            activity_transition = "0"

        if isVcInCategory(
            category=session_category, 
            channel=before.channel
        ):
            study_transition = "1"
        else:
            study_transition = "0"
        
        if after.channel:
            channel_transition += "1"
            details['beforeChannel'] = str(before.channel.id)
            
            if isVcInCategory(
                category=session_category, 
                channel=after.channel
            ):
                study_transition += "1"
            else:
                study_transition += "0"
        else:
            channel_transition += "0"
            study_transition += "0"
    else:
        channel_transition = "0"
        study_transition = "0"

        if after.channel:
            channel_transition += "1"

            if after.self_stream:
                stream_transition += "1"
            else:
                stream_transition += "0"

            if after.self_video:
                video_transition += "1"
            else:
                video_transition += "0"

            if after.self_video or after.self_stream:
                activity_transition += "1"
            else: 
                activity_transition += "0"
            
            if isVcInCategory(
                category=session_category, 
                channel=after.channel
            ):
                study_transition += "1"
            else:
                study_transition += "0"
        else:
            channel_transition += "0"
            study_transition += "0"

    details["transitions"] = {
        "channel": channel_transition,
        "study": study_transition,
        "cam": video_transition,
        "ss": stream_transition,
        "activity": activity_transition
    }
    details["user_id"] = member.id
    return details