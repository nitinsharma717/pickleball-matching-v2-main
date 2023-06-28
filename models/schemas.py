from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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
    notes: str


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
    status: str
    opponent1Name: str
    opponent2Name: str
    winnerName: str

class Match(CreateAndUpdateMatch):
    id: int

    class Config:
        orm_mode = True


class PaginatedMatchInfo(BaseModel):
    limit: int
    offset: int
    data: List[Match]



class TeamField(BaseModel):
    player1: int
    player2: int
class CreateAndUpdateDoublesMatch(BaseModel):
    team1: Dict[str, int]
    team2: Dict[str, int]
    score: str 
    winner: Dict[str, int]
    date: datetime
    location: str
    status: str
    team1Name: str
    team2Name: str
    winnerName: str

class DoublesMatch(CreateAndUpdateDoublesMatch):
    id: int

    class Config:
        orm_mode = True


class PaginatedDoublesMatchInfo(BaseModel):
    limit: int
    offset: int
    data: List[DoublesMatch]