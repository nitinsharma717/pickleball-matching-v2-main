from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
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


class SinglesMatchInfo(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    player1 = Column(String, nullable=False)
    player2 = Column(String, nullable=False)
    score = Column(String, nullable = True)
    winner = Column(String, nullable = True)
    

