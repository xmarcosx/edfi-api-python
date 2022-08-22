from typing import List
from uuid import UUID

from daos.school import SchoolDAO
from schemas.school import School, SchoolCreate, SchoolUpdate

school_dao = SchoolDAO()


class SchoolService:
    def create_school(self, school_create: SchoolCreate) -> School:
        return school_dao.create(school_create)

    def get_school(self, id: UUID) -> School:
        return school_dao.get(id)

    def list_schools(self) -> List[School]:
        return school_dao.list()

    def update_school(self, id: UUID, school_update: SchoolUpdate) -> School:
        return school_dao.update(id, school_update)

    def delete_school(self, id: UUID) -> None:
        return school_dao.delete(id)
