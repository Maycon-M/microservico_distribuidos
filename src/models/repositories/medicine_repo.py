from sqlalchemy.orm import Session
from sqlalchemy import select
from src.interfaces.repositories.medicine_repo_interface import MedicineRepoInterface
from src.models.entities.medicine import Medicine

class MedicineRepo (MedicineRepoInterface):
    def create(self, db: Session, new_medicine: Medicine) -> Medicine:
        try:
            db.add(new_medicine)
            db.flush()
            db.refresh(new_medicine)
            return new_medicine
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, med_id: int): 
        return db.get(Medicine, med_id)
    
    def list_by_user(self, db: Session, user_id: int): 
        return list(db.scalars(select(Medicine).where(Medicine.user_id==user_id)))
