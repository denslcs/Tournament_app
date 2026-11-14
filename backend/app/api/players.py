from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Player, Tournament, Match, Team
from app.api.teams import get_team
from app.api.common import commit, require, tournament_status
from app.schemas.entities import PlayerInput, PlayerRead

router = APIRouter(prefix="/tournaments/{tournament_id}/teams/{team_id}/players", tags=["Игроки"])


def editable(db, tournament_id, team_id):
    tournament = require(db, Tournament, tournament_id)
    if tournament_status(tournament) != "Регистрация":
        raise HTTPException(409, "Изменять состав можно только во время регистрации")
    team = get_team(db, tournament_id, team_id)
    if db.scalar(select(Match.id).where((Match.home_team_id == team_id) | (Match.away_team_id == team_id)).limit(1)):
        raise HTTPException(409, "Состав нельзя изменить после назначения матча")
    return team


def get_player(db, tournament_id, team_id, player_id):
    get_team(db, tournament_id, team_id)
    player = db.get(Player, player_id)
    if player is None or player.team_id != team_id:
        raise HTTPException(404, "Игрок не найден в этой команде")
    return player


def validate_nickname(db, team_id, nickname, skip_id=None):
    query = select(Player.id).where(Player.team_id == team_id, func.lower(Player.nickname) == nickname.lower())
    if skip_id is not None:
        query = query.where(Player.id != skip_id)
    if db.scalar(query) is not None:
        raise HTTPException(409, "Игрок с таким ником уже есть в команде")


def set_captain(db, team_id, player):
    for other in db.scalars(select(Player).where(Player.team_id == team_id, Player.id != player.id)):
        other.is_captain = False
    player.is_captain = True


@router.post("", response_model=PlayerRead, status_code=201)
def create(tournament_id: int, team_id: int, data: PlayerInput, db: Session = Depends(get_db)):
    team = db.scalar(select(Team).where(Team.id == team_id, Team.tournament_id == tournament_id).with_for_update())
    if team is None:
        raise HTTPException(404, "Команда не найдена в турнире")
    editable(db, tournament_id, team_id)
    if db.scalar(select(func.count(Player.id)).where(Player.team_id == team_id)) >= 5:
        raise HTTPException(409, "В команде уже пять игроков")
    validate_nickname(db, team_id, data.nickname)
    player = Player(team_id=team_id, **data.model_dump())
    db.add(player)
    db.flush()
    if data.is_captain:
        set_captain(db, team_id, player)
    commit(db)
    db.refresh(player)
    return player


@router.get("", response_model=list[PlayerRead])
def list_all(tournament_id: int, team_id: int, db: Session = Depends(get_db)):
    get_team(db, tournament_id, team_id)
    return db.scalars(select(Player).where(Player.team_id == team_id).order_by(Player.id)).all()


@router.get("/{player_id}", response_model=PlayerRead)
def get_one(tournament_id: int, team_id: int, player_id: int, db: Session = Depends(get_db)):
    return get_player(db, tournament_id, team_id, player_id)


@router.put("/{player_id}", response_model=PlayerRead)
def update(tournament_id: int, team_id: int, player_id: int, data: PlayerInput, db: Session = Depends(get_db)):
    editable(db, tournament_id, team_id)
    player = get_player(db, tournament_id, team_id, player_id)
    validate_nickname(db, team_id, data.nickname, skip_id=player_id)
    for key, value in data.model_dump().items():
        setattr(player, key, value)
    if data.is_captain:
        set_captain(db, team_id, player)
    commit(db)
    db.refresh(player)
    return player


@router.delete("/{player_id}", status_code=204)
def delete(tournament_id: int, team_id: int, player_id: int, db: Session = Depends(get_db)):
    editable(db, tournament_id, team_id)
    player = get_player(db, tournament_id, team_id, player_id)
    db.delete(player)
    commit(db)
    return Response(status_code=204)
