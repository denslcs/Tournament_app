from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Tournament
from app.schemas.entities import TournamentCreate, TournamentUpdate, TournamentRead
from app.api.common import require, commit, tournament_response

router = APIRouter(prefix="/tournaments", tags=["Турниры"])


@router.post("", response_model=TournamentRead, status_code=201)
def create(data: TournamentCreate, db: Session = Depends(get_db)):
    t = Tournament(**data.model_dump())
    db.add(t)
    commit(db)
    return tournament_response(db, t)


@router.get("", response_model=list[TournamentRead])
def list_all(db: Session = Depends(get_db)):
    return [tournament_response(db, t) for t in db.scalars(select(Tournament).order_by(Tournament.id)).all()]


@router.get("/{tournament_id}", response_model=TournamentRead)
def get_one(tournament_id: int, db: Session = Depends(get_db)):
    return tournament_response(db, require(db, Tournament, tournament_id))


@router.put("/{tournament_id}", response_model=TournamentRead)
def update(tournament_id: int, data: TournamentUpdate, db: Session = Depends(get_db)):
    t = require(db, Tournament, tournament_id)
    if t.finished and not data.finished:
        raise HTTPException(409, "Нельзя снова открыть завершённый турнир")
    if t.canceled and not data.canceled:
        raise HTTPException(409, "Нельзя снова открыть отменённый турнир")
    if data.canceled and data.finished:
        raise HTTPException(422, "Турнир не может одновременно быть отменён и завершён")
    for key, value in data.model_dump().items():
        setattr(t, key, value)
    commit(db)
    return tournament_response(db, t)


@router.delete("/{tournament_id}", status_code=204)
def delete(tournament_id: int, db: Session = Depends(get_db)):
    t = require(db, Tournament, tournament_id)
    db.delete(t)
    commit(db)
    return Response(status_code=204)
