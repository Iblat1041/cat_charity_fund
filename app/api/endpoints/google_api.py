from typing import Any

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_projects_crud
from app.services import google_api
from app.services.constants import Limits

router = APIRouter()


@router.post(
    "/",
    response_model=dict[str, Any],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    limit: int = Limits.LIMIT.value,
    offset: int = Limits.LIMIT.value,
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Обрабатывает запрос, отправленный методом POST.

    Args:
        limit (int, optional): возвращает первые 10 строк
        offset (int, optional): пропускает указаное число строк
        session : объект AsyncSession для работы с асинхронными сессиями;
        wrapper_services : Aiogoogle — объект «обёртки», передаётся из настроек
    Returns:
        _type_: _description_
    """
    reservations = await charity_projects_crud.get_projects_by_completion_rate(
        limit, offset, session=session
    )
    spreadsheet_id, spreadsheet_url = await google_api.spreadsheets_create(
        wrapper_services
    )
    await google_api.set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await google_api.spreadsheets_update_value(
            spreadsheet_id,
            reservations,
            wrapper_services
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Возникла ошибка: {e}"
        )
    return {
        'spreadsheet_id': spreadsheet_id,
        'spreadsheet_url': spreadsheet_url
    }
