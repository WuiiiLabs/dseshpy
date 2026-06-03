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

        if isVcInCategory(
            category=sessionCategory, 
            channel=before.channel
        ):
            studyTransition = "1"
        else:
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

    return {
        "channelTransitions": channelTransition,
        "studyTransition": studyTransition,
        "details": {}
    }