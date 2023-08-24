from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_pass = os.getenv("POSTGRES_PASSWORD")
postgres_server = os.getenv("POSTGRES_SERVER")
postgres_db = os.getenv("POSTGRES_DB")


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{postgres_user}:{postgres_pass}@{postgres_server}/{postgres_db}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
