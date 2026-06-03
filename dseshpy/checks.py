from discord import (
    VoiceChannel,
    CategoryChannel
)

def isVcInCategory(category: CategoryChannel, channel: VoiceChannel):
    return category.id == channel.category.id