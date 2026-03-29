# app/routers/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.stats import StatsResponse
from app.services import stats_service
from app.utils.security import require_admin

router = APIRouter(prefix="/stats", tags=["Estadísticas"])


@router.get("/", response_model=StatsResponse)
def get_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """
    Obtiene estadísticas de ventas. Solo admin.
    - days: cantidad de días hacia atrás para el historial (default 30)
    """
    return stats_service.get_stats(db, days)