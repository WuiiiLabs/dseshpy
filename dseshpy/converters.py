"""
Converters.py
===

This file provides translators of repeated checkins.
"""
from discord import VoiceState, CategoryChannel
from checks import (
    isVcInCategory
)

def convStateToActivity(
    before: VoiceState, 
    after: VoiceState, 
    sessionCategory: CategoryChannel
):
    details = {}
    if before.channel:
        channelTransition = "1"
        details['beforeChannel'] = str(before.channel.id)

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

    details["channelTransitions"] = channelTransition
    details["studyTransition"] = studyTransition
    return details