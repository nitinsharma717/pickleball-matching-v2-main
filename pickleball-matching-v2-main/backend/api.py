# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_players, create_player, get_player_info_by_id, update_player_info, delete_player_info, get_player_info_by_email
from database import get_db
from exceptions import PlayerInfoException
from schemas import Player, CreateAndUpdatePlayer, PaginatedPlayerInfo

router = APIRouter()


@cbv(router)
class Players:
    session: Session = Depends(get_db)

    # API to get the list of player info
    @router.get("/players", response_model=PaginatedPlayerInfo)
    def list_players(self, limit: int = 10, offset: int = 0):

        players_list = get_all_players(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": players_list}

        return response

    # API endpoint to add a player info to the database
    @router.post("/players")
    def add_player(self, player_info: CreateAndUpdatePlayer):

        try:
            player_info = create_player(self.session, player_info)
            return player_info
        except PlayerInfoException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular player
@router.get("/players/{player_id}", response_model=Player)
def get_player_info(player_id: int, session: Session = Depends(get_db)):
    try:
        player_info = get_player_info_by_id(session, player_id)
        return player_info
    except PlayerInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
@router.get("/players/email/{player_email}", response_model=Player)
def get_player_info(player_email: str, session: Session = Depends(get_db)):
    try:
        player_info = get_player_info_by_email(session, player_email)
        return player_info
    except PlayerInfoException as cie:
        raise HTTPException(**cie.__dict__)



# API to update a existing player info
@router.put("/players/{player_id}", response_model=Player)
def update_player(player_id: int, new_info: CreateAndUpdatePlayer, session: Session = Depends(get_db)):

    try:
        player_info = update_player_info(session, player_id, new_info)
        return player_info
    except PlayerInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a player info from the data base
@router.delete("/players/{player_id}", status_code = 204)
def delete_player(player_id: int, session: Session = Depends(get_db)):
    try:
        return delete_player_info(session, player_id)
    except PlayerInfoException as cie:
        raise HTTPException(**cie.__dict__)
