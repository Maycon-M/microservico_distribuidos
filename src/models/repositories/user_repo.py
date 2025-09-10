from sqlalchemy.orm import Session
from sqlalchemy import select
from src.interfaces.repositories.user_repo_interface import UserRepoInterface
from src.models.entities.user import User

class UserRepo(UserRepoInterface):
    
    def create(self, db: Session, new_user: User) -> User:
        try:
            db.add(new_user)
            db.flush()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()
            raise e
        
    def get_by_email(self, db: Session, email: str): 
        return db.scalar(select(User).where(User.email==email))
    
    def get(self, db: Session, user_id: int): 
        return db.get(User, user_id)
