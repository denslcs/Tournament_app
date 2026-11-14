from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

Game = Literal["dota2", "cs2", "lol", "valorant", "fortnite"]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TournamentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    game: Game
    capacity: Literal[8, 16]
    prize_rub: int = Field(ge=0)
    starts_at: datetime
    registration_closes_at: datetime
    ends_at: datetime | None = None

    @field_validator("starts_at", "registration_closes_at", "ends_at")
    @classmethod
    def timezone_required(cls, value):
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Дата и время должны содержать часовой пояс, например +03:00")
        return value

    @model_validator(mode="after")
    def check_dates(self):
        if self.registration_closes_at > self.starts_at:
            raise ValueError("Регистрация должна закрыться не позднее начала турнира")
        if self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("Конец турнира должен быть позже начала")
        return self


class TournamentUpdate(TournamentCreate):
    # PUT replaces editable tournament fields. Lifecycle flags are intentionally not exposed as arbitrary statuses.
    canceled: bool = False
    finished: bool = False


class TournamentRead(ORMModel):
    id: int
    name: str
    game: Game
    capacity: int
    prize_rub: int
    starts_at: datetime
    registration_closes_at: datetime
    ends_at: datetime | None
    canceled: bool
    finished: bool
    registered_teams: int
    status: str


class TeamInput(BaseModel):
    name: str = Field(min_length=2, max_length=120)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Название команды должно содержать минимум 2 символа")
        return value


class PlayerInput(BaseModel):
    nickname: str = Field(min_length=1, max_length=80)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    is_captain: bool = False

    @field_validator("nickname", "first_name", "last_name")
    @classmethod
    def clean_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value


class PlayerRead(ORMModel):
    id: int
    team_id: int
    nickname: str
    first_name: str
    last_name: str
    is_captain: bool


class TeamRead(ORMModel):
    id: int
    tournament_id: int
    name: str
    players: list[PlayerRead]
    max_players: int = 5


class MatchCreate(BaseModel):
    home_team_id: int = Field(gt=0)
    away_team_id: int = Field(gt=0)
    scheduled_at: datetime

    @field_validator("scheduled_at")
    @classmethod
    def timezone_required(cls, v):
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError("Время матча должно включать часовой пояс")
        return v

    @model_validator(mode="after")
    def check_different(self):
        if self.home_team_id == self.away_team_id:
            raise ValueError("Команда не может играть против самой себя")
        return self


class MatchUpdate(MatchCreate):
    finished: bool = False
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def check_scores(self):
        if self.finished and (self.home_score is None or self.away_score is None):
            raise ValueError("Для завершённого матча нужно указать оба счёта")
        if not self.finished and (self.home_score is not None or self.away_score is not None):
            raise ValueError("Счёт указывают при завершении матча")
        return self


class MatchRead(ORMModel):
    id: int
    tournament_id: int
    home_team_id: int
    away_team_id: int
    scheduled_at: datetime
    home_score: int | None
    away_score: int | None
    finished: bool
    status: str
