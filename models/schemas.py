from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# PLAYER SCHEMAS
class CreateAndUpdatePlayer(BaseModel):
    firstName: str 
    middleInitials: Optional[str]
    lastName: str 
    email: str 
    rating: str
    win: str
    loss: str

class Player(CreateAndUpdatePlayer):
    id: int

    class Config:
        orm_mode = True


class PaginatedPlayerInfo(BaseModel):
    limit: int
    offset: int
    data: List[Player]


# MATCH SCHEMAS
class CreateAndUpdateMatch(BaseModel):
    opponent1: int; 
    opponent2: int; 
    score: str 
    winner: int 
    date: datetime
    location: str

class Match(CreateAndUpdateMatch):
    id: int

    class Config:
        orm_mode = True


class PaginatedMatchInfo(BaseModel):
    limit: int
    offset: int
    data: List[Match]