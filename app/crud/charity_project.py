
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ):
        return await session.scalars(
            select(self.model).where(
                self.model.name == project_name
            )
        )

    async def get_projects_by_completion_rate(
        self,
        limit: int = None,
        offset: int = None, *,
        session: AsyncSession
    ) -> list[CharityProject]:
        """
        Cортирует список со всеми закрытыми проектами по количеству времени,
        которое понадобилось на сбор средств, — от меньшего к большему.
        """
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.description,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label("open_duration")
            ).where(CharityProject.fully_invested).order_by("open_duration")
            .limit(limit)
            .offset(offset)
        )
        return projects.fetchall()


charity_projects_crud = CRUDCharityProject(CharityProject)
