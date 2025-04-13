from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.organization import Organization
from schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# 1. Просмотр всех организаций
@router.get("/", response_model=list[OrganizationResponse])
async def get_all_organizations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization))
    organizations = result.scalars().all()
    return organizations


# 2. Просмотр организации по ID
@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization_by_id(org_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена")
    return organization


# 3. Создание новой организации
@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_org = Organization(**org_data.dict())
        db.add(new_org)
        await db.commit()
        await db.refresh(new_org)
        return new_org
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при создании организации: {str(e)}")


# 4. Обновление данных организации
@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int, org_data: OrganizationUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена")

    # Обновляем данные
    for key, value in org_data.dict(exclude_unset=True).items():
        setattr(organization, key, value)

    await db.commit()
    await db.refresh(organization)
    return organization


# 5. Удаление организации
@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization).filter(Organization.id == org_id))
    organization = result.scalar_one_or_none()
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена")

    await db.delete(organization)
    await db.commit()
    return {"message": "Организация успешно удалена"}