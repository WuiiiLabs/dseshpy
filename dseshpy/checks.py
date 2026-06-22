from discord import (
    VoiceChannel,
    CategoryChannel,
    VoiceState
)
from typing import Union, Optional

def is_vc_in_category(category: Union[CategoryChannel, int], channel: Union[VoiceChannel, int]) -> bool:
    """Checks if a voice channel belongs to a specific category."""
    if not category or not channel:
        return False
        
    cat_id = category.id if hasattr(category, 'id') else int(category)
    
    if hasattr(channel, 'category_id'):
        return channel.category_id == cat_id
    
    return False

def get_channel_status(state: VoiceState) -> bool:
    """Checks if a user is currently in a voice channel."""
    return state.channel is not None

def get_session_status(state: VoiceState, session_category: Union[CategoryChannel, int]) -> bool:
    """Checks if a user's voice state is within a study session category."""
    if not get_channel_status(state):
        return False
    return is_vc_in_category(session_category, state.channel)

def is_before_study_session(before: VoiceState, session_category: Union[CategoryChannel, int]) -> bool:
    """Checks if a user was in a study session before the transition."""
    return get_session_status(before, session_category)

def is_after_study_session(after: VoiceState, session_category: Union[CategoryChannel, int]) -> bool:
    """Checks if a user is in a study session after the transition."""
    return get_session_status(after, session_category)

def is_session_cam(state: VoiceState) -> bool:
    """Checks if a user's camera is active in their voice state."""
    return bool(state.self_video)

def is_session_ss(state: VoiceState) -> bool:
    """Checks if a user is screen sharing in their voice state."""
    return bool(state.self_stream)

def is_session_activity(state: VoiceState) -> bool:
    """Checks if a user has any activity (cam or screen share) in their voice state."""
    return is_session_cam(state) or is_session_ss(state)

def is_activity_started(before: VoiceState, after: VoiceState) -> bool:
    """Checks if a user started any activity (cam or screen share)."""
    return not is_session_activity(before) and is_session_activity(after)

def is_activity_stopped(before: VoiceState, after: VoiceState) -> bool:
    """Checks if a user stopped any activity (cam or screen share)."""
    return is_session_activity(before) and not is_session_activity(after)

def get_channel_id(state: VoiceState) -> Optional[str]:
    """Returns the channel ID of the voice state if it exists."""
    return str(state.channel.id) if state.channel else None
