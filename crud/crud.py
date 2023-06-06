# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions.exceptions import PlayerInfoInfoAlreadyExistError, PlayerInfoNotFoundError, PlayerInfoInvalid, EmailInvalid
from models.models import PlayerInfo
from models.schemas import CreateAndUpdatePlayer
from email_validator import validate_email, EmailNotValidError

# Function to get list of Player info
def get_all_players(session: Session, limit: int, offset: int) -> List[PlayerInfo]:
    return session.query(PlayerInfo).offset(offset).limit(limit).all()


# Function to  get info of a particular player
def get_player_info_by_id(session: Session, _id: int) -> PlayerInfo:
    player_info = session.query(PlayerInfo).get(_id)

    if player_info is None:
        raise PlayerInfoNotFoundError

    return player_info

def get_player_info_by_email(session: Session, _email: str) -> PlayerInfo:
    player_info = session.query(PlayerInfo).filter_by(email=_email).one()
    if player_info is None:
        raise PlayerInfoNotFoundError

    return player_info

# Function to add a new player info to the database
def create_player(session: Session, player_info: CreateAndUpdatePlayer) -> PlayerInfo:
    player_details = session.query(PlayerInfo).filter(PlayerInfo.email == player_info.email).first()
    if player_details is not None:
        raise PlayerInfoInfoAlreadyExistError
    
    player_info_dict = player_info.dict()

    try:
        validate_email(player_info_dict['email'])
    except EmailNotValidError:
        raise EmailInvalid()
    
    for value in player_info_dict.values():
        if isinstance(value, str) and value.strip() == "":
            raise PlayerInfoInvalid()


    new_player_info = PlayerInfo(**player_info.dict())
    session.add(new_player_info)
    session.commit()
    session.refresh(new_player_info)
    return new_player_info


# Function to update details of the player
def update_player_info(session: Session, _id: int, info_update: CreateAndUpdatePlayer) -> PlayerInfo:
    player_info = get_player_info_by_id(session, _id)

    if player_info is None:
        raise PlayerInfoNotFoundError
    
    player_info.firstName = info_update.firstName
    player_info.lastName = info_update.lastName
    player_info.email = info_update.email
    player_info.rating = info_update.rating
    player_info.middleInitials = info_update.middleInitials

    session.commit()
    session.refresh(player_info)

    return player_info


# Function to delete a player info from the db
def delete_player_info(session: Session, _id: int):
    player_info = get_player_info_by_id(session, _id)

    if player_info is None:
        raise PlayerInfoNotFoundError

    # Nitin
    session.delete(player_info)
    session.commit()

# function to create matches between people by email
def create_player_pairings(session: Session, _emails: list, _isDouble: bool):
    players_info = []
    for email in _emails:
        players_info.append(get_player_info_by_email(session, email))
    return create_matches(players=players_info, isDouble=_isDouble)

def create_matches(players, isDouble = False):
    if isDouble:
        sorted_players = sorted(players, key=lambda x: x.rating, reverse=True)
        matches = []
        while len(sorted_players) >= 4:
            pair1 = sorted_players.pop(0)
            pair2 = sorted_players.pop(0)
            pair3 = sorted_players.pop(0)
            pair4 = sorted_players.pop(0)
            matches.append([[pair1, pair4], [pair2, pair3]])
        return matches

    sorted_players = sorted(players, key=lambda x: x.rating, reverse=True)
    matches = []
    while len(sorted_players) >= 2:
        pair1 = sorted_players.pop(0)
        pair2 = sorted_players.pop(0)
        matches.append([pair1, pair2])

    return matches

def create_tournament(session: Session, _emails: list):
    players_info = []
    for email in _emails:
        players_info.append(get_player_info_by_email(session, email))
    sorted_players = sorted(players_info, key=lambda x: x.rating, reverse=True)
    matches = []
    while len(sorted_players) >= 2:
        pair1 = sorted_players.pop(0)
        pair2 = sorted_players.pop()
        matches.append([pair1, pair2])
    return matches






