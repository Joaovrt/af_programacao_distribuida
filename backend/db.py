from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_engine('sqlite:///school.db', echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
  Base.metadata.create_all(bind=engine)