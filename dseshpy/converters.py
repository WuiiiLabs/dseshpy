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
    sessionCategory: CategoryChannel
):
    details = {}
    if before.channel:
        channelTransition = "1"
        details['beforeChannel'] = str(before.channel.id)

        if before.self_stream:
            streamTransition = "1"
        else:
            streamTransition = "0"

        if before.self_video:
            videoTransition = "1"
        else:
            videoTransition = "0"

        if before.self_video or before.self_stream:
            activityTransition = "1"
        else: 
            activityTransition = "0"

        if isVcInCategory(
            category=sessionCategory, 
            channel=before.channel
        ):
            studyTransition = "1"
        else:
            studyTransition = "0"

        if after.channel:
            channelTransition += "1"
            details['beforeChannel'] = str(before.channel.id)
            
            if isVcInCategory(
                category=sessionCategory, 
                channel=after.channel
            ):
                studyTransition += "1"
            else:
                studyTransition += "0"
        else:
            channelTransition += "0"
            studyTransition += "0"
    else:
        channelTransition = "0"
        studyTransition = "0"

        if after.channel:
            channelTransition += "1"

            if after.self_stream:
                streamTransition += "1"
            else:
                streamTransition += "0"

            if after.self_video:
                videoTransition += "1"
            else:
                videoTransition += "0"

            if after.self_video or after.self_stream:
                activityTransition += "1"
            else: 
                activityTransition += "0"
            
            if isVcInCategory(
                category=sessionCategory, 
                channel=after.channel
            ):
                studyTransition += "1"
            else:
                studyTransition += "0"
        else:
            channelTransition += "0"
            studyTransition += "0"

    details["transitions"] = {
        "channel": channelTransition,
        "study": studyTransition,
        "cam": videoTransition,
        "ss": streamTransition,
        "activity": activityTransition
    }
    details["member"] = member.id
    return details