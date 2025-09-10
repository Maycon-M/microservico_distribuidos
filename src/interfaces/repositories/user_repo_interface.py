from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.entities.user import User

class UserRepoInterface(ABC):
    
    @abstractmethod
    def create(self, db: Session, new_user: User) -> User:
        raise NotImplementedError
       
    @abstractmethod 
    def get_by_email(self, db: Session, email: str): 
        raise NotImplementedError
    
    @abstractmethod
    def get(self, db: Session, user_id: int): 
        raise NotImplementedError
