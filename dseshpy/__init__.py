"""
Deshpy
===
This package is made for handling discord study sessions
---
Package under development. ^.^

---
Thank you
"""
from pymongo.collection import Collection as _Collection
collections = {}

def initialize(
    session_collection: _Collection
):
    collections['session'] = session_collection

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