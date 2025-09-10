from sqlalchemy.orm import Session
from sqlalchemy import select
from src.domain.users import UserCreate
from src.interfaces.repositories.user_repo_interface import UserRepoInterface
from src.models.entities.user import User

class UserRepo(UserRepoInterface):
    
    def create(self, db: Session, user_params: UserCreate) -> User:
        try:
            new_user = User(
                name=user_params.name,
                email=user_params.email,
                timezone=user_params.timezone,
            )
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
