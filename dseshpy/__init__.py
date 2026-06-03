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