from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from app.models.entities import Tournament, Team, Match
from app.schemas.entities import TeamInput, TeamRead
from app.api.common import require, commit, tournament_status

router = APIRouter(prefix="/tournaments/{tournament_id}/teams", tags=["Команды и регистрация"])


def get_team(db, tournament_id, team_id):
    t = db.scalar(select(Team).options(selectinload(Team.players)).where(Team.id == team_id, Team.tournament_id == tournament_id))
    if t is None:
        raise HTTPException(404, "Команда не найдена в турнире")
    return t


@router.post("", response_model=TeamRead, status_code=201)
def create(tournament_id: int, data: TeamInput, db: Session = Depends(get_db)):
    t = db.scalar(select(Tournament).where(Tournament.id == tournament_id).with_for_update())
    if t is None:
        raise HTTPException(404, "Турнир не найден")
    if tournament_status(t) != "Регистрация":
        raise HTTPException(409, "Регистрация на турнир закрыта")
    count = db.scalar(select(func.count(Team.id)).where(Team.tournament_id == tournament_id))
    if count >= t.capacity:
        raise HTTPException(409, "Все места в турнире заняты")
    if db.scalar(select(Team.id).where(Team.tournament_id == tournament_id, func.lower(Team.name) == data.name.lower())):
        raise HTTPException(409, "Команда с таким названием уже есть")
    team = Team(tournament_id=tournament_id, name=data.name)
    db.add(team)
    commit(db)
    db.refresh(team)
    return team


@router.get("", response_model=list[TeamRead])
def list_all(tournament_id: int, db: Session = Depends(get_db)):
    require(db, Tournament, tournament_id)
    return db.scalars(select(Team).options(selectinload(Team.players)).where(Team.tournament_id == tournament_id).order_by(Team.id)).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_one(tournament_id: int, team_id: int, db: Session = Depends(get_db)):
    return get_team(db, tournament_id, team_id)


@router.put("/{team_id}", response_model=TeamRead)
def update(tournament_id: int, team_id: int, data: TeamInput, db: Session = Depends(get_db)):
    t = require(db, Tournament, tournament_id)
    if tournament_status(t) in ("Завершён", "Отменён"):
        raise HTTPException(409, "Редактирование закрытого турнира запрещено")
    team = get_team(db, tournament_id, team_id)
    if db.scalar(select(Team.id).where(Team.tournament_id == tournament_id, Team.id != team_id, func.lower(Team.name) == data.name.lower())):
        raise HTTPException(409, "Команда с таким названием уже есть")
    team.name = data.name
    commit(db)
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=204)
def delete(tournament_id: int, team_id: int, db: Session = Depends(get_db)):
    t = require(db, Tournament, tournament_id)
    if tournament_status(t) != "Регистрация":
        raise HTTPException(409, "Отменить регистрацию можно только пока она открыта")
    team = get_team(db, tournament_id, team_id)
    linked = db.scalar(select(Match.id).where((Match.home_team_id == team_id) | (Match.away_team_id == team_id)).limit(1))
    if linked is not None:
        raise HTTPException(409, "Команда участвует в назначенном матче")
    db.delete(team)
    commit(db)
    return Response(status_code=204)
