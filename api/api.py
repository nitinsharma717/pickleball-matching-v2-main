# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from pydantic import BaseModel
from crud.crud import get_all_players, create_player, get_player_info_by_id, update_player_info, delete_player_info, get_player_info_by_email
from crud.crud import get_all_matches, get_match_info_by_id, create_match, update_match_info, delete_match_info
from database.database import get_db
from exceptions.exceptions import PlayerInfoException
from models.schemas import Player, CreateAndUpdatePlayer, PaginatedPlayerInfo, Match, PaginatedMatchInfo, CreateAndUpdateMatch


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
    
    # @router.post("/matches")
    # def create_matches(self, email_list: list[str], isDouble: bool):
        try:
            match_info = create_player_pairings(self.session, email_list, isDouble)
            return match_info
        except PlayerInfoException as cie:
            raise HTTPException(**cie.__dict__)
    
    # @router.post("/tournament")
    # def create_tournament(self, email_list: list[str]):
        try:
            match_info = create_tournament(self.session, email_list)
            return match_info
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

# API to create a list of players that will be a part of Session


# API to get the list of player info
@router.get("/matches", response_model=PaginatedMatchInfo)
def list_matches(limit: int = 10, offset: int = 0, session: Session = Depends(get_db)):
    matches_list = get_all_matches(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": matches_list}
    return response

# API endpoint to add a player info to the database
@router.post("/matches")
def add_match(match_info: CreateAndUpdateMatch, session: Session = Depends(get_db)):
    try:
        match_info = create_match(session, match_info)
        return match_info
    except PlayerInfoException as cie:
        raise HTTPException(**cie.__dict__)