from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.entities import Tournament, Team, Match, Player


def require(db: Session, model: type, item_id: int):
    value = db.get(model, item_id)
    if value is None:
        raise HTTPException(404, "Запись не найдена")
    return value


def commit(db: Session):
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(409, "Дублирующиеся данные или нарушение ограничений БД") from error


def utc(dt: datetime):
    # SQLite test databases may return naive datetimes; PostgreSQL returns aware UTC instants.
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def tournament_status(t: Tournament):
    now = datetime.now(timezone.utc)
    if t.canceled:
        return "Отменён"
    if t.finished or (t.ends_at is not None and now >= utc(t.ends_at)):
        return "Завершён"
    if now >= utc(t.starts_at):
        return "Идёт"
    if now >= utc(t.registration_closes_at):
        return "Скоро"
    return "Регистрация"


def tournament_response(db: Session, t: Tournament):
    count = db.scalar(select(func.count(Team.id)).where(Team.tournament_id == t.id))
    return dict(id=t.id, name=t.name, game=t.game, capacity=t.capacity, prize_rub=t.prize_rub,
                starts_at=t.starts_at, registration_closes_at=t.registration_closes_at,
                ends_at=t.ends_at, canceled=t.canceled, finished=t.finished,
                registered_teams=count, status=tournament_status(t))


def match_response(m: Match):
    status = "Завершён" if m.finished else ("Идёт" if datetime.now(timezone.utc) >= utc(m.scheduled_at) else "Ожидается")
    return dict(id=m.id, tournament_id=m.tournament_id, home_team_id=m.home_team_id,
                away_team_id=m.away_team_id, scheduled_at=m.scheduled_at, home_score=m.home_score,
                away_score=m.away_score, finished=m.finished, status=status)


def require_match_team(db: Session, tournament_id: int, team_id: int):
    team = db.get(Team, team_id)
    if team is None or team.tournament_id != tournament_id:
        raise HTTPException(422, f"Команда {team_id} не зарегистрирована на этом турнире")
    count = db.scalar(select(func.count(Player.id)).where(Player.team_id == team_id))
    captain_count = db.scalar(select(func.count(Player.id)).where(Player.team_id == team_id, Player.is_captain.is_(True)))
    if count != 5 or captain_count != 1:
        raise HTTPException(409, f"В команде {team_id} должно быть 5 игроков и 1 капитан для назначения матча")
