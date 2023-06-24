from typing import List
from sqlalchemy.orm import Session
from exceptions.exceptions import MatchInfoAlreadyExistError, MatchInfoNotFoundError, MatchInfoInvalid
from models.models import MatchInfo
from models.schemas import CreateAndUpdateMatch
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

    match_info.opponent1 = info_update.opponent1
    match_info.opponent2 = info_update.opponent2
    match_info.score = info_update.score
    match_info.winner = info_update.winner
    match_info.date = info_update.date
    match_info.location = info_update.location

    session.commit()
    session.refresh(match_info)

    return match_info


def delete_match_info(session: Session, _id: int):
    match_info = get_match_info_by_id(session, _id)
    if match_info is None:
        raise MatchInfoNotFoundError

    session.delete(match_info)
    session.commit()
