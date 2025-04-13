from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.project import Project
from schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from typing import List
from sqlalchemy.orm import joinedload
from .utils import definition

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects(db: AsyncSession = Depends(get_db)):
    stmt = select(Project).options(joinedload(Project.organization))
    result = await db.execute(stmt)
    projects = result.scalars().all()

    if not projects:
        raise HTTPException(status_code=404, detail="Проекты не найдены")

    return [
        ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            category=project.category,
            participants_count=project.participants_count,
            collected_amount=project.collected_amount,
            target_amount=project.target_amount,
            end_date=project.end_date,
            location=project.location,
            author_name=project.organization_id,
            co2=project.co2,
        )
        for project in projects
    ]

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")
    return project

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_project = Project(**project_data.dict())
        generated_value = definition(f"Посчитай макимально правильно и эффективно сколько  сколько CO2 сэкономлено. Нужно посчитать на основе наших данных. Дать четкий и понятный ответ. ОТВЕТ МНЕ ПРЕДОСТАВИТЬ ТОЛЬКО В ВИДЕ ЦИФРЫ, БЕЗ ТЕКСТА. ПРОСТО В ОТВЕТ ВЕРНИ МНЕ СКОЛЬКО БУДЕТ СЭКОНОМЛЕНО CO2 вот данные: {project_data}")
        new_project.co2 = generated_value
        new_project.organization_id = 1
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        return new_project
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при создании проекта: {str(e)}")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    # Обновляем данные
    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


# Удаление проекта
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    await db.delete(project)
    await db.commit()
    return {"message": "Проект успешно удален"}
