from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user import User
from models.project import Project
from models.organization import Organization
from database import get_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.user import User
from models.project import Project
from database import get_db

admin_router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="admin/templates")

from sqlalchemy import select
from sqlalchemy import func

@admin_router.get("/projects", response_class=HTMLResponse)
async def admin_projects(
    request: Request,
    db: Session = Depends(get_db)
):
    # Запрос проектов
    result = await db.execute(
        select(Project)
        .where(Project.status == "moderation")
    )
    projects = result.scalars().all()
    
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects}
    )

@admin_router.post("/projects/{project_id}/approve")
async def approve_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db)
):
    # Получение проекта
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if project:
        project.status = "approved"
        await db.commit()
    result = await db.execute(
        select(Project)
        .where(Project.status == "moderation")
    )
    projects = result.scalars().all()
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects}
    )

@admin_router.post("/projects/{project_id}/delete")
async def delete_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db)
):
    # Получаем проект
    result = await db.execute(
        select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Меняем статус
    project.status = "deleted"
    
    try:
        await db.commit()
        await db.refresh(project)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    # Получаем обновленный список
    new_result = await db.execute(
        select(Project)
        .where(Project.status == "moderation")
    )
    projects = new_result.scalars().all()
    
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects}
    )

@admin_router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10
):
    try:
        # Получаем общее количество пользователей
        total_count = await db.execute(select(func.count(User.id)))
        total = total_count.scalar()

        # Получаем пользователей с пагинацией
        offset = (page - 1) * per_page
        result = await db.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        users = result.scalars().all()

        return templates.TemplateResponse(
            "users.html",
            {
                "request": request,
                "users": users,
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при загрузке пользователей: {str(e)}"
        )

from sqlalchemy import select, func
from models.organization import Organization

@admin_router.get("/organizations", response_class=HTMLResponse)
async def admin_organizations(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10
):
    try:
        # Общее количество организаций
        total_count = await db.execute(select(func.count(Organization.id)))
        total = total_count.scalar()

        # Пагинация
        offset = (page - 1) * per_page
        result = await db.execute(
            select(Organization)
            .offset(offset)
            .limit(per_page)
        )
        organizations = result.scalars().all()

        return templates.TemplateResponse(
            "organization.html",
            {
                "request": request,
                "organizations": organizations,
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при загрузке организаций: {str(e)}"
        )
