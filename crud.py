# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import PlayerInfoInfoAlreadyExistError, PlayerInfoNotFoundError, PlayerInfoInvalid, EmailInvalid
from models import PlayerInfo
from schemas import CreateAndUpdatePlayer
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

    session.delete(player_info)
    session.commit()