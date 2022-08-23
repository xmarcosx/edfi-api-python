from __future__ import annotations

from datetime import datetime, date
from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class EducationOrganizationPeriod(BaseModel):
    begin_date: date = Field(
        title="beginDate",
        alias="beginDate",
        description="The month, day, and year for the start of the period.",
        identity="true",
    )
    end_date: date | None = Field(
        default=None,
        title="endDate",
        alias="endDate",
        description="The month, day, and year for the end of the period.",
    )


class EducationOrganizationAddress(BaseModel):
    address_type_descriptor: str = Field(
        title="addressTypeDescriptor",
        alias="addressTypeDescriptor",
        example="uri://ed-fi.org/AddressTypeDescriptor#Physical",
        description="The type of address listed for an individual or organization. For example: Physical Address, Mailing Address, Home Address, etc.)",
        identity="true",
    )
    state_abbreviation_descriptor: str = Field(
        title="stateAbbreviationDescriptor",
        alias="stateAbbreviationDescriptor",
        example="uri://ed-fi.org/StateAbbreviationDescriptor#TX",
        description="The abbreviation for the state (within the United States) or outlying area in which an address is located.",
        identity="true",
    )
    city: str = Field(
        title="city",
        alias="city",
        example="Grand Oaks",
        description="The name of the city in which an address is located.",
        identity="true",
    )
    postal_code: str = Field(
        title="postalCode",
        alias="postalCode",
        example="73334",
        description="The five or nine digit zip code or overseas postal code portion of an address.",
        identity="true",
    )
    street_number_name: str = Field(
        title="streetNumberName",
        alias="streetNumberName",
        example="456 Oaks Street",
        description="The street number and street name or post office box number of an address.",
        identity="true",
    )
    locale_descriptor: str | None = Field(
        default=None,
        title="localeDescriptor",
        alias="localeDescriptor",
        description="A general geographic indicator that categorizes U.S. territory (e.g., City, Suburban).",
    )
    apartment_room_suite_number: str | None = Field(
        default=None,
        title="apartmentRoomSuiteNumber",
        alias="apartmentRoomSuiteNumber",
        description="The apartment, room, or suite number of an address.",
    )
    building_site_number: str | None = Field(
        default=None,
        title="buildingSiteNumber",
        alias="buildingSiteNumber",
        description="The number of the building on the site, if more than one building shares the same address.",
    )
    congressional_district: str | None = Field(
        default=None,
        title="congressionalDistrict",
        alias="congressionalDistrict",
        description="The congressional district in which an address is located.",
    )
    county_fips_code: str| None = Field(
        default=None,
        title="countyFIPSCode",
        alias="countyFIPSCode",
        description="The Federal Information Processing Standards (FIPS) numeric code for the county issued by the National Institute of Standards and Technology (NIST). Counties are considered to be the 'first-order subdivisions' of each State and statistically equivalent entity, regardless of their local designations (county, parish, borough, etc.) Counties in different States will have the same code. A unique county number is created when combined with the 2-digit FIPS State Code.",
    )
    do_not_publish_indicator: bool| None = Field(
        default=None,
        title="doNotPublishIndicator",
        alias="doNotPublishIndicator",
        description="An indication that the address should not be published.",
    )
    latitude: str| None = Field(
        default=None,
        title="latitude",
        alias="latitude",
        description="The geographic latitude of the physical address.",
    )
    longitude: str| None = Field(
        default=None,
        title="longitude",
        alias="longitude",
        description="The geographic longitude of the physical address.",
    )
    name_of_county: str| None = Field(
        default=None,
        title="nameOfCounty",
        alias="nameOfCounty",
        description="TThe name of the county, parish, borough, or comparable unit (within a state) in 'which an address is located.",
    )
    periods: List[EducationOrganizationPeriod] | None = Field(
        default=None,
        description="An unordered collection of educationOrganizationAddressPeriods. The time periods for which the address is valid. For physical addresses, the periods in which the person lived at that address."
    )


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
    periods: List[EducationOrganizationPeriod]


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
class SchoolBaseModel(BaseModel):
    school_id: int = Field(
        title="schoolId",
        alias="schoolId",
        example="123456",
        description="The identifier assigned to a school.",
        identity="true",
    )
    name_of_institution: str = Field(
        title="nameOfInstitution",
        alias="nameOfInstitution",
        example="Grand Oaks High School",
        description="The full, legally accepted name of the institution.",
    )
    addresses: List[EducationOrganizationAddress] | None = Field(
        default=None,
        title="addresses",
        description="An unordered collection of educationOrganizationAddresses. The set of elements that describes an address for the education entity, including the street address, city, state, ZIP code, and ZIP code + 4."
    )
    administrativeFundingControlDescriptor: str | None = None
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
    schoolCategories: List[SchoolCategory] = None
    schoolTypeDescriptor: str = None
    shortNameOfInstitution: str = None
    titleIPartASchoolDesignationDescriptor: str = None
    gradeLevels: List[GradeLevel]
    webSite: str = None

# class CreateSchoolModel(SchoolBaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)

#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}


class UpdateSchoolModel(SchoolBaseModel):
    _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)


class SchoolModel(SchoolBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
