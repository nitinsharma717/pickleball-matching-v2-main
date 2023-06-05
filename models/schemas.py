from pydantic import BaseModel
from typing import Optional, List


# TO support creation and update APIs
class CreateAndUpdatePlayer(BaseModel):
    firstName: str 
    middleInitials: Optional[str]
    lastName: str 
    email: str 
    rating: str


class Player(CreateAndUpdatePlayer):
    id: int

    class Config:
        orm_mode = True


class PaginatedPlayerInfo(BaseModel):
    limit: int
    offset: int
    data: List[Player]

class SinglesMatch(BaseModel):
    player1: Player
    player2: Player
    score: str
    winner: Player    

class DoublesMatch(BaseModel):
    player1: List[Player]
    player2: List[Player]
    score: str
    winner: Player    
    