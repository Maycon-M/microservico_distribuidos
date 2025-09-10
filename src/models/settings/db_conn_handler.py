from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from src.core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

@event.listens_for(engine, "before_cursor_execute")
def _enable_fast_executemany(_conn, cursor, _statement, _parameters, _context, executemany):
    if executemany and hasattr(cursor, "fast_executemany"):
        cursor.fast_executemany = True

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)

def get_session() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
