from typing import List
from sqlalchemy.orm import Session
from exceptions.exceptions import DoublesMatchAlreadyExistError, DoublesMatchException, DoublesMatchInvalidError, DoublesMatchNotFoundError
from crud.player import update_player_info, get_player_info_by_id
from models.models import DoublesMatchInfo
from models.schemas import CreateAndUpdateDoublesMatch, CreateAndUpdatePlayer


def get_all_doubles_matches(session: Session, limit: int, offset: int) -> List[DoublesMatchInfo]:
    return session.query(DoublesMatchInfo).offset(offset).limit(limit).all()


def get_doubles_match_info_by_id(session: Session, _id: int) -> DoublesMatchInfo:
    doubles_match_info = session.query(DoublesMatchInfo).get(_id)

    if doubles_match_info is None:
        raise DoublesMatchNotFoundError

    return doubles_match_info


def create_doubles_match(session: Session, doubles_match_info: CreateAndUpdateDoublesMatch) -> DoublesMatchInfo:
    doubles_match_info_dict = doubles_match_info.dict()

    for value in doubles_match_info_dict.values():
        if isinstance(value, str) and value.strip() == "":
            raise DoublesMatchInvalidError()


    new_doubles_match_info = DoublesMatchInfo(**doubles_match_info.dict())
    session.add(new_doubles_match_info)
    session.commit()
    session.refresh(new_doubles_match_info)
    return new_doubles_match_info




def update_doubles_match_info(session: Session, _id: int, info_update: CreateAndUpdateDoublesMatch) -> DoublesMatchInfo:
    doubles_match_info = get_doubles_match_info_by_id(session, _id)

    if doubles_match_info is None:
        raise DoublesMatchNotFoundError

    matchStatus = doubles_match_info.status

    doubles_match_info.team1 = info_update.team1
    doubles_match_info.team2 = info_update.team2
    doubles_match_info.score = info_update.score
    doubles_match_info.winner = info_update.winner
    doubles_match_info.date = info_update.date
    doubles_match_info.location = info_update.location
    doubles_match_info.status = info_update.status
    doubles_match_info.team1Name = info_update.team1Name
    doubles_match_info.team2Name = info_update.team2Name
    doubles_match_info.winnerName = info_update.winnerName

    winner_id = doubles_match_info.winner
    loser_id = doubles_match_info.team1 if doubles_match_info.winner != doubles_match_info.team1 else doubles_match_info.team2
    # Update the winner's wins and loser's losses
    first_winner_object = get_player_info_by_id(session=session, _id = winner_id['player1'])
    second_winner_object = get_player_info_by_id(session=session, _id = winner_id['player2'])
    first_loser_object = get_player_info_by_id(session=session, _id=loser_id['player1'])
    second_loser_object = get_player_info_by_id(session=session, _id=loser_id['player2'])

    if (matchStatus != "COMPLETED"):
        update_player_info(session, winner_id['player1'], CreateAndUpdatePlayer(
            firstName = first_winner_object.firstName,
            lastName = first_winner_object.lastName,
            email = first_winner_object.email,
            rating = first_winner_object.rating,
            middleInitials = first_winner_object.middleInitials,
            win = first_winner_object.win + 1,
            loss = first_winner_object.loss,
            notes = first_winner_object.notes
        ))

        update_player_info(session, winner_id['player2'], CreateAndUpdatePlayer(
            firstName = second_winner_object.firstName,
            lastName = second_winner_object.lastName,
            email = second_winner_object.email,
            rating = second_winner_object.rating,
            middleInitials = second_winner_object.middleInitials,
            win = second_winner_object.win + 1,
            loss = second_winner_object.loss,
            notes = second_winner_object.notes
        ))
        
        update_player_info(session, loser_id['player1'], CreateAndUpdatePlayer(
            firstName = first_loser_object.firstName,
            lastName = first_loser_object.lastName,
            email = first_loser_object.email,
            rating = first_loser_object.rating,
            middleInitials = first_loser_object.middleInitials,
            win = first_loser_object.win,
            loss = first_loser_object.loss + 1,
            notes = first_loser_object.notes
        ))

        update_player_info(session, loser_id['player2'], CreateAndUpdatePlayer(
            firstName = second_loser_object.firstName,
            lastName = second_loser_object.lastName,
            email = second_loser_object.email,
            rating = second_loser_object.rating,
            middleInitials = second_loser_object.middleInitials,
            win = second_loser_object.win,
            loss = second_loser_object.loss + 1,
            notes = second_loser_object.notes
        ))

    session.commit()
    session.refresh(doubles_match_info)

    return doubles_match_info


def delete_doubles_match_info(session: Session, _id: int):
    doubles_match_info = get_doubles_match_info_by_id(session, _id)
    if doubles_match_info is None:
        raise DoublesMatchNotFoundError

    session.delete(doubles_match_info)
    session.commit()
