from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


user="root"
password="1234"##HArd coded password for testing purpose
dbname="capitec_db"

DATABAE_URL="mysql+pymysql://root:1234@localhost/capitec_db"

engine = create_engine(DATABAE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
