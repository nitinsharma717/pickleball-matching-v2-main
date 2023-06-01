from pydantic import BaseModel
from typing import Optional, List


# TO support creation and update APIs
class CreateAndUpdatePlayer(BaseModel):
    firstName: str 
    middleInitials: Optional[str]
    lastName: str 
    email: str 
    rating: str


# TO support list and get APIs
class Player(CreateAndUpdatePlayer):
    id: int

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedPlayerInfo(BaseModel):
    limit: int
    offset: int
    data: List[Player]