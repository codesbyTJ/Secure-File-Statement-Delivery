from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from urllib.parse import urlparse

# read from env or use defaults (change for production!)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1234@localhost/capitec_db")

def _ensure_mysql_db(url: str) -> bool:
    # try to create the database if it doesn't exist; return True on success
    try:
        import pymysql
    except ImportError:
        return False

    if not url.startswith("mysql+pymysql://"):
        return False

    # parse out components
    parsed = urlparse(url.replace("mysql+pymysql://", "http://"))
    user = parsed.username or "root"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 3306
    dbname = parsed.path.lstrip("/") or "capitec_db"

    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# If MySQL is requested try to ensure DB exists, otherwise fall back to sqlite for dev
if DATABASE_URL.startswith("mysql+pymysql://"):
    ok = _ensure_mysql_db(DATABASE_URL)
    if not ok:
        # fallback
        DATABASE_URL = "sqlite:///./dev.db"
        connect_args = {"check_same_thread": False}
    else:
        connect_args = {}
else:
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
