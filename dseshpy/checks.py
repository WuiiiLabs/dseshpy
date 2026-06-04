from discord import (
    VoiceChannel,
    CategoryChannel
)
from typing import Union

def isVcInCategory(category: Union[CategoryChannel, int], channel: Union[VoiceChannel, int]):
    """Checks if a voice channel belongs to a specific category."""
    catID = category.id if hasattr(category, 'id') else int(category)
    
    if hasattr(channel, 'category_id'):
        return channel.category_id == catID
    
    return False
