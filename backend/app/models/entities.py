from datetime import datetime
from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    game: Mapped[str] = mapped_column(String(30), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_rub: Mapped[int] = mapped_column(BigInteger, nullable=False)
    registration_closes_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    canceled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    teams: Mapped[list["Team"]] = relationship(back_populates="tournament", cascade="all, delete-orphan")
    matches: Mapped[list["Match"]] = relationship(back_populates="tournament", cascade="all, delete-orphan")
    __table_args__ = (CheckConstraint("capacity IN (8, 16)", name="ck_tournament_capacity"), CheckConstraint("prize_rub >= 0", name="ck_tournament_prize"))


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    tournament: Mapped[Tournament] = relationship(back_populates="teams")
    players: Mapped[list["Player"]] = relationship(back_populates="team", cascade="all, delete-orphan", lazy="selectin")
    __table_args__ = (UniqueConstraint("tournament_id", "name", name="uq_team_name_per_tournament"),)


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    nickname: Mapped[str] = mapped_column(String(80), nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_captain: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    team: Mapped[Team] = relationship(back_populates="players")
    __table_args__ = (UniqueConstraint("team_id", "nickname", name="uq_player_nickname_per_team"),)


class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False, index=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    home_score: Mapped[int | None] = mapped_column(Integer)
    away_score: Mapped[int | None] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tournament: Mapped[Tournament] = relationship(back_populates="matches")
    __table_args__ = (
        CheckConstraint("home_team_id <> away_team_id", name="ck_match_teams_different"),
        CheckConstraint("home_score IS NULL OR home_score >= 0", name="ck_match_home_score"),
        CheckConstraint("away_score IS NULL OR away_score >= 0", name="ck_match_away_score"),
    )
