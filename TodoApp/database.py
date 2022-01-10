from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234!@127.0.0.1:3306/todoapp"
# engine
engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)

# session maker function
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base - to create db model
Base = declarative_base()

# connect to sqlite db
