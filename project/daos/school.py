from typing import List
from uuid import UUID

from database import db
from schemas.school import School, SchoolCreate, SchoolUpdate


class SchoolDAO:
    collection_name = "schools"

    def create(self, school_create: SchoolCreate) -> School:
        data = school_create.dict()
        data["id"] = str(data["id"])
        doc_ref = db.collection(self.collection_name).document(str(school_create.id))
        doc_ref.set(data)
        return self.get(school_create.id)

    def get(self, id: UUID) -> School:
        doc_ref = db.collection(self.collection_name).document(str(id))
        doc = doc_ref.get()
        if doc.exists:
            return School(**doc.to_dict())
        return

    def list(self) -> List[School]:
        schools_ref = db.collection(self.collection_name)
        return [
            School(**doc.get().to_dict())
            for doc in schools_ref.list_documents()
            if doc.get().to_dict()
        ]

    def update(self, id: UUID, school_update: SchoolUpdate) -> School:
        data = school_update.dict()
        doc_ref = db.collection(self.collection_name).document(str(id))
        doc_ref.update(data)
        return self.get(id)

    def delete(self, id: UUID) -> None:
        db.collection(self.collection_name).document(str(id)).delete()
