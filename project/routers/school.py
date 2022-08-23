from typing import List

from fastapi import APIRouter, Body, HTTPException, Query
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


@router.get(
    "/schools",
    response_model=List[School],
    tags=["schools"],
    description="This GET operation provides access to resources using the 'Get' search pattern. The values of any properties of the resource that are specified will be used to return all matching results (if it exists).",
)
def list_schools(
    offset: int = Query(
        0,
        description="Indicates how many items should be skipped before returning results.",
    ),
    limit: int = Query(
        2500,
        description="Indicates the maximum number of items that should be returned in the results.",
    ),
    totalCount: bool = Query(
        False,
        description="Indicates if the total number of items available should be returned in the 'Total-Count' header of the response. If set to false, 'Total-Count' header will not be provided.",
    ),
    schoolId: int
    | None = Query(None, description="The identifier assigned to a school."),
    localEducationAgencyId: int
    | None = Query(
        None, description="The identifier assigned to a local education agency."
    ),
    charterApprovalSchoolYear: int
    | None = Query(
        None,
        description="The school year in which a charter school was initially approved.",
    ),
    administrativeFundingControlDescriptor: str
    | None = Query(
        None,
        description="The type of education institution as classified by its funding source, for example public or private.",
    ),
    charterApprovalAgencyTypeDescriptor: str
    | None = Query(
        None,
        description="The type of agency that approved the establishment or continuation of a charter school.",
    ),
    charterStatusDescriptor: str
    | None = Query(
        None,
        description="A school or agency providing free public elementary or secondary education to eligible students under a specific charter granted by the state legislature or other appropriate authority and designated by such authority to be a charter school.",
    ),
    internetAccessDescriptor: str
    | None = Query(None, description="The type of Internet access available."),
    magnetSpecialProgramEmphasisSchoolDescriptor: str
    | None = Query(
        None,
        description="A school that has been designed: 1) to attract students of different racial/ethnic backgrounds for the purpose of reducing, preventing, or eliminating racial isolation; and/or 2) to provide an academic or social focus on a particular theme (e.g., science/math, performing arts, gifted/talented, or foreign language).",
    ),
    schoolTypeDescriptor: str
    | None = Query(
        None,
        description="The type of education institution as classified by its primary focus.",
    ),
    titleIPartASchoolDesignationDescriptor: str
    | None = Query(
        None, description="Denotes the Title I Part A designation for the school."
    ),
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
