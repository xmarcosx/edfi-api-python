from __future__ import annotations

from datetime import datetime, date
from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseConfig, BaseModel, Field, validator, Extra
from bson import ObjectId
from bson.errors import InvalidId


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
    county_fips_code: str | None = Field(
        default=None,
        title="countyFIPSCode",
        alias="countyFIPSCode",
        description="The Federal Information Processing Standards (FIPS) numeric code for the county issued by the National Institute of Standards and Technology (NIST). Counties are considered to be the 'first-order subdivisions' of each State and statistically equivalent entity, regardless of their local designations (county, parish, borough, etc.) Counties in different States will have the same code. A unique county number is created when combined with the 2-digit FIPS State Code.",
    )
    do_not_publish_indicator: bool | None = Field(
        default=None,
        title="doNotPublishIndicator",
        alias="doNotPublishIndicator",
        description="An indication that the address should not be published.",
    )
    latitude: str | None = Field(
        default=None,
        title="latitude",
        alias="latitude",
        description="The geographic latitude of the physical address.",
    )
    longitude: str | None = Field(
        default=None,
        title="longitude",
        alias="longitude",
        description="The geographic longitude of the physical address.",
    )
    name_of_county: str | None = Field(
        default=None,
        title="nameOfCounty",
        alias="nameOfCounty",
        description="TThe name of the county, parish, borough, or comparable unit (within a state) in 'which an address is located.",
    )
    periods: List[EducationOrganizationPeriod] | None = Field(
        default=None,
        description="An unordered collection of educationOrganizationAddressPeriods. The time periods for which the address is valid. For physical addresses, the periods in which the person lived at that address.",
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


class SchoolYearTypeReference(BaseModel):
    school_year: int = Field(
        title="schoolYear",
        alias="schoolYear",
        description="The street number and street name or post office box number of an address.",
        identity="true",
    )


class EducationOrganizationCategory(BaseModel):
    education_organization_category_descriptor: str = Field(
        title="educationOrganizationCategoryDescriptor",
        alias="educationOrganizationCategoryDescriptor",
        example="uri://ed-fi.org/EducationOrganizationCategoryDescriptor#School",
        description="The classification of the education agency within the geographic boundaries of a state according to the level of administrative and operational control granted by the state.",
        identity="true",
    )


class EducationOrganizationIdentificationCode(BaseModel):
    education_organization_identification_system_descriptor: str = Field(
        title="educationOrganizationIdentificationSystemDescriptor",
        alias="educationOrganizationIdentificationSystemDescriptor",
        description="The school system, state, or agency assigning the identification code.",
        identity="true",
    )
    identification_code: str | None = Field(
        default=None,
        title="identificationCode",
        alias="identificationCode",
        description="A unique number or alphanumeric code that is assigned to an education organization by a school, school system, state, or other agency or entity.",
    )


class EducationOrganizationIndicator(BaseModel):
    indicator_descriptor: str = Field(
        title="indicatorDescriptor",
        alias="indicatorDescriptor",
        description="The name or code for the indicator or metric.",
        identity="true",
    )
    indicator_group_descriptor: str | None = Field(
        title="indicatorGroupDescriptor",
        alias="indicatorGroupDescriptor",
        description="The name or code for the indicator or metric.",
    )
    indicator_level_descriptor: str | None = Field(
        title="indicatorLevelDescriptor",
        alias="indicatorLevelDescriptor",
        description="The value of the indicator or metric, as a value from a controlled vocabulary. The semantics of an empty value is 'not submitted.'",
    )
    designaed_by: str | None = Field(
        title="designatedBy",
        alias="designatedBy",
        description="The value of the indicator or metric, as a value from a controlled vocabulary. The semantics of an empty value is 'not submitted.'",
    )
    indicator_value: str | None = Field(
        title="indicatorValue",
        alias="indicatorValue",
        description="The value of the indicator or metric, as a value from a controlled vocabulary. The semantics of an empty value is 'not submitted.'",
    )
    periods: List[EducationOrganizationPeriod] | None = Field(
        default=None,
        description="An unordered collection of educationOrganizationAddressPeriods. The time periods for which the address is valid. For physical addresses, the periods in which the person lived at that address.",
    )


class InstitutionTelephone(BaseModel):
    institutionTelephoneNumberTypeDescriptor: str
    telephoneNumber: str


class LocalEducationAgencyReference(BaseModel):
    local_education_agency_id: int = Field(
        title="localEducationAgencyId",
        alias="localEducationAgencyId",
        description="The identifier assigned to a local education agency.",
        identity="true",
    )


class PostSecondaryInstitutionReference(BaseModel):
    postSecondaryInstitutionId: int


class SchoolGradeLevel(BaseModel):
    grade_level_descriptor: str = Field(
        title="gradeLevelDescriptor",
        alias="gradeLevelDescriptor",
        example="uri://ed-fi.org/GradeLevelDescriptor#Ninth grade",
        description="The grade levels served at the school.",
        identity="true",
    )


class SchoolCategory(BaseModel):
    school_category_descriptor: str = Field(
        title="schoolCategoryDescriptor",
        alias="schoolCategoryDescriptor",
        example="uri://ed-fi.org/SchoolCategoryDescriptor#High School",
        description="The one or more categories of school.",
        identity="true",
    )


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
        description="An unordered collection of educationOrganizationAddresses. The set of elements that describes an address for the education entity, including the street address, city, state, ZIP code, and ZIP code + 4.",
    )
    administrative_funding_control_descriptor: str | None = Field(
        title="administrativeFundingControlDescriptor",
        alias="administrativeFundingControlDescriptor",
        description="The type of education institution as classified by its funding source, for example public or private.",
    )
    charter_approval_school_year_type_reference: SchoolYearTypeReference | None = Field(
        title="charterApprovalSchoolYearTypeReference",
        alias="charterApprovalSchoolYearTypeReference",
        description="",
    )
    charter_status_descriptor: str | None = Field(
        title="charterStatusDescriptor",
        alias="charterStatusDescriptor",
        description="A school or agency providing free public elementary or secondary education to eligible students under a specific charter granted by the state legislature or other appropriate authority and designated by such authority to be a charter school.",
    )
    education_organization_categories: List[EducationOrganizationCategory] = Field(
        title="educationOrganizationCategories",
        alias="educationOrganizationCategories",
        description="An unordered collection of educationOrganizationCategories. The classification of the education agency within the geographic boundaries of a state according to the level of administrative and operational control granted by the state.",
    )
    identification_codes: List[EducationOrganizationIdentificationCode] | None = Field(
        title="identificationCodes",
        alias="identificationCodes",
        description="An unordered collection of educationOrganizationIdentificationCodes. A unique number or alphanumeric code assigned to an education organization by a school, school system, a state, or other agency or entity.",
    )
    indicators: List[EducationOrganizationIndicator] | None = Field(
        title="indicators",
        alias="indicators",
        description="An unordered collection of educationOrganizationIndicators. An indicator or metric of an education organization.",
    )
    institutionTelephones: List[InstitutionTelephone] = None
    internationalAddresses: List[InternationalAddress] = None
    internet_access_descriptor: str | None = Field(
        title="internetAccessDescriptor",
        alias="internetAccessDescriptor",
        description="The type of Internet access available.",
    )
    magnet_special_program_emphasis_school_descriptor: str | None = Field(
        title="magnetSpecialProgramEmphasisSchoolDescriptor",
        alias="magnetSpecialProgramEmphasisSchoolDescriptor",
        description="A school that has been designed: 1) to attract students of different racial/ethnic backgrounds for the purpose of reducing, preventing, or eliminating racial isolation; and/or 2) to provide an academic or social focus on a particular theme (e.g., science/math, performing arts, gifted/talented, or foreign language).",
    )
    operational_status_descriptor: str | None = Field(
        title="operationalStatusDescriptor",
        alias="operationalStatusDescriptor",
        description="The current operational status of the education organization (e.g., active, inactive).",
    )
    local_education_agency_reference: LocalEducationAgencyReference | None = Field(
        title="localEducationAgencyReference",
        alias="localEducationAgencyReference",
        description="The type of education institution as classified by its primary focus.",
    )
    school_categories: List[SchoolCategory] | None = Field(
        title="schoolCategories",
        alias="schoolCategories",
        description="An unordered collection of schoolCategories. The one or more categories of school.",
    )
    school_type_descriptor: str | None = Field(
        title="schoolTypeDescriptor",
        alias="schoolTypeDescriptor",
        description="The type of education institution as classified by its primary focus.",
    )
    short_name_of_institution: str | None = Field(
        title="shortNameOfInstitution",
        alias="shortNameOfInstitution",
        description="A short name for the institution.",
    )
    title_i_part_a_school_designation_descriptor: str | None = Field(
        title="titleIPartASchoolDesignationDescriptor",
        alias="titleIPartASchoolDesignationDescriptor",
        description="Denotes the Title I Part A designation for the school.",
    )
    grade_levels: List[SchoolGradeLevel] = Field(
        title="gradeLevels",
        alias="gradeLevels",
        description="An unordered collection of schoolGradeLevels. The grade levels served at the school.",
    )
    web_site: str | None = Field(
        title="webSite",
        alias="webSite",
        description="The public web site address (URL) for the education organization.",
    )
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id"."""
        if not data:
            return data
        id = data.pop("_id", None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", False)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        # if "_id" not in parsed and "id" in parsed:
        #     parsed["_id"] = parsed.pop("id")
        if "_id" in parsed:
            parsed.pop("_id")
        if "id" in parsed:
            parsed.pop("id")
        return parsed


class CreateSchoolModel(SchoolBaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId)
    # _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateSchoolModel(SchoolBaseModel):
    _lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)


class SchoolModel(SchoolBaseModel):
    id: PyObjectId | None = None # Field(default_factory=PyObjectId)
    last_modified_date: datetime = Field(
        default_factory=datetime.utcnow, alias="_lastModifiedDate"
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
