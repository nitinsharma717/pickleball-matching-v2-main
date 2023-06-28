from typing import List
from sqlalchemy.orm import Session
from exceptions.exceptions import MatchInfoAlreadyExistError, MatchInfoNotFoundError, MatchInfoInvalid
from crud.player import update_player_info, get_player_info_by_id
from models.models import MatchInfo
from models.schemas import CreateAndUpdateMatch, CreateAndUpdatePlayer
from email_validator import validate_email, EmailNotValidError


def get_all_matches(session: Session, limit: int, offset: int) -> List[MatchInfo]:
    return session.query(MatchInfo).offset(offset).limit(limit).all()


def get_match_info_by_id(session: Session, _id: int) -> MatchInfo:
    match_info = session.query(MatchInfo).get(_id)

    if match_info is None:
        raise MatchInfoNotFoundError

    return match_info


def create_match(session: Session, match_info: CreateAndUpdateMatch) -> MatchInfo:
    match_info_dict = match_info.dict()

    for value in match_info_dict.values():
        if isinstance(value, str) and value.strip() == "":
            raise MatchInfoInvalid()


    new_match_info = MatchInfo(**match_info.dict())
    session.add(new_match_info)
    session.commit()
    session.refresh(new_match_info)
    return new_match_info




def update_match_info(session: Session, _id: int, info_update: CreateAndUpdateMatch) -> MatchInfo:
    match_info = get_match_info_by_id(session, _id)

    if match_info is None:
        raise MatchInfoNotFoundError

    matchStatus = match_info.status

    match_info.opponent1 = info_update.opponent1
    match_info.opponent2 = info_update.opponent2
    match_info.score = info_update.score
    match_info.winner = info_update.winner
    match_info.date = info_update.date
    match_info.location = info_update.location
    match_info.status = info_update.status
    match_info.opponent1Name = info_update.opponent1Name
    match_info.opponent2Name = info_update.opponent2Name
    match_info.winnerName = info_update.winnerName


    winner_id = match_info.winner
    loser_id = match_info.opponent1 if match_info.winner != match_info.opponent1 else match_info.opponent2

    # Update the winner's wins and loser's losses
    winner_object = get_player_info_by_id(session=session, _id = winner_id)
    loser_object = get_player_info_by_id(session=session, _id = loser_id)

    if (matchStatus != "COMPLETED"):
        update_player_info(session, winner_id, CreateAndUpdatePlayer(
            firstName = winner_object.firstName,
            lastName = winner_object.lastName,
            email = winner_object.email,
            rating = winner_object.rating,
            middleInitials = winner_object.middleInitials,
            win = winner_object.win + 1,
            loss = winner_object.loss,
            notes = winner_object.notes
        ))
        
        update_player_info(session, loser_id, CreateAndUpdatePlayer(
            firstName = loser_object.firstName,
            lastName = loser_object.lastName,
            email = loser_object.email,
            rating = loser_object.rating,
            middleInitials = loser_object.middleInitials,
            win = loser_object.win,
            loss = loser_object.loss + 1,
            notes = loser_object.notes
        ))
    
    session.commit()
    session.refresh(match_info)

    return match_info


def delete_match_info(session: Session, _id: int):
    match_info = get_match_info_by_id(session, _id)
    if match_info is None:
        raise MatchInfoNotFoundError

    session.delete(match_info)
    session.commit()
