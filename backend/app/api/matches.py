from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Tournament, Match
from app.schemas.entities import MatchCreate, MatchUpdate, MatchRead
from app.api.common import require, commit, match_response, require_match_team, utc

router = APIRouter(prefix="/tournaments/{tournament_id}/matches", tags=["Матчи"])


def get_match(db, tournament_id, match_id):
    m = db.get(Match, match_id)
    if m is None or m.tournament_id != tournament_id:
        raise HTTPException(404, "Матч не найден в турнире")
    return m


def validate(db, tournament_id, data):
    t = require(db, Tournament, tournament_id)
    if t.canceled or t.finished:
        raise HTTPException(409, "Нельзя назначать матчи в закрытом турнире")
    require_match_team(db, tournament_id, data.home_team_id)
    require_match_team(db, tournament_id, data.away_team_id)
    if utc(data.scheduled_at) < utc(t.starts_at):
        raise HTTPException(422, "Матч не может начинаться раньше турнира")
    if t.ends_at and utc(data.scheduled_at) > utc(t.ends_at):
        raise HTTPException(422, "Матч не может начинаться после конца турнира")


@router.post("", response_model=MatchRead, status_code=201)
def create(tournament_id: int, data: MatchCreate, db: Session = Depends(get_db)):
    validate(db, tournament_id, data)
    m = Match(tournament_id=tournament_id, **data.model_dump())
    db.add(m)
    commit(db)
    return match_response(m)


@router.get("", response_model=list[MatchRead])
def list_all(tournament_id: int, db: Session = Depends(get_db)):
    require(db, Tournament, tournament_id)
    return [match_response(m) for m in db.scalars(select(Match).where(Match.tournament_id == tournament_id).order_by(Match.scheduled_at)).all()]


@router.get("/{match_id}", response_model=MatchRead)
def get_one(tournament_id: int, match_id: int, db: Session = Depends(get_db)):
    return match_response(get_match(db, tournament_id, match_id))


@router.put("/{match_id}", response_model=MatchRead)
def update(tournament_id: int, match_id: int, data: MatchUpdate, db: Session = Depends(get_db)):
    m = get_match(db, tournament_id, match_id)
    validate(db, tournament_id, data)
    for key, val in data.model_dump().items():
        setattr(m, key, val)
    commit(db)
    return match_response(m)


@router.delete("/{match_id}", status_code=204)
def delete(tournament_id: int, match_id: int, db: Session = Depends(get_db)):
    m = get_match(db, tournament_id, match_id)
    db.delete(m)
    commit(db)
    return Response(status_code=204)
