from __future__ import annotations

from datetime import datetime, date
from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class Period(BaseModel):
    beginDate: date
    endDate: date

    @validator("beginDate", "endDate")
    def parse_date(cls, value):
        return datetime.combine(value, datetime.min.time())


class Address(BaseModel):
    addressTypeDescriptor: str
    apartmentRoomSuiteNumber: str = None
    buildingSiteNumber: str = None
    city: str
    congressionalDistrict: str = None
    countyFIPSCode: str = None
    doNotPublishIndicator: bool = None
    latitude: str = None
    longitude: str = None
    localeDescriptor: str = None
    nameOfCounty: str = None
    postalCode: str
    stateAbbreviationDescriptor: str
    streetNumberName: str
    nameOfCounty: str
    periods: List[Period]


class InternationalAddress(BaseModel):
    addressTypeDescriptor: str
    countryDescriptor: str
    addressLine1: str
    addressLine2: str
    addressLine3: str
    addressLine4: str
    beginDate: date
    endDate: date
    latitude: str = None
    longitude: str = None

    @validator("beginDate", "endDate")
    def parse_date(cls, value):
        return datetime.combine(value, datetime.min.time())


class CharterApprovalSchoolYearType(BaseModel):
    schoolYear: int


class EducationOrganizationCategory(BaseModel):
    educationOrganizationCategoryDescriptor: str


class IdentificationCode(BaseModel):
    educationOrganizationIdentificationSystemDescriptor: str
    identificationCode: str


class Indicator(BaseModel):
    indicatorDescriptor: str
    indicatorGroupDescriptor: str
    indicatorLevelDescriptor: str
    designatedBy: str
    indicatorValue: str
    periods: List[Period]


class InstitutionTelephone(BaseModel):
    institutionTelephoneNumberTypeDescriptor: str
    telephoneNumber: str


class LocalEducationAgency(BaseModel):
    localEducationAgencyId: int


class PostSecondaryInstitutionReference(BaseModel):
    postSecondaryInstitutionId: int


class GradeLevel(BaseModel):
    gradeLevelDescriptor: str


class SchoolCategory(BaseModel):
    schoolCategoryDescriptor: str

# school models
class SchoolBase(BaseModel):
    schoolId: int
    nameOfInstitution: str
    addresses: List[Address]
    administrativeFundingControlDescriptor: str = None
    charterApprovalSchoolYearTypeReference: CharterApprovalSchoolYearType = None
    charterStatusDescriptor: str = None
    educationOrganizationCategories: List[EducationOrganizationCategory]
    identificationCodes: List[IdentificationCode] = None
    indicators: List[Indicator] = None
    institutionTelephones: List[InstitutionTelephone] = None
    internationalAddresses: List[InternationalAddress] = None
    internetAccessDescriptor: str = None
    magnetSpecialProgramEmphasisSchoolDescriptor: str = None
    operationalStatusDescriptor: str = None
    localEducationAgencyReference: LocalEducationAgency
    schoolCategories: List[SchoolCategory]= None
    schoolTypeDescriptor: str = None
    shortNameOfInstitution: str = None
    titleIPartASchoolDesignationDescriptor: str = None
    gradeLevels: List[GradeLevel]
    webSite: str = None


class SchoolCreate(SchoolBase):
    id: UUID = Field(default_factory=uuid4)
    _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)


class SchoolUpdate(SchoolBase):
    _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)


class School(SchoolBase):
    id: UUID
    _lastModifiedDate: datetime

    class Config:
        orm_mode = True
