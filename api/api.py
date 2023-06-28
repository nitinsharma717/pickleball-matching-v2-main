# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from pydantic import BaseModel
from crud.player import get_all_players, create_player, get_player_info_by_id, update_player_info, delete_player_info, get_player_info_by_email
from crud.match import get_all_matches, get_match_info_by_id, create_match, update_match_info, delete_match_info
from crud.doubles_match import get_all_doubles_matches, get_doubles_match_info_by_id, create_doubles_match, update_doubles_match_info, delete_doubles_match_info
from database.database import get_db
from exceptions.exceptions import PlayerInfoException, MatchInfoException, DoublesMatchException
from models.schemas import Player, CreateAndUpdatePlayer, PaginatedPlayerInfo, Match, PaginatedMatchInfo, CreateAndUpdateMatch, DoublesMatch, PaginatedDoublesMatchInfo, CreateAndUpdateDoublesMatch


router = APIRouter()

@router.get("/players", response_model=PaginatedPlayerInfo)
def list_players(limit: int = 1000, offset: int = 0, session: Session = Depends(get_db)):

    players_list = get_all_players(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": players_list}

    return response

@router.post("/players")
def add_player(player_info: CreateAndUpdatePlayer, session: Session = Depends(get_db)):
    try:
        player_info = create_player(session, player_info)
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

# API to create a list of players that will be a part of Session

# API to get the list of player info
@router.get("/matches", response_model=PaginatedMatchInfo)
def list_matches(limit: int = 1000, offset: int = 0, session: Session = Depends(get_db)):
    matches_list = get_all_matches(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": matches_list}
    return response

# API endpoint to add a player info to the database
@router.post("/matches")
def add_match(match_info: CreateAndUpdateMatch, session: Session = Depends(get_db)):
    try:
        match_info = create_match(session, match_info)
        return match_info
    except MatchInfoException as cie:
        raise HTTPException(**cie.__dict__)

@router.get("/matches/{match_id}", response_model=Match)
def get_match_info(match_id: int, session: Session = Depends(get_db)):
    try:
        match_info = get_match_info_by_id(session, match_id)
        return match_info
    except MatchInfoException as cie:
        raise HTTPException(**cie.__dict__)

@router.put("/matches/{match_id}", response_model=Match)
def update_match(match_id: int, new_info: CreateAndUpdateMatch, session: Session = Depends(get_db)):
    try:
        match_info = update_match_info(session, match_id, new_info)
        return match_info
    except MatchInfoException as cie:
        raise HTTPException(**cie.__dict__)

@router.delete("/matches/{match_id}", status_code = 204)
def delete_match(match_id: int, session: Session = Depends(get_db)):
    try:
        return delete_match_info(session, match_id)
    except MatchInfoException as cie:
        raise HTTPException(**cie.__dict__)



#################################### DOUBLES MATCHES ##################################################

@router.get("/doubles_matches", response_model = PaginatedDoublesMatchInfo)
def list_doubles_matches(limit: int = 1000, offset: int = 0, session: Session = Depends(get_db)):
    doubles_matches_list = get_all_doubles_matches(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": doubles_matches_list}
    return response
# API endpoint to add a player info to the database
@router.post("/doubles_matches")
def add_doubles_match(doubles_match_info: CreateAndUpdateDoublesMatch, session: Session = Depends(get_db)):
    try:
        doubles_match_info = create_doubles_match(session, doubles_match_info)
        return doubles_match_info
    except DoublesMatchException as cie:
        raise HTTPException(**cie.__dict__)

@router.get("/doubles_matches/{doubles_match_id}", response_model=DoublesMatch)
def get_doubles_match_info(doubles_match_id: int, session: Session = Depends(get_db)):
    try:
        doubles_match_info = get_doubles_match_info_by_id(session, doubles_match_id)
        return doubles_match_info
    except DoublesMatchException as cie:
        raise HTTPException(**cie.__dict__)

@router.put("/doubles_matches/{doubles_match_id}", response_model=DoublesMatch)
def update_doubles_match(doubles_match_id: int, new_info: CreateAndUpdateDoublesMatch, session: Session = Depends(get_db)):
    try:
        doubles_match_info = update_doubles_match_info(session, doubles_match_id, new_info)
        return doubles_match_info
    except DoublesMatchException as cie:
        raise HTTPException(**cie.__dict__)

@router.delete("/doubles_matches/{doubles_match_id}", status_code = 204)
def delete_doubles_match(doubles_match_id: int, session: Session = Depends(get_db)):
    try:
        return delete_doubles_match_info(session, doubles_match_id)
    except DoublesMatchException as cie:
        raise HTTPException(**cie.__dict__)