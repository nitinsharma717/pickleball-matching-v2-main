from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum, DateTime, JSON
from database.database import Base
from sqlalchemy.orm import validates
import enum



class PlayerInfo(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    middleInitials = Column(String, nullable=True)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    win = Column(Integer, nullable = True)
    loss = Column(Integer, nullable = True)
    notes = Column(String, nullable = True)


class MatchInfo(Base):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True, index=True)
    opponent1 = Column(Integer, nullable=False)
    opponent2 = Column(Integer, nullable=False)
    score = Column(String, nullable = False)
    winner = Column(Integer, nullable = False)
    date = Column(DateTime, nullable = False)
    location = Column(String, nullable = False)
    status = Column(String, nullable = False)
    opponent1Name = Column(String, nullable = False)
    opponent2Name = Column(String, nullable = False)
    winnerName = Column(String, nullable = False)

class DoublesMatchInfo(Base):
    __tablename__ = "doubles-match"
    id = Column(Integer, primary_key=True, index=True)
    team1 = Column(JSON, nullable=False)
    team2 = Column(JSON, nullable=False)
    score = Column(String, nullable = False)
    winner = Column(JSON, nullable = False)
    date = Column(DateTime, nullable = False)
    location = Column(String, nullable = False)
    status = Column(String, nullable = False)
    team1Name = Column(String, nullable = False)
    team2Name = Column(String, nullable = False)
    winnerName = Column(String, nullable = False)
    

