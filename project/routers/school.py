import os
from typing import List
import json
import motor.motor_asyncio
from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from schemas.school import SchoolModel, CreateSchoolModel, UpdateSchoolModel
from bson import json_util

router = APIRouter()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

responses = {
    200: {"description": "The resource was updated."},
    201: {"description": "The resource was created."},
    400: {
        "description": "Bad Request. The request was invalid and cannot be completed. See the response body for specific validation errors. This will typically be an issue with the query parameters or their values."
    },
    401: {
        "description": "Unauthorized. The request requires authentication. The OAuth bearer token was either not provided or is invalid. The operation may succeed once authentication has been successfully completed."
    },
    403: {
        "description": "Forbidden. The request cannot be completed in the current authorization context. Contact your administrator if you believe this operation should be allowed."
    },
    405: {
        "description": "Method Is Not Allowed. When the Snapshot-Identifier header is present the method is not allowed."
    },
    409: {
        "description": "Conflict. The request cannot be completed because it would result in an invalid state. See the response body for details."
    },
    412: {
        "description": "The resource's current server-side ETag value does not match the supplied If-Match header value in the request. This indicates the resource has been modified by another consumer."
    },
    500: {
        "description": "An unhandled error occurred on the server. See the response body for details."
    },
}


@router.post(
    "/schools", response_model=SchoolModel, responses={**responses}, tags=["schools"]
)
async def create_school(school: CreateSchoolModel = Body(...)) -> SchoolModel:
    """
    Accepts json matching pydantic model createschoolmodel
    Converts to SchoolModel allowing id and last_modified_date to populate
    Document inserted and retrieved
    """
    new_school = await client.edfi.schools.insert_one(
        SchoolModel(**school.dict()).mongo()
    )
    if new_school.acknowledged:
        created = await client.edfi.schools.find_one({"_id": new_school.inserted_id})
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(SchoolModel.from_mongo(created)),
        )
    else:
        raise HTTPException(status_code=409, detail="Unable to store document.")


# @router.get("/schools/{id}", response_model=SchoolModel, tags=["schools"])
# def get_school(id: UUID4) -> SchoolModel:
#     school = school_service.get_school(id)
#     if not school:
#         raise HTTPException(status_code=404, detail="School not found.")
#     return school


@router.get(
    "/schools",
    response_model=List[SchoolModel],
    tags=["schools"],
    description="This GET operation provides access to resources using the 'Get' search pattern. The values of any properties of the resource that are specified will be used to return all matching results (if it exists).",
)
async def list_schools(
    offset: int = Query(
        default=0,
        description="Indicates how many items should be skipped before returning results.",
    ),
    limit: int = Query(
        default=2500,
        description="Indicates the maximum number of items that should be returned in the results.",
    ),
    total_count: bool = Query(
        default=False,
        alias="totalCount",
        description="Indicates if the total number of items available should be returned in the 'Total-Count' header of the response. If set to false, 'Total-Count' header will not be provided.",
    ),
    school_id: int
    | None = Query(
        default=None,
        alias="schoolId",
        description="The identifier assigned to a school.",
    ),
    local_education_agency_id: int
    | None = Query(
        default=None,
        alias="localEducationAgencyId",
        description="The identifier assigned to a local education agency.",
    ),
    charter_approval_school_year: int
    | None = Query(
        default=None,
        alias="charterApprovalSchoolYear",
        description="The school year in which a charter school was initially approved.",
    ),
    administrative_funding_control_descriptor: str
    | None = Query(
        default=None,
        alias="administrativeFundingControlDescriptor",
        description="The type of education institution as classified by its funding source, for example public or private.",
    ),
    charterApprovalAgencyTypeDescriptor: str
    | None = Query(
        None,
        description="The type of agency that approved the establishment or continuation of a charter school.",
    ),
    charter_status_descriptor: str
    | None = Query(
        default=None,
        alias="charterStatusDescriptor",
        description="A school or agency providing free public elementary or secondary education to eligible students under a specific charter granted by the state legislature or other appropriate authority and designated by such authority to be a charter school.",
    ),
    internet_access_descriptor: str
    | None = Query(
        default=None,
        alias="internetAccessDescriptor",
        description="The type of Internet access available.",
    ),
    magnetSpecialProgramEmphasisSchoolDescriptor: str
    | None = Query(
        None,
        description="A school that has been designed: 1) to attract students of different racial/ethnic backgrounds for the purpose of reducing, preventing, or eliminating racial isolation; and/or 2) to provide an academic or social focus on a particular theme (e.g., science/math, performing arts, gifted/talented, or foreign language).",
    ),
    school_type_descriptor: str
    | None = Query(
        default=None,
        alias="schoolTypeDescriptor",
        description="The type of education institution as classified by its primary focus.",
    ),
    title_i_part_a_school_designation_descriptor: str
    | None = Query(
        default=None,
        alias="titleIPartASchoolDesignationDescriptor",
        description="Denotes the Title I Part A designation for the school.",
    ),
) -> List[SchoolModel]:
    schools = await client.edfi.schools.find().skip(offset).limit(limit).to_list(limit)
    return [SchoolModel.from_mongo(record) for record in schools]


# @router.put("/schools/{id}", response_model=SchoolModel, tags=["schools"])
# def update_school(id: UUID4, school_update: UpdateSchoolModel = Body(...)) -> SchoolModel:
#     school = school_service.get_school(id)
#     if not school:
#         raise HTTPException(status_code=404, detail="School not found.")
#     return school_service.update_school(id, school_update)


# @router.delete("/schools/{id}", response_model=SchoolModel, tags=["schools"])
# def delete_school(id: UUID4) -> SchoolModel:
#     school = school_service.get_school(id)
#     if not school:
#         raise HTTPException(status_code=404, detail="School not found.")
#     return school_service.delete_school(id)
