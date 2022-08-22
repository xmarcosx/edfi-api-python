from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Address(BaseModel):
    addressTypeDescriptor: str
    city: str
    postalCode: str
    stateAbbreviationDescriptor: str
    streetNumberName: str
    nameOfCounty: str
    periods: List


class EducationOrganizationCategory(BaseModel):
    educationOrganizationCategoryDescriptor: str


class PostSecondaryInstitutionReference(BaseModel):
    postSecondaryInstitutionId: int


class GradeLevel(BaseModel):
    gradeLevelDescriptor: str


class School(BaseModel):
    schoolId: int
    nameOfInstitution: str
    addresses: List[Address]
    educationOrganizationCategories: List[EducationOrganizationCategory]
    identificationCodes: List
    indicators: List
    institutionTelephones: List
    internationalAddresses: List
    schoolCategories: List
    gradeLevels: List[GradeLevel]
    webSite: str = None
