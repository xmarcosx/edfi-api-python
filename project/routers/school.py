from typing import List

from fastapi import APIRouter, Body, HTTPException
from pydantic.types import UUID4

from schemas.school import School, SchoolCreate, SchoolUpdate
from services.school import SchoolService

router = APIRouter()
school_service = SchoolService()


@router.post("/schools", response_model=School, tags=["schools"])
def create_school(school_create: SchoolCreate = Body(...)) -> School:
    return school_service.create_school(school_create)


@router.get("/schools/{id}", response_model=School, tags=["schools"])
def get_school(id: UUID4) -> School:
    school = school_service.get_school(id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found.")
    return school


@router.get("/schools", response_model=List[School], tags=["schools"])
def list_schools(
    offset: int = 0,
    limit: int = 2500,
    totalCount: bool = False,
    schoolId: int | None = None,
    localEducationAgencyId: int | None = None,
    charterApprovalSchoolYear: int | None = None,
    administrativeFundingControlDescriptor: str | None = None,
    charterApprovalAgencyTypeDescriptor: str | None = None,
    charterStatusDescriptor: str | None = None,
    internetAccessDescriptor: str | None = None,
    magnetSpecialProgramEmphasisSchoolDescriptor: str | None = None,
    schoolTypeDescriptor: str | None = None,
    titleIPartASchoolDesignationDescriptor: str | None = None,
) -> List[School]:
    schools = school_service.list_schools()
    return schools


@router.put("/schools/{id}", response_model=School, tags=["schools"])
def update_school(id: UUID4, school_update: SchoolUpdate = Body(...)) -> School:
    school = school_service.get_school(id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found.")
    return school_service.update_school(id, school_update)


@router.delete("/schools/{id}", response_model=School, tags=["schools"])
def delete_school(id: UUID4) -> School:
    school = school_service.get_school(id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found.")
    return school_service.delete_school(id)
