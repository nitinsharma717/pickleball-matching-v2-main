from pydantic import BaseModel
from typing import Optional, List


# TO support creation and update APIs
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


